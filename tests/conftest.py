"""Pytest configuration and shared fixtures.

Author: Ruslan Magana
Website: ruslanmv.com
"""

import os
from pathlib import Path
from typing import Generator

import pytest


@pytest.fixture(scope="session")
def test_env() -> Generator[None, None, None]:
    """Set up test environment variables.

    This fixture sets up mock environment variables for testing
    and cleans them up after tests complete.
    """
    # Save original environment
    original_env = {
        "API_KEY": os.environ.get("API_KEY"),
        "PROJECT_ID": os.environ.get("PROJECT_ID"),
    }

    # Set test environment variables
    os.environ["API_KEY"] = "test_api_key_12345"
    os.environ["PROJECT_ID"] = "test_project_id_67890"

    yield

    # Restore original environment
    for key, value in original_env.items():
        if value is None:
            os.environ.pop(key, None)
        else:
            os.environ[key] = value


@pytest.fixture
def sample_prompt() -> str:
    """Provide a sample prompt for testing.

    Returns:
        str: Sample environment description prompt
    """
    return "a tropical beach at sunset with palm trees"


@pytest.fixture
def mock_watsonx_response() -> dict:
    """Provide a mock WatsonX.ai API response.

    Returns:
        dict: Mock API response structure
    """
    return {
        "results": [
            {
                "generated_text": (
                    "A stunning tropical beach scene unfolds at sunset. "
                    "Golden light bathes the white sand as palm trees sway gently "
                    "in the breeze. Crystal clear turquoise water laps at the shore. "
                    "The sky is painted in brilliant oranges, pinks, and purples."
                )
            }
        ]
    }


@pytest.fixture
def temp_env_file(tmp_path: Path) -> Generator[Path, None, None]:
    """Create a temporary .env file for testing.

    Args:
        tmp_path: Pytest temporary directory fixture

    Yields:
        Path: Path to temporary .env file
    """
    env_file = tmp_path / ".env"
    env_file.write_text(
        "API_KEY=test_api_key\n"
        "PROJECT_ID=test_project_id\n"
        "DEBUG=true\n"
    )
    yield env_file
    # Cleanup happens automatically with tmp_path
