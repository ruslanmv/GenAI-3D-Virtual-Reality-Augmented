"""Unit tests for the Gradio application module.

Author: Ruslan Magana
Website: ruslanmv.com
"""

from unittest.mock import MagicMock, patch

import pytest
from PIL import Image

from genai_3d_vr_ar.app import generate_360_image, get_pipeline


@pytest.mark.unit
class TestGetPipeline:
    """Test Stable Diffusion pipeline initialization."""

    @patch("genai_3d_vr_ar.app.DiffusionPipeline")
    @patch("genai_3d_vr_ar.app.get_global_config")
    @patch("genai_3d_vr_ar.app.torch")
    def test_get_pipeline_success(
        self,
        mock_torch: MagicMock,
        mock_get_config: MagicMock,
        mock_pipeline_class: MagicMock,
    ) -> None:
        """Test successful pipeline initialization."""
        # Clear cached pipeline
        import genai_3d_vr_ar.app
        genai_3d_vr_ar.app._pipeline = None

        # Mock configuration
        mock_config = MagicMock()
        mock_config.stable_diffusion.model_id = "test/model"
        mock_config.stable_diffusion.use_lora = False
        mock_config.stable_diffusion.device = "cpu"
        mock_get_config.return_value = mock_config

        # Mock torch
        mock_torch.cuda.is_available.return_value = False

        # Mock pipeline
        mock_pipeline = MagicMock()
        mock_pipeline_class.from_pretrained.return_value = mock_pipeline

        # Test
        pipeline = get_pipeline()

        assert pipeline is not None
        mock_pipeline_class.from_pretrained.assert_called_once()


@pytest.mark.unit
class TestGenerate360Image:
    """Test 360° image generation function."""

    @patch("genai_3d_vr_ar.app.get_pipeline")
    @patch("genai_3d_vr_ar.app.generate_environment")
    @patch("genai_3d_vr_ar.app.get_global_config")
    def test_generate_360_image_success(
        self,
        mock_get_config: MagicMock,
        mock_generate_env: MagicMock,
        mock_get_pipeline: MagicMock,
        sample_prompt: str,
    ) -> None:
        """Test successful 360° image generation."""
        # Mock configuration
        mock_config = MagicMock()
        mock_config.stable_diffusion.num_inference_steps = 50
        mock_config.stable_diffusion.guidance_scale = 7.5
        mock_config.stable_diffusion.use_lora = True
        mock_config.stable_diffusion.trigger_word = "qxj"
        mock_get_config.return_value = mock_config

        # Mock environment generation
        mock_generate_env.return_value = "Enriched prompt description"

        # Mock pipeline
        mock_pipeline = MagicMock()
        mock_result = MagicMock()
        mock_image = Image.new("RGB", (512, 512))
        mock_result.images = [mock_image]
        mock_pipeline.return_value = mock_result
        mock_get_pipeline.return_value = mock_pipeline

        # Test
        image, message = generate_360_image(
            prompt=sample_prompt,
            enrichment_type="Standard",
        )

        assert image is not None
        assert isinstance(image, Image.Image)
        assert "Success" in message or "✅" in message
        mock_generate_env.assert_called_once()
        mock_pipeline.assert_called_once()

    def test_generate_360_image_empty_prompt(self) -> None:
        """Test error handling with empty prompt."""
        image, message = generate_360_image(
            prompt="",
            enrichment_type="Standard",
        )

        assert image is None
        assert "Error" in message or "❌" in message

    @patch("genai_3d_vr_ar.app.get_pipeline")
    @patch("genai_3d_vr_ar.app.generate_environment")
    @patch("genai_3d_vr_ar.app.get_global_config")
    def test_generate_360_image_enrichment_failure(
        self,
        mock_get_config: MagicMock,
        mock_generate_env: MagicMock,
        mock_get_pipeline: MagicMock,
        sample_prompt: str,
    ) -> None:
        """Test handling of prompt enrichment failure."""
        # Mock configuration
        mock_config = MagicMock()
        mock_config.stable_diffusion.num_inference_steps = 50
        mock_config.stable_diffusion.guidance_scale = 7.5
        mock_config.stable_diffusion.use_lora = False
        mock_get_config.return_value = mock_config

        # Mock failed enrichment (falls back to original prompt)
        from genai_3d_vr_ar.generate_environment import WatsonXModelError
        mock_generate_env.side_effect = WatsonXModelError("API Error")

        # Mock pipeline
        mock_pipeline = MagicMock()
        mock_result = MagicMock()
        mock_image = Image.new("RGB", (512, 512))
        mock_result.images = [mock_image]
        mock_pipeline.return_value = mock_result
        mock_get_pipeline.return_value = mock_pipeline

        # Test - should succeed with warning
        image, message = generate_360_image(
            prompt=sample_prompt,
            enrichment_type="Standard",
        )

        # Should still generate image despite enrichment failure
        assert image is not None
        mock_pipeline.assert_called_once()


@pytest.mark.integration
@pytest.mark.slow
class TestAppIntegration:
    """Integration tests for the application (requires models)."""

    @pytest.mark.skip(reason="Requires downloaded models and GPU")
    def test_full_pipeline_integration(self) -> None:
        """Test full pipeline with real models (skipped by default)."""
        image, message = generate_360_image(
            prompt="a tropical beach",
            enrichment_type="Standard",
        )

        assert image is not None
        assert isinstance(image, Image.Image)
        assert "Success" in message
