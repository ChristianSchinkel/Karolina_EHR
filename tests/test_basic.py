"""
Basic tests for Karolina EHR package.
"""
import pytest


def test_package_import():
    """Test that the package can be imported."""
    import karolina_ehr
    assert karolina_ehr.__version__ == "0.1.0"


def test_main_function():
    """Test that main function exists and is callable."""
    from karolina_ehr.main import main
    assert callable(main)
