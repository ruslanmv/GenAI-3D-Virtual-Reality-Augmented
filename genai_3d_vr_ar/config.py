"""Configuration management for GenAI 3D VR/AR platform.

This module provides centralized configuration management with environment
variable loading, validation, and default values.

Author: Ruslan Magana
Website: ruslanmv.com
"""

import logging
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


@dataclass
class WatsonXConfig:
    """Configuration for IBM WatsonX.ai services.

    Attributes:
        api_key: IBM Cloud API key for authentication
        project_id: WatsonX.ai project identifier
        url: WatsonX.ai service endpoint URL
        model_type: Default LLM model type to use
        max_tokens: Maximum number of tokens to generate
        min_tokens: Minimum number of tokens to generate
        temperature: Sampling temperature (0.0 to 1.0)
        decoding_method: Decoding strategy (SAMPLE, GREEDY)
    """

    api_key: str
    project_id: str
    url: str = "https://us-south.ml.cloud.ibm.com"
    model_type: str = "ibm/mpt-7b-instruct2"
    max_tokens: int = 250
    min_tokens: int = 150
    temperature: float = 0.7
    decoding_method: str = "sample"


@dataclass
class StableDiffusionConfig:
    """Configuration for Stable Diffusion image generation.

    Attributes:
        model_id: Hugging Face model identifier
        use_lora: Whether to use LoRA fine-tuning
        lora_model_id: LoRA model identifier if enabled
        trigger_word: Special trigger word for LoRA models
        num_inference_steps: Number of denoising steps
        guidance_scale: Classifier-free guidance scale
        device: Computation device (cuda, cpu, mps)
    """

    model_id: str = "runwayml/stable-diffusion-v1-5"
    use_lora: bool = True
    lora_model_id: str = "ProGamerGov/360-Diffusion-LoRA-sd-v1-5"
    trigger_word: str = "qxj"
    num_inference_steps: int = 50
    guidance_scale: float = 7.5
    device: str = "cuda"


@dataclass
class ApplicationConfig:
    """Main application configuration.

    Attributes:
        debug: Enable debug mode
        log_level: Logging level
        watsonx: WatsonX.ai configuration
        stable_diffusion: Stable Diffusion configuration
    """

    debug: bool = False
    log_level: str = "INFO"
    watsonx: WatsonXConfig = None  # type: ignore
    stable_diffusion: StableDiffusionConfig = None  # type: ignore


class ConfigurationError(Exception):
    """Raised when configuration is invalid or incomplete."""

    pass


def load_environment(env_path: Optional[Path] = None) -> None:
    """Load environment variables from .env file.

    Args:
        env_path: Optional path to .env file. If None, searches in current and parent directories.

    Raises:
        ConfigurationError: If .env file is not found or cannot be loaded
    """
    if env_path is None:
        # Search for .env in current and parent directories
        current_dir = Path.cwd()
        env_candidates = [
            current_dir / ".env",
            current_dir.parent / ".env",
        ]

        for candidate in env_candidates:
            if candidate.exists():
                env_path = candidate
                break

    if env_path and env_path.exists():
        load_dotenv(dotenv_path=env_path)
        logger.info(f"Loaded environment from {env_path}")
    else:
        logger.warning("No .env file found, using environment variables only")


