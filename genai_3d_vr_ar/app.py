"""Gradio web application for 360° image generation.

This module provides a production-ready Gradio web interface for generating
360-degree equirectangular images using Stable Diffusion with LoRA fine-tuning
and IBM WatsonX.ai prompt enrichment.

Author: Ruslan Magana
Website: ruslanmv.com

Example:
    Run the web application::

        $ python -m genai_3d_vr_ar.app

    Or use the entry point::

        $ genai-3d-vr
"""

import logging
import sys
from typing import Optional, Tuple

import gradio as gr
import torch
from diffusers import DiffusionPipeline, StableDiffusionPipeline
from PIL import Image

from genai_3d_vr_ar.config import ConfigurationError, get_global_config
from genai_3d_vr_ar.generate_environment import (
    WatsonXModelError,
    generate_environment,
)

# Configure logging
logger = logging.getLogger(__name__)

# Global pipeline instance (initialized on first use)
_pipeline: Optional[StableDiffusionPipeline] = None


class ImageGenerationError(Exception):
    """Raised when image generation fails."""

    pass


def get_pipeline() -> StableDiffusionPipeline:
    """Get or create the Stable Diffusion pipeline instance.

    This function initializes the Stable Diffusion pipeline with LoRA fine-tuning
    on first call and returns the cached instance on subsequent calls.

    Returns:
        StableDiffusionPipeline: Configured Stable Diffusion pipeline

    Raises:
        ImageGenerationError: If pipeline initialization fails
        ConfigurationError: If configuration is invalid
    """
    global _pipeline

    if _pipeline is not None:
        return _pipeline

    try:
        logger.info("Initializing Stable Diffusion pipeline...")

        # Load configuration
        config = get_global_config()
        sd_config = config.stable_diffusion

        # Determine device
        device = sd_config.device
        if device == "cuda" and not torch.cuda.is_available():
            logger.warning("CUDA requested but not available, falling back to CPU")
            device = "cpu"

        logger.info(f"Using device: {device}")

        # Load base Stable Diffusion model
        logger.info(f"Loading base model: {sd_config.model_id}")

        pipeline = DiffusionPipeline.from_pretrained(
            sd_config.model_id,
            torch_dtype=torch.float16 if device == "cuda" else torch.float32,
            safety_checker=None,  # Disable for performance
            requires_safety_checker=False,
        )

        # Load LoRA weights if enabled
        if sd_config.use_lora and sd_config.lora_model_id:
            logger.info(f"Loading LoRA weights: {sd_config.lora_model_id}")
            try:
                pipeline.load_lora_weights(sd_config.lora_model_id)
                logger.info("LoRA weights loaded successfully")
            except Exception as e:
                logger.warning(f"Failed to load LoRA weights: {e}")
                logger.warning("Continuing without LoRA fine-tuning")

        # Move to device and optimize
        pipeline = pipeline.to(device)

        if device == "cuda":
            # Enable memory optimizations
            pipeline.enable_attention_slicing()
            logger.info("Enabled attention slicing for memory optimization")

        logger.info("Pipeline initialization complete")
        _pipeline = pipeline

        return _pipeline

    except Exception as e:
        error_msg = f"Failed to initialize Stable Diffusion pipeline: {str(e)}"
        logger.error(error_msg)
        raise ImageGenerationError(error_msg) from e


