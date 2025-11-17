# GenAI 3D Virtual Reality & Augmented Reality Platform

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

> **Production-ready platform for generating immersive 3D VR/AR content using cutting-edge Generative AI technologies**

Powered by **IBM WatsonX.ai** and **Stable Diffusion**, this platform enables the creation of stunning 360-degree equirectangular images suitable for Virtual Reality and Augmented Reality experiences. Compatible with Meta Quest 3, Apple Vision Pro, and other modern VR/AR devices.

---

## 🌟 About

The **GenAI 3D VR/AR Platform** is a comprehensive, production-grade solution for AI-powered 3D content generation. It combines the power of Large Language Models (LLMs) for intelligent prompt enrichment with state-of-the-art diffusion models for high-quality 360° image synthesis.

### Key Highlights

- **🤖 AI-Powered Prompt Enrichment**: Leverages IBM WatsonX.ai's advanced LLMs to transform simple text prompts into rich, detailed scene descriptions
- **🎨 360° Image Generation**: Uses Stable Diffusion with LoRA fine-tuning to create immersive equirectangular images
- **🥽 VR/AR Ready**: Outputs are optimized for modern VR headsets (Meta Quest 3, Apple Vision Pro)
- **🎮 Unreal Engine Integration**: Includes guides for creating intelligent NPCs with conversational AI
- **🌐 Web Interface**: Beautiful, user-friendly Gradio interface for easy interaction
- **🏗️ Production-Ready**: Comprehensive error handling, logging, testing, and documentation

### Author