def get_watsonx_config() -> WatsonXConfig:
    """Get WatsonX.ai configuration from environment variables.

    Returns:
        WatsonXConfig: Validated WatsonX.ai configuration

    Raises:
        ConfigurationError: If required environment variables are missing or invalid
    """
    api_key = os.getenv("API_KEY") or os.getenv("api_key")
    project_id = os.getenv("PROJECT_ID") or os.getenv("project_id")

    if not api_key or api_key.startswith("<your"):
        raise ConfigurationError(
            "API_KEY not found or contains placeholder value. "
            "Please set API_KEY environment variable with your IBM Cloud API key."
        )

    if not project_id or project_id.startswith("<your"):
        raise ConfigurationError(
            "PROJECT_ID not found or contains placeholder value. "
            "Please set PROJECT_ID environment variable with your WatsonX.ai project ID."
        )

    url = os.getenv("WATSONX_URL", "https://us-south.ml.cloud.ibm.com")
    model_type = os.getenv("WATSONX_MODEL_TYPE", "ibm/mpt-7b-instruct2")

    # Parse numeric values with defaults
    try:
        max_tokens = int(os.getenv("WATSONX_MAX_TOKENS", "250"))
        min_tokens = int(os.getenv("WATSONX_MIN_TOKENS", "150"))
        temperature = float(os.getenv("WATSONX_TEMPERATURE", "0.7"))
    except ValueError as e:
        raise ConfigurationError(f"Invalid numeric configuration value: {e}")

    decoding_method = os.getenv("WATSONX_DECODING_METHOD", "sample").upper()

    logger.info(f"WatsonX.ai configured with model: {model_type}")

    return WatsonXConfig(
        api_key=api_key,
        project_id=project_id,
        url=url,
        model_type=model_type,
        max_tokens=max_tokens,
        min_tokens=min_tokens,
        temperature=temperature,
        decoding_method=decoding_method,
    )


def get_stable_diffusion_config() -> StableDiffusionConfig:
    """Get Stable Diffusion configuration from environment variables.

    Returns:
        StableDiffusionConfig: Stable Diffusion configuration with defaults
    """
    model_id = os.getenv("SD_MODEL_ID", "runwayml/stable-diffusion-v1-5")
    use_lora = os.getenv("SD_USE_LORA", "true").lower() == "true"
    lora_model_id = os.getenv("SD_LORA_MODEL_ID", "ProGamerGov/360-Diffusion-LoRA-sd-v1-5")
    trigger_word = os.getenv("SD_TRIGGER_WORD", "qxj")

    try:
        num_inference_steps = int(os.getenv("SD_NUM_INFERENCE_STEPS", "50"))
        guidance_scale = float(os.getenv("SD_GUIDANCE_SCALE", "7.5"))
    except ValueError as e:
        logger.warning(f"Invalid SD numeric config, using defaults: {e}")
        num_inference_steps = 50
        guidance_scale = 7.5

    device = os.getenv("SD_DEVICE", "cuda")

    logger.info(f"Stable Diffusion configured: model={model_id}, device={device}")

    return StableDiffusionConfig(
        model_id=model_id,
        use_lora=use_lora,
        lora_model_id=lora_model_id,
        trigger_word=trigger_word,
        num_inference_steps=num_inference_steps,
        guidance_scale=guidance_scale,
        device=device,
    )


def get_config() -> ApplicationConfig:
    """Get complete application configuration.

    Returns:
        ApplicationConfig: Complete application configuration

    Raises:
        ConfigurationError: If configuration is invalid or incomplete
    """
    # Load environment variables
    load_environment()

    # Get debug and log level
    debug = os.getenv("DEBUG", "false").lower() == "true"
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()

    # Set logging level
    logging.getLogger().setLevel(log_level)

    # Get subsystem configurations
    watsonx_config = get_watsonx_config()
    sd_config = get_stable_diffusion_config()

    config = ApplicationConfig(
        debug=debug,
        log_level=log_level,
        watsonx=watsonx_config,
        stable_diffusion=sd_config,
    )

    logger.info("Application configuration loaded successfully")
    return config


# Create a global config instance
_global_config: Optional[ApplicationConfig] = None


def get_global_config() -> ApplicationConfig:
    """Get or create the global configuration instance.

    Returns:
        ApplicationConfig: Global application configuration
    """
    global _global_config
    if _global_config is None:
        _global_config = get_config()
    return _global_config


if __name__ == "__main__":
    # Test configuration loading
    try:
        config = get_config()
        print("✓ Configuration loaded successfully!")
        print(f"  WatsonX Model: {config.watsonx.model_type}")
        print(f"  SD Model: {config.stable_diffusion.model_id}")
        print(f"  Debug Mode: {config.debug}")
    except ConfigurationError as e:
        print(f"✗ Configuration error: {e}")
