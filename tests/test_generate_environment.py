"""Unit tests for environment generation module.

Author: Ruslan Magana
Website: ruslanmv.com
"""

from unittest.mock import MagicMock, patch

import pytest

from genai_3d_vr_ar.generate_environment import (
    WatsonXModelError,
    generate_environment,
    get_model,
)


@pytest.mark.unit
class TestGetModel:
    """Test WatsonX model creation."""

    @patch("genai_3d_vr_ar.generate_environment.Model")
    def test_get_model_success(self, mock_model_class: MagicMock) -> None:
        """Test successful model creation."""
        mock_model = MagicMock()
        mock_model_class.return_value = mock_model

        model = get_model(
            model_type="ibm/mpt-7b-instruct2",
            max_tokens=250,
            min_tokens=150,
            decoding="sample",
            temperature=0.7,
            api_key="test_key",
            project_id="test_project",
        )

        assert model == mock_model
        mock_model_class.assert_called_once()

    def test_get_model_invalid_temperature(self) -> None:
        """Test model creation with invalid temperature."""
        with pytest.raises(ValueError, match="Temperature"):
            get_model(
                model_type="test",
                max_tokens=100,
                min_tokens=50,
                decoding="sample",
                temperature=2.0,  # Invalid: > 1.0
                api_key="test",
                project_id="test",
            )

    def test_get_model_invalid_tokens(self) -> None:
        """Test model creation with invalid token values."""
        with pytest.raises(ValueError, match="min_tokens"):
            get_model(
                model_type="test",
                max_tokens=100,
                min_tokens=200,  # Invalid: > max_tokens
                decoding="sample",
                temperature=0.7,
                api_key="test",
                project_id="test",
            )

    def test_get_model_invalid_decoding(self) -> None:
        """Test model creation with invalid decoding method."""
        with pytest.raises(ValueError, match="decoding method"):
            get_model(
                model_type="test",
                max_tokens=100,
                min_tokens=50,
                decoding="invalid_method",
                temperature=0.7,
                api_key="test",
                project_id="test",
            )


@pytest.mark.unit
class TestGenerateEnvironment:
    """Test environment description generation."""

    @patch("genai_3d_vr_ar.generate_environment.get_model")
    @patch("genai_3d_vr_ar.generate_environment.get_global_config")
    def test_generate_environment_success(
        self,
        mock_get_config: MagicMock,
        mock_get_model: MagicMock,
        mock_watsonx_response: dict,
        test_env,
    ) -> None:
        """Test successful environment generation."""
        # Mock configuration
        mock_config = MagicMock()
        mock_config.watsonx.model_type = "ibm/mpt-7b-instruct2"
        mock_config.watsonx.max_tokens = 250
        mock_config.watsonx.min_tokens = 150
        mock_config.watsonx.decoding_method = "sample"
        mock_config.watsonx.temperature = 0.7
        mock_config.watsonx.api_key = "test_key"
        mock_config.watsonx.project_id = "test_project"
        mock_config.watsonx.url = "https://test.ibm.com"
        mock_get_config.return_value = mock_config

        # Mock model
        mock_model = MagicMock()
        mock_model.generate.return_value = mock_watsonx_response
        mock_get_model.return_value = mock_model

        # Test
        result = generate_environment("tropical beach")

        assert isinstance(result, str)
        assert len(result) > 0
        mock_model.generate.assert_called_once()

    def test_generate_environment_empty_prompt(self) -> None:
        """Test error with empty prompt."""
        with pytest.raises(ValueError, match="empty"):
            generate_environment("")

    @patch("genai_3d_vr_ar.generate_environment.get_model")
    @patch("genai_3d_vr_ar.generate_environment.get_global_config")
    def test_generate_environment_model_error(
        self,
        mock_get_config: MagicMock,
        mock_get_model: MagicMock,
    ) -> None:
        """Test error handling when model generation fails."""
        mock_config = MagicMock()
        mock_config.watsonx.model_type = "test"
        mock_config.watsonx.max_tokens = 250
        mock_config.watsonx.min_tokens = 150
        mock_config.watsonx.decoding_method = "sample"
        mock_config.watsonx.temperature = 0.7
        mock_config.watsonx.api_key = "test"
        mock_config.watsonx.project_id = "test"
        mock_config.watsonx.url = "https://test.com"
        mock_get_config.return_value = mock_config

        mock_model = MagicMock()
        mock_model.generate.return_value = {}  # Empty response
        mock_get_model.return_value = mock_model

        with pytest.raises(WatsonXModelError, match="empty"):
            generate_environment("test prompt")


@pytest.mark.integration
class TestGenerateEnvironmentIntegration:
    """Integration tests for environment generation (requires credentials)."""

    @pytest.mark.skip(reason="Requires valid IBM Cloud credentials")
    def test_generate_environment_real_api(self) -> None:
        """Test with real API (skipped by default)."""
        result = generate_environment("a mystical forest")
        assert isinstance(result, str)
        assert len(result) > 50
