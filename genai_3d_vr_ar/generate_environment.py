"""Environment description generator using IBM WatsonX.ai.

This module provides functionality to generate detailed environmental descriptions
using IBM WatsonX.ai's Large Language Models (LLMs). It enriches simple text prompts
into comprehensive, vivid descriptions suitable for 3D scene generation.

Author: Ruslan Magana
Website: ruslanmv.com

Example:
    Basic usage::

        from genai_3d_vr_ar.generate_environment import generate_environment

        prompt = "a tropical beach at sunset"
        description = generate_environment(prompt)
        print(description)

    Command-line usage::

        $ python -m genai_3d_vr_ar.generate_environment
        Describe your desired environment: a mystical forest
        [Generated description...]
"""

import logging
import sys
from typing import Dict, Optional

from ibm_watson_machine_learning.foundation_models import Model
from ibm_watson_machine_learning.foundation_models.utils.enums import (
    DecodingMethods,
    ModelTypes,
)
from ibm_watson_machine_learning.metanames import GenTextParamsMetaNames as GenParams

from genai_3d_vr_ar.config import ConfigurationError, get_global_config

# Configure logging
logger = logging.getLogger(__name__)


class WatsonXModelError(Exception):
    """Raised when WatsonX.ai model operations fail."""

    pass


def get_model(
    model_type: str,
    max_tokens: int,
    min_tokens: int,
    decoding: str,
    temperature: float,
    api_key: str,
    project_id: str,
    url: str = "https://us-south.ml.cloud.ibm.com",
) -> Model:
    """Create and configure a WatsonX.ai LLM model instance.

    This function initializes an IBM Watson Machine Learning model with specified
    parameters for text generation tasks.

    Args:
        model_type: The model identifier (e.g., 'ibm/mpt-7b-instruct2')
        max_tokens: Maximum number of tokens to generate
        min_tokens: Minimum number of tokens to generate
        decoding: Decoding method ('sample', 'greedy')
        temperature: Sampling temperature (0.0 to 1.0) for randomness control
        api_key: IBM Cloud API key for authentication
        project_id: WatsonX.ai project identifier
        url: WatsonX.ai service endpoint URL

    Returns:
        Model: Configured WatsonX.ai model instance

    Raises:
        WatsonXModelError: If model creation or configuration fails
        ValueError: If parameters are invalid

    Example:
        >>> model = get_model(
        ...     model_type="ibm/mpt-7b-instruct2",
        ...     max_tokens=250,
        ...     min_tokens=150,
        ...     decoding="sample",
        ...     temperature=0.7,
        ...     api_key="your_api_key",
        ...     project_id="your_project_id"
        ... )
    """
    # Validate parameters
    if not 0.0 <= temperature <= 1.0:
        raise ValueError(f"Temperature must be between 0.0 and 1.0, got {temperature}")

    if min_tokens > max_tokens:
        raise ValueError(
            f"min_tokens ({min_tokens}) cannot be greater than max_tokens ({max_tokens})"
        )

    if max_tokens <= 0:
        raise ValueError(f"max_tokens must be positive, got {max_tokens}")

    # Map decoding method string to enum
    decoding_method_map = {
        "sample": DecodingMethods.SAMPLE,
        "greedy": DecodingMethods.GREEDY,
    }

    decoding_method = decoding_method_map.get(decoding.lower())
    if decoding_method is None:
        raise ValueError(
            f"Invalid decoding method '{decoding}'. Must be 'sample' or 'greedy'"
        )

    try:
        # Configure generation parameters
        generate_params: Dict[str, object] = {
            GenParams.MAX_NEW_TOKENS: max_tokens,
            GenParams.MIN_NEW_TOKENS: min_tokens,
            GenParams.DECODING_METHOD: decoding_method,
            GenParams.TEMPERATURE: temperature,
        }

        # Create model instance
        model = Model(
            model_id=model_type,
            params=generate_params,
            credentials={
                "apikey": api_key,
                "url": url,
            },
            project_id=project_id,
        )

        logger.info(
            f"WatsonX.ai model initialized: {model_type} "
            f"(temp={temperature}, max_tokens={max_tokens})"
        )

        return model

    except Exception as e:
        error_msg = f"Failed to create WatsonX.ai model: {str(e)}"
        logger.error(error_msg)
        raise WatsonXModelError(error_msg) from e


