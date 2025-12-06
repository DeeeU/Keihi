"""
pytest configuration and fixtures for backend tests
"""
import pytest


@pytest.fixture
def sample_data():
    """Sample fixture for testing"""
    return {
        "name": "テストデータ",
        "value": 100,
    }