**Ruslan Magana**
🌐 Website: [ruslanmv.com](https://ruslanmv.com)
📧 Contact: contact@ruslanmv.com

---

## ✨ Features

### Core Capabilities

| Feature | Description |
|---------|-------------|
| **Prompt Enrichment** | Transform simple prompts into vivid, detailed scene descriptions using WatsonX.ai |
| **360° Image Synthesis** | Generate high-quality equirectangular images with Stable Diffusion |
| **LoRA Fine-tuning** | Specialized 360° image generation using custom LoRA weights |
| **Batch Processing** | Generate multiple variations with different parameters |
| **Web Interface** | Intuitive Gradio UI with real-time preview |
| **CLI Tools** | Command-line utilities for automation and integration |
| **Type Safety** | Comprehensive type hints throughout the codebase |
| **Error Handling** | Robust error handling with informative messages |
| **Logging** | Detailed logging for debugging and monitoring |
| **Testing** | Extensive unit and integration tests |

### Technical Stack

- **AI/ML**: IBM WatsonX.ai, Stable Diffusion, LoRA, PyTorch, Transformers
- **Web**: Gradio (Python web framework)
- **Development**: Python 3.10+, uv (package manager), pytest, ruff, black, mypy
- **Cloud**: AWS SageMaker ready, IBM Cloud integration
- **VR/AR**: Equirectangular format, Meta Quest 3, Apple Vision Pro compatible

---

## 📋 Table of Contents

- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [Usage](#-usage)
- [Configuration](#-configuration)
- [Development](#-development)
- [Testing](#-testing)
- [Project Structure](#-project-structure)
- [API Documentation](#-api-documentation)
- [Deployment](#-deployment)
- [Contributing](#-contributing)
- [License](#-license)
- [Acknowledgements](#-acknowledgements)

---

## 🚀 Installation

### Prerequisites

- **Python**: 3.10 or higher
- **GPU**: CUDA-compatible GPU recommended (optional, will use CPU as fallback)
- **IBM Cloud Account**: For WatsonX.ai access
- **API Credentials**: WatsonX.ai API key and Project ID

### Method 1: Using uv (Recommended)

[uv](https://github.com/astral-sh/uv) is a fast Python package installer and resolver.

```bash
# Install uv if not already installed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone the repository
git clone https://github.com/ruslanmv/GenAI-3D-Virtual-Reality-Augmented.git
cd GenAI-3D-Virtual-Reality-Augmented

# Install dependencies
make install

# Or install with development dependencies
make install-dev
```

### Method 2: Using pip

```bash
# Clone the repository
git clone https://github.com/ruslanmv/GenAI-3D-Virtual-Reality-Augmented.git
cd GenAI-3D-Virtual-Reality-Augmented

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install package
pip install -e .

# Or install with development dependencies
pip install -e ".[dev,test,docs]"
```

### Configuration

1. **Create environment file**:
   ```bash
   make env-create
   # Or manually: cp .env.example .env
   ```

2. **Edit `.env` file** with your credentials:
   ```bash
   API_KEY=your_ibm_cloud_api_key
   PROJECT_ID=your_watsonx_project_id
   ```

3. **Verify configuration**:
   ```bash
   make env-check
   ```

---

## ⚡ Quick Start

### Run the Web Application

```bash
# Start the Gradio web interface
make run

# Or directly with Python
python -m genai_3d_vr_ar.app
```

The application will be available at `http://localhost:7860`

### Generate from Command Line

```bash
# Run the CLI environment generator
make run-env-gen

# Or directly
python -m genai_3d_vr_ar.generate_environment
```

### Generate Your First 360° Image

1. Open the web interface at `http://localhost:7860`
2. Enter a prompt: *"a tropical beach at sunset with palm trees"*
3. Select enrichment type: **Standard**
4. Click **"Generate 360° Image"**
5. Wait for the AI to generate your immersive scene!

---

## 📖 Usage

### Web Interface

The Gradio web interface provides an intuitive way to generate 360° images:

1. **Scene Description**: Enter your desired environment
2. **Enrichment Type**: Choose how detailed the enrichment should be
   - **Standard**: Balanced detail and generation time
   - **Detailed**: More comprehensive descriptions
   - **Cinematic**: Hollywood-style scene descriptions
3. **Advanced Settings**: Fine-tune generation parameters
   - **Inference Steps**: Higher = better quality (20-100)
   - **Guidance Scale**: How closely to follow prompt (1.0-15.0)

### Python API

```python
from genai_3d_vr_ar import generate_environment
from genai_3d_vr_ar.app import generate_360_image

# Generate enriched prompt
enriched = generate_environment("a mystical forest with glowing mushrooms")
print(enriched)

# Generate 360° image
image, status = generate_360_image(
    prompt="a cyberpunk city at night",
    enrichment_type="Detailed",
    num_inference_steps=75,
    guidance_scale=8.0
)

# Save the image
if image:
    image.save("cyberpunk_city_360.png")
```

### Command Line Interface

```bash
# Generate enriched description
python -m genai_3d_vr_ar.generate_environment
# Follow the interactive prompt

# Or use as part of a script
echo "a futuristic space station" | python -m genai_3d_vr_ar.generate_environment
```

---

## ⚙️ Configuration

### Environment Variables

All configuration is managed through environment variables. See `.env.example` for a complete list.

#### Required

- `API_KEY`: IBM Cloud API key
- `PROJECT_ID`: WatsonX.ai project ID

#### Optional

**WatsonX.ai**:
- `WATSONX_URL`: Service endpoint (default: us-south)
- `WATSONX_MODEL_TYPE`: LLM model to use
- `WATSONX_MAX_TOKENS`: Maximum generation length (default: 250)
- `WATSONX_TEMPERATURE`: Sampling temperature (default: 0.7)

**Stable Diffusion**:
- `SD_MODEL_ID`: Base model (default: sd-v1-5)
- `SD_USE_LORA`: Enable LoRA (default: true)
- `SD_NUM_INFERENCE_STEPS`: Denoising steps (default: 50)
- `SD_DEVICE`: Computation device (cuda/cpu/mps)

### Advanced Configuration

Edit `genai_3d_vr_ar/config.py` to customize:
- Model parameters
- Default values
- Validation rules
- Logging configuration

---

## 🛠️ Development

### Available Commands

View all available commands:

```bash
make help
```

### Code Quality

```bash
# Format code
make format

# Run linter
make lint

# Type checking
make type-check

# Run all checks
make check
```

### Pre-commit Hooks

```bash
# Install pre-commit hooks
make pre-commit

# Run on all files
make pre-commit-run
```

### Clean Up

```bash
# Remove Python artifacts
make clean-pyc

# Remove build artifacts
make clean-build

# Remove test artifacts
make clean-test

# Clean everything
make clean
```

---

## 🧪 Testing

### Run Tests

```bash
# Run all tests
make test

# Run with coverage
make test-cov

# Run only unit tests
make test-unit

# Run only integration tests
make test-integration

# Verbose output
make test-verbose
```

### Test Coverage

Test coverage reports are generated in `htmlcov/index.html` after running:

```bash
make test-cov
```

### Writing Tests

Tests are located in the `tests/` directory:

- `tests/test_config.py`: Configuration tests
- `tests/test_generate_environment.py`: WatsonX.ai integration tests
- `tests/test_app.py`: Image generation tests

Example test:

```python
import pytest
from genai_3d_vr_ar import generate_environment

@pytest.mark.unit
def test_generate_environment():
    result = generate_environment("test prompt")
    assert isinstance(result, str)
    assert len(result) > 0
```

---

## 📁 Project Structure

```
GenAI-3D-Virtual-Reality-Augmented/
│
├── genai_3d_vr_ar/          # Main package
│   ├── __init__.py          # Package initialization
│   ├── app.py               # Gradio web application
│   ├── generate_environment.py  # WatsonX.ai integration
│   └── config.py            # Configuration management
│
├── tests/                   # Test suite
│   ├── __init__.py
│   ├── conftest.py          # Pytest fixtures
│   ├── test_config.py
│   ├── test_generate_environment.py
│   └── test_app.py
│
├── 3D/                      # 360° generation documentation
│   └── README.md
│
├── NPC/                     # Unreal Engine NPC guides
│   └── README.md
│
├── .env.example             # Environment template
├── .gitignore              # Git ignore rules
├── LICENSE                 # Apache 2.0 license
├── Makefile                # Development automation
├── pyproject.toml          # Project configuration
├── README.md               # This file
└── setup.md                # Detailed setup guide
```

---

## 📚 API Documentation

### Core Modules

#### `genai_3d_vr_ar.generate_environment`

Generate enriched environment descriptions using WatsonX.ai.

**Functions**:

- `generate_environment(prompt: str) -> str`
  - Enriches a text prompt with detailed descriptions
  - Parameters:
    - `prompt`: User-provided scene description
  - Returns: Enriched, detailed description
  - Raises: `WatsonXModelError`, `ConfigurationError`

- `get_model(...) -> Model`
  - Creates a configured WatsonX.ai model instance
  - Returns: IBM Watson ML Model object

#### `genai_3d_vr_ar.app`

Generate 360° images using Stable Diffusion.

**Functions**:

- `generate_360_image(prompt, enrichment_type, ...) -> Tuple[Image, str]`
  - Generates a 360° equirectangular image
  - Parameters:
    - `prompt`: Scene description
    - `enrichment_type`: Standard/Detailed/Cinematic
    - `num_inference_steps`: Denoising steps (optional)
    - `guidance_scale`: CFG scale (optional)
  - Returns: (PIL Image, status message)

- `get_pipeline() -> StableDiffusionPipeline`
  - Initializes the Stable Diffusion pipeline
  - Returns: Configured pipeline instance

#### `genai_3d_vr_ar.config`

Configuration management and validation.

**Classes**:

- `WatsonXConfig`: WatsonX.ai configuration dataclass
- `StableDiffusionConfig`: Stable Diffusion configuration
- `ApplicationConfig`: Complete application config

**Functions**:

- `get_config() -> ApplicationConfig`
  - Load and validate configuration
  - Returns: Complete validated configuration

---

## 🚢 Deployment

### Local Deployment

```bash
# Run the application
make run

# Access at http://localhost:7860
```

### Docker Deployment (Coming Soon)

```bash
# Build Docker image
make docker-build

# Run container
make docker-run
```

### AWS SageMaker Deployment

See `setup.md` for detailed AWS SageMaker deployment instructions.

### Production Considerations

1. **Environment Variables**: Use secrets management (AWS Secrets Manager, etc.)
2. **GPU Resources**: Ensure CUDA-compatible GPU for optimal performance
3. **Model Caching**: Pre-download models to avoid startup delays
4. **Logging**: Configure centralized logging (CloudWatch, etc.)
5. **Monitoring**: Set up health checks and performance monitoring
6. **Scaling**: Use load balancers for multiple instances

---

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:

### Development Setup

```bash
# Fork and clone the repository
git clone https://github.com/YOUR_USERNAME/GenAI-3D-Virtual-Reality-Augmented.git
cd GenAI-3D-Virtual-Reality-Augmented

# Install development dependencies
make install-dev

# Install pre-commit hooks
make pre-commit
```

### Contribution Workflow

1. **Create a Branch**: `git checkout -b feature/your-feature-name`
2. **Make Changes**: Implement your feature or bug fix
3. **Write Tests**: Add tests for your changes
4. **Run Tests**: `make test` - ensure all tests pass
5. **Format Code**: `make format` - format your code
6. **Run Checks**: `make check` - ensure code quality
7. **Commit**: `git commit -m "feat: add your feature"`
8. **Push**: `git push origin feature/your-feature-name`
9. **Pull Request**: Open a PR with a clear description

### Commit Message Convention

Follow [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `test:` Test additions or changes
- `refactor:` Code refactoring
- `chore:` Maintenance tasks

### Code Style

- Follow PEP 8
- Use type hints
- Write comprehensive docstrings
- Maintain test coverage above 80%

---

## 📄 License

This project is licensed under the **Apache License 2.0** - see the [LICENSE](LICENSE) file for details.

```
Copyright 2024 Ruslan Magana

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```

---

## 🙏 Acknowledgements

This project builds upon the amazing work of:

- **IBM WatsonX.ai**: For providing state-of-the-art LLM capabilities
- **Stability AI**: For the Stable Diffusion models
- **Hugging Face**: For the Transformers and Diffusers libraries
- **Gradio**: For the excellent web framework
- **ProGamerGov**: For the 360-Diffusion-LoRA fine-tuned model
- **Astral**: For the incredible uv package manager

Special thanks to the open-source community for continuous innovation in AI/ML.

---

## 📞 Support & Contact

- **Website**: [ruslanmv.com](https://ruslanmv.com)
- **Issues**: [GitHub Issues](https://github.com/ruslanmv/GenAI-3D-Virtual-Reality-Augmented/issues)
- **Discussions**: [GitHub Discussions](https://github.com/ruslanmv/GenAI-3D-Virtual-Reality-Augmented/discussions)

---

## 🗺️ Roadmap

- [ ] Docker containerization
- [ ] Kubernetes deployment configurations
- [ ] Real-time streaming generation
- [ ] Multi-language support
- [ ] Video generation from images
- [ ] Enhanced VR headset integrations
- [ ] Cloud deployment templates (AWS, GCP, Azure)
- [ ] RESTful API server
- [ ] Mobile app support

---

<div align="center">

**Made with ❤️ by [Ruslan Magana](https://ruslanmv.com)**

⭐ Star this repository if you find it helpful!

</div>