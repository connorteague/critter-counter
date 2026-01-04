"""
Pytest configuration and shared fixtures.

This file provides common test fixtures and configuration for all tests.
"""

import pytest
import os
import tempfile
from datetime import datetime
from typing import Generator


@pytest.fixture
def temp_data_dir() -> Generator[str, None, None]:
    """
    Provide a temporary directory for test data files.

    This fixture creates a temporary directory that's automatically
    cleaned up after the test completes.

    Yields:
        str: Path to temporary directory
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir


@pytest.fixture
def temp_log_file(temp_data_dir: str) -> str:
    """
    Provide a temporary log file path.

    Args:
        temp_data_dir: Temporary directory fixture

    Returns:
        str: Path to temporary log file
    """
    return os.path.join(temp_data_dir, "test_events.csv")


@pytest.fixture
def temp_counts_file(temp_data_dir: str) -> str:
    """
    Provide a temporary counts persistence file path.

    Args:
        temp_data_dir: Temporary directory fixture

    Returns:
        str: Path to temporary counts file
    """
    return os.path.join(temp_data_dir, "test_counts.json")


@pytest.fixture
def sample_rfid_readings():
    """
    Provide sample RFID reading data for testing.

    Returns:
        list: List of sample RFID readings with tag IDs and RSSI values
    """
    return [
        {"id": "E200001234567890ABCDEF01", "rssi": -55.0},
        {"id": "E200009876543210FEDCBA09", "rssi": -62.0},
        {"id": "E200005555555555AAAAAAAA", "rssi": -48.0},
    ]


@pytest.fixture
def mock_rfid_scan_approaching():
    """
    Mock RFID scan data showing cattle approaching (for ENTRY).

    Returns RSSI values that increase over time (signal getting stronger).
    """
    return [
        [{"id": "E200001111111111", "rssi": -70.0}],  # Far
        [{"id": "E200001111111111", "rssi": -60.0}],  # Closer
        [{"id": "E200001111111111", "rssi": -50.0}],  # Close
    ]


@pytest.fixture
def mock_rfid_scan_departing():
    """
    Mock RFID scan data showing cattle departing (for EXIT).

    Returns RSSI values that decrease over time (signal getting weaker).
    """
    return [
        [{"id": "E200002222222222", "rssi": -50.0}],  # Close
        [{"id": "E200002222222222", "rssi": -60.0}],  # Moving away
        [{"id": "E200002222222222", "rssi": -70.0}],  # Far
    ]


@pytest.fixture
def mock_rfid_scan_multi_tag():
    """
    Mock RFID scan with multiple tags detected simultaneously.

    Simulates a group of cattle moving together.
    """
    return [
        {"id": "E200001111111111", "rssi": -55.0},
        {"id": "E200002222222222", "rssi": -58.0},
        {"id": "E200003333333333", "rssi": -52.0},
    ]


@pytest.fixture
def freeze_time(monkeypatch):
    """
    Fixture to freeze time for testing time-dependent functionality.

    Usage:
        def test_something(freeze_time):
            freeze_time(datetime(2025, 1, 1, 12, 0, 0))
            # Test code that depends on current time
    """

    def _freeze_time(frozen_datetime: datetime):
        """Set datetime.now() to return a specific time."""
        import datetime as dt

        class FrozenDatetime:
            @classmethod
            def now(cls, tz=None):
                return frozen_datetime

            @classmethod
            def today(cls):
                return frozen_datetime.date()

        monkeypatch.setattr(dt, "datetime", FrozenDatetime)

    return _freeze_time


# Test configuration
def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers",
        "hardware: marks tests that require hardware (deselect with '-m \"not hardware\"')",
    )
    config.addinivalue_line("markers", "integration: marks tests as integration tests")