def generate_360_image(
    prompt: str,
    enrichment_type: str,
    custom_data: Optional[str] = None,
    num_inference_steps: Optional[int] = None,
    guidance_scale: Optional[float] = None,
) -> Tuple[Optional[Image.Image], str]:
    """Generate a 360° equirectangular image from a text prompt.

    This function enriches the user prompt using WatsonX.ai, then generates
    a 360-degree image using Stable Diffusion with LoRA fine-tuning.

    Args:
        prompt: User-provided text description of the desired scene
        enrichment_type: Type of enrichment to apply ('Standard', 'Detailed', 'Cinematic')
        custom_data: Optional custom data for advanced enrichment
        num_inference_steps: Optional number of denoising steps (default from config)
        guidance_scale: Optional classifier-free guidance scale (default from config)

    Returns:
        Tuple[Optional[Image.Image], str]: Generated image and status message

    Example:
        >>> image, message = generate_360_image("tropical beach", "Standard")
        >>> image.save("beach_360.png")
    """
    try:
        # Validate input
        if not prompt or not prompt.strip():
            error_msg = "❌ Error: Prompt cannot be empty"
            logger.warning("Empty prompt provided")
            return None, error_msg

        logger.info(f"Generating 360° image for prompt: '{prompt[:50]}...'")

        # Load configuration
        config = get_global_config()
        sd_config = config.stable_diffusion

        # Use provided parameters or defaults
        num_inference_steps = num_inference_steps or sd_config.num_inference_steps
        guidance_scale = guidance_scale or sd_config.guidance_scale

        # Step 1: Enrich prompt with WatsonX.ai
        status_msg = "🔄 Enriching prompt with WatsonX.ai..."
        logger.info(status_msg)

        try:
            enriched_prompt = generate_environment(prompt)
            logger.info(f"Prompt enriched successfully ({len(enriched_prompt)} chars)")
        except WatsonXModelError as e:
            logger.warning(f"Prompt enrichment failed, using original: {e}")
            enriched_prompt = prompt
            status_msg = (
                "⚠️ Warning: Could not enrich prompt, using original. "
                f"Proceeding with generation...\n{str(e)}"
            )

        # Add trigger word for LoRA if enabled
        if sd_config.use_lora and sd_config.trigger_word:
            enriched_prompt = f"{sd_config.trigger_word} {enriched_prompt}"
            logger.info(f"Added LoRA trigger word: {sd_config.trigger_word}")

        # Step 2: Generate image
        status_msg = "🎨 Generating 360° image with Stable Diffusion..."
        logger.info(status_msg)

        pipeline = get_pipeline()

        # Generate image
        with torch.inference_mode():
            result = pipeline(
                prompt=enriched_prompt,
                num_inference_steps=num_inference_steps,
                guidance_scale=guidance_scale,
            )

        if not result or not result.images:
            raise ImageGenerationError("Pipeline returned no images")

        image = result.images[0]

        success_msg = (
            f"✅ Success! Generated 360° image\n"
            f"Resolution: {image.size[0]}x{image.size[1]}\n"
            f"Inference Steps: {num_inference_steps}\n"
            f"Guidance Scale: {guidance_scale}"
        )

        logger.info(f"Image generated successfully: {image.size}")

        return image, success_msg

    except ConfigurationError as e:
        error_msg = f"❌ Configuration Error: {str(e)}\n\nPlease check your .env file."
        logger.error(error_msg)
        return None, error_msg

    except ImageGenerationError as e:
        error_msg = f"❌ Image Generation Error: {str(e)}"
        logger.error(error_msg)
        return None, error_msg

    except Exception as e:
        error_msg = f"❌ Unexpected Error: {str(e)}"
        logger.exception("Unexpected error during image generation")
        return None, error_msg