def generate_environment(
    prompt: str,
    model_type: Optional[str] = None,
    max_tokens: Optional[int] = None,
    min_tokens: Optional[int] = None,
    decoding: Optional[str] = None,
    temperature: Optional[float] = None,
) -> str:
    """Generate a detailed environmental description from a text prompt.

    This function takes a simple text prompt and uses WatsonX.ai to generate
    a comprehensive, detailed description suitable for 3D scene generation.

    Args:
        prompt: User-provided text describing the desired environment
        model_type: Optional model identifier (defaults to config)
        max_tokens: Optional max tokens (defaults to config)
        min_tokens: Optional min tokens (defaults to config)
        decoding: Optional decoding method (defaults to config)
        temperature: Optional temperature (defaults to config)

    Returns:
        str: Generated detailed environmental description

    Raises:
        WatsonXModelError: If model generation fails
        ConfigurationError: If configuration is invalid
        ValueError: If prompt is empty

    Example:
        >>> description = generate_environment("a cyberpunk city at night")
        >>> print(description)
        A neon-lit cyberpunk metropolis sprawls beneath a starless sky...
    """
    if not prompt or not prompt.strip():
        raise ValueError("Prompt cannot be empty")

    try:
        # Load configuration
        config = get_global_config()
        watsonx_config = config.watsonx

        # Use provided parameters or fall back to config
        model_type = model_type or watsonx_config.model_type
        max_tokens = max_tokens or watsonx_config.max_tokens
        min_tokens = min_tokens or watsonx_config.min_tokens
        decoding = decoding or watsonx_config.decoding_method
        temperature = temperature or watsonx_config.temperature

        logger.info(f"Generating environment description for prompt: '{prompt[:50]}...'")

        # Create model
        model = get_model(
            model_type=model_type,
            max_tokens=max_tokens,
            min_tokens=min_tokens,
            decoding=decoding,
            temperature=temperature,
            api_key=watsonx_config.api_key,
            project_id=watsonx_config.project_id,
            url=watsonx_config.url,
        )

        # Generate description
        enhanced_prompt = (
            f"Generate a detailed, vivid description of the following environment "
            f"for 3D scene generation. Include details about lighting, atmosphere, "
            f"textures, and spatial layout:\n\n{prompt}"
        )

        generated_response = model.generate(prompt=enhanced_prompt)

        # Extract generated text
        if (
            not generated_response
            or "results" not in generated_response
            or not generated_response["results"]
        ):
            raise WatsonXModelError("Model returned empty or invalid response")

        description = generated_response["results"][0]["generated_text"]

        logger.info(
            f"Successfully generated description ({len(description)} characters)"
        )

        return description.strip()

    except ConfigurationError as e:
        logger.error(f"Configuration error: {e}")
        raise

    except WatsonXModelError as e:
        logger.error(f"Model error: {e}")
        raise

    except Exception as e:
        error_msg = f"Unexpected error during environment generation: {str(e)}"
        logger.error(error_msg)
        raise WatsonXModelError(error_msg) from e


def main() -> None:
    """Command-line interface for environment description generation.

    Prompts the user for an environment description and generates a detailed
    version using WatsonX.ai.
    """
    print("=" * 70)
    print("GenAI 3D VR/AR Environment Generator")
    print("Powered by IBM WatsonX.ai")
    print("=" * 70)
    print()

    try:
        # Get user input
        user_prompt = input("Describe your desired environment: ").strip()

        if not user_prompt:
            print("Error: Prompt cannot be empty")
            sys.exit(1)

        print()
        print("Generating detailed description...")
        print("-" * 70)

        # Generate description
        environment_description = generate_environment(user_prompt)

        print()
        print("Generated Description:")
        print("=" * 70)
        print(environment_description)
        print("=" * 70)

    except ConfigurationError as e:
        print(f"\n✗ Configuration Error: {e}")
        print("\nPlease ensure your .env file contains:")
        print("  - API_KEY=<your_ibm_cloud_api_key>")
        print("  - PROJECT_ID=<your_watsonx_project_id>")
        sys.exit(1)

    except WatsonXModelError as e:
        print(f"\n✗ Model Error: {e}")
        sys.exit(1)

    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user")
        sys.exit(0)

    except Exception as e:
        print(f"\n✗ Unexpected Error: {e}")
        logger.exception("Unexpected error in main()")
        sys.exit(1)


if __name__ == "__main__":
    main()
