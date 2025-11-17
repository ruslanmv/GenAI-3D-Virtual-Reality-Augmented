"""GenAI 3D Virtual Reality & Augmented Reality Platform.

A production-ready platform for generating 3D VR/AR content using
IBM WatsonX.ai and Stable Diffusion technologies.

Author: Ruslan Magana
Website: ruslanmv.com
License: Apache 2.0
"""

__version__ = "1.0.0"
__author__ = "Ruslan Magana"
__email__ = "contact@ruslanmv.com"
__license__ = "Apache-2.0"

from genai_3d_vr_ar.generate_environment import (
    generate_environment,
    get_model,
)

__all__ = [
    "generate_environment",
    "get_model",
    "__version__",
    "__author__",
    "__email__",
    "__license__",
]