def create_interface() -> gr.Blocks:
    """Create and configure the Gradio interface.

    Returns:
        gr.Blocks: Configured Gradio interface

    Example:
        >>> interface = create_interface()
        >>> interface.launch()
    """
    with gr.Blocks(
        title="GenAI 3D VR/AR - 360° Image Generator",
        theme=gr.themes.Soft(),
    ) as interface:
        # Header
        gr.Markdown(
            """
            # 🌐 GenAI 3D VR/AR Platform
            ## 360° Image Generation with AI

            **Powered by IBM WatsonX.ai & Stable Diffusion**

            Generate stunning 360-degree equirectangular images for VR/AR experiences.
            Compatible with Meta Quest 3, Apple Vision Pro, and other VR headsets.

            ---
            """
        )

        # Input section
        with gr.Row():
            with gr.Column(scale=2):
                prompt_input = gr.Textbox(
                    label="Scene Description",
                    placeholder="Describe your desired 360° environment (e.g., 'a tropical beach at sunset with palm trees')",
                    lines=3,
                    max_lines=5,
                )

                with gr.Row():
                    enrichment_type = gr.Dropdown(
                        label="Enrichment Type",
                        choices=["Standard", "Detailed", "Cinematic"],
                        value="Standard",
                        info="How much detail to add to your prompt",
                    )

                    custom_data = gr.Textbox(
                        label="Custom Data (Optional)",
                        placeholder="Additional context or requirements",
                        lines=1,
                    )

                with gr.Accordion("Advanced Settings", open=False):
                    num_steps = gr.Slider(
                        minimum=20,
                        maximum=100,
                        value=50,
                        step=5,
                        label="Inference Steps",
                        info="More steps = higher quality but slower",
                    )

                    guidance = gr.Slider(
                        minimum=1.0,
                        maximum=15.0,
                        value=7.5,
                        step=0.5,
                        label="Guidance Scale",
                        info="How closely to follow the prompt",
                    )

                generate_btn = gr.Button(
                    "🎨 Generate 360° Image",
                    variant="primary",
                    size="lg",
                )

            with gr.Column(scale=3):
                image_output = gr.Image(
                    label="Generated 360° Image",
                    type="pil",
                    height=400,
                )

                status_output = gr.Textbox(
                    label="Status",
                    lines=4,
                    max_lines=8,
                    interactive=False,
                )

        # Examples
        gr.Examples(
            examples=[
                ["a tropical beach at sunset with palm trees and crystal clear water", "Standard"],
                ["a futuristic cyberpunk city street at night with neon signs", "Detailed"],
                ["a mystical forest with glowing mushrooms and fireflies", "Cinematic"],
                ["a cozy mountain cabin interior with fireplace and wooden furniture", "Standard"],
                ["an alien landscape with multiple moons and exotic plants", "Detailed"],
            ],
            inputs=[prompt_input, enrichment_type],
            label="Example Prompts",
        )

        # Footer
        gr.Markdown(
            """
            ---
            **Author:** Ruslan Magana | **Website:** [ruslanmv.com](https://ruslanmv.com)

            **License:** Apache 2.0 | **Version:** 1.0.0

            💡 **Tip:** For best results, be specific about lighting, atmosphere, and key elements in your scene.
            """
        )

        # Connect event handler
        generate_btn.click(
            fn=generate_360_image,
            inputs=[
                prompt_input,
                enrichment_type,
                custom_data,
                num_steps,
                guidance,
            ],
            outputs=[image_output, status_output],
        )

    return interface


def main() -> None:
    """Main entry point for the Gradio web application.

    Initializes and launches the web interface for 360° image generation.
    """
    print("=" * 70)
    print("GenAI 3D VR/AR Platform - 360° Image Generator")
    print("Author: Ruslan Magana | Website: ruslanmv.com")
    print("=" * 70)
    print()

    try:
        # Validate configuration
        logger.info("Validating configuration...")
        config = get_global_config()
        logger.info("Configuration validated successfully")

        # Pre-initialize pipeline (optional, for faster first generation)
        logger.info("Pre-initializing Stable Diffusion pipeline...")
        get_pipeline()
        logger.info("Pipeline ready")

        # Create and launch interface
        logger.info("Creating Gradio interface...")
        interface = create_interface()

        logger.info("Launching web application...")
        interface.launch(
            server_name="0.0.0.0",
            server_port=7860,
            share=False,
            show_error=True,
        )

    except ConfigurationError as e:
        print(f"\n✗ Configuration Error: {e}")
        print("\nPlease ensure your .env file contains:")
        print("  - API_KEY=<your_ibm_cloud_api_key>")
        print("  - PROJECT_ID=<your_watsonx_project_id>")
        sys.exit(1)

    except ImageGenerationError as e:
        print(f"\n✗ Pipeline Initialization Error: {e}")
        sys.exit(1)

    except KeyboardInterrupt:
        print("\n\nShutting down gracefully...")
        sys.exit(0)

    except Exception as e:
        print(f"\n✗ Unexpected Error: {e}")
        logger.exception("Unexpected error in main()")
        sys.exit(1)


if __name__ == "__main__":
    main()
