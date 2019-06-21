"""
Provide configurations for tests.
"""
import pytest

from calculator.server import server


@pytest.fixture
def app():
    """
    Return fixture for server object.
    """
    return server
