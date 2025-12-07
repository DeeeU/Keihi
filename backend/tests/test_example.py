"""
Example test file for backend

This is a placeholder test to demonstrate the test setup.
Replace this with actual tests once the application code is implemented.
"""


def test_example():
    """Example test that always passes"""
    assert True


def test_basic_math():
    """Example test with basic assertion"""
    result = 1 + 1
    assert result == 2


def test_with_fixture(sample_data):
    """Example test using a fixture"""
    assert sample_data["name"] == "テストデータ"
    assert sample_data["value"] == 100
