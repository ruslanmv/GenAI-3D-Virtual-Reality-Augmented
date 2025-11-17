"""Unit tests for configuration module.

Author: Ruslan Magana
Website: ruslanmv.com
"""

import os
from pathlib import Path

import pytest

from genai_3d_vr_ar.config import (
    ConfigurationError,
    WatsonXConfig,
    get_config,
    get_stable_diffusion_config,
    get_watsonx_config,
    load_environment,
)


@pytest.mark.unit
class TestWatsonXConfig:
    """Test WatsonX configuration dataclass."""

    def test_watsonx_config_creation(self) -> None:
        """Test creating WatsonX configuration."""
        config = WatsonXConfig(
            api_key="test_key",
            project_id="test_project",
        )

        assert config.api_key == "test_key"
        assert config.project_id == "test_project"
        assert config.url == "https://us-south.ml.cloud.ibm.com"
        assert config.max_tokens == 250
        assert config.min_tokens == 150
        assert config.temperature == 0.7


@pytest.mark.unit
class TestLoadEnvironment:
    """Test environment loading functionality."""

    def test_load_environment_from_file(self, temp_env_file: Path) -> None:
        """Test loading environment from .env file."""
        load_environment(temp_env_file)

        assert os.getenv("API_KEY") == "test_api_key"
        assert os.getenv("PROJECT_ID") == "test_project_id"


@pytest.mark.unit
class TestGetWatsonXConfig:
    """Test WatsonX configuration retrieval."""

    def test_get_watsonx_config_success(self, test_env) -> None:
        """Test successful WatsonX configuration retrieval."""
        config = get_watsonx_config()

        assert config.api_key == "test_api_key_12345"
        assert config.project_id == "test_project_id_67890"

    def test_get_watsonx_config_missing_api_key(self) -> None:
        """Test error when API_KEY is missing."""
        # Clear environment variables
        os.environ.pop("API_KEY", None)
        os.environ.pop("api_key", None)

        with pytest.raises(ConfigurationError, match="API_KEY"):
            get_watsonx_config()

    def test_get_watsonx_config_placeholder_values(self) -> None:
        """Test error when credentials contain placeholders."""
        os.environ["API_KEY"] = "<your_api_key>"
        os.environ["PROJECT_ID"] = "test_project"

        with pytest.raises(ConfigurationError, match="placeholder"):
            get_watsonx_config()


@pytest.mark.unit
class TestGetStableDiffusionConfig:
    """Test Stable Diffusion configuration retrieval."""

    def test_get_sd_config_defaults(self) -> None:
        """Test SD configuration with default values."""
        config = get_stable_diffusion_config()

        assert config.model_id == "runwayml/stable-diffusion-v1-5"
        assert config.use_lora is True
        assert config.num_inference_steps == 50
        assert config.device == "cuda"

    def test_get_sd_config_custom_values(self) -> None:
        """Test SD configuration with custom environment values."""
        os.environ["SD_MODEL_ID"] = "custom/model"
        os.environ["SD_NUM_INFERENCE_STEPS"] = "75"
        os.environ["SD_DEVICE"] = "cpu"

        config = get_stable_diffusion_config()

        assert config.model_id == "custom/model"
        assert config.num_inference_steps == 75
        assert config.device == "cpu"

        # Cleanup
        os.environ.pop("SD_MODEL_ID", None)
        os.environ.pop("SD_NUM_INFERENCE_STEPS", None)
        os.environ.pop("SD_DEVICE", None)


@pytest.mark.unit
class TestGetConfig:
    """Test complete application configuration retrieval."""

    def test_get_config_success(self, test_env) -> None:
        """Test successful configuration loading."""
        config = get_config()

        assert config.watsonx is not None
        assert config.stable_diffusion is not None
        assert isinstance(config.debug, bool)
