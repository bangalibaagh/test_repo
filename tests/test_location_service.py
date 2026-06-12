"""Tests for location_service structured logging."""

import logging
from unittest.mock import MagicMock, patch

import pytest

from src.schemas.location import LocationCreate, LocationUpdate


@pytest.fixture()
def _mock_location():
    loc = MagicMock()
    loc.id = 1
    loc.name = "Test Location"
    return loc


def test_create_location_logs_string_message(caplog, _mock_location):
    """create_location must log a string message, not a dict."""
    mock_db = MagicMock()
    mock_db.refresh.side_effect = lambda obj: None

    with patch("src.services.location_service.Location", return_value=_mock_location):
        with caplog.at_level(logging.INFO, logger="src.services.location_service"):
            from src.services.location_service import create_location

            payload = LocationCreate(
                name="Test Location",
                address="123 Main St",
                latitude=0.0,
                longitude=0.0,
            )
            create_location(mock_db, payload)

    assert len(caplog.records) >= 1
    record = caplog.records[-1]
    assert isinstance(record.getMessage(), str)
    assert not record.getMessage().startswith("{")
    assert record.event == "location_created"


def test_get_location_not_found_logs_string_message(caplog):
    """get_location must log a string warning message, not a dict, when not found."""
    from fastapi import HTTPException
    from src.services.location_service import get_location

    mock_db = MagicMock()
    mock_db.query.return_value.filter.return_value.first.return_value = None

    with caplog.at_level(logging.WARNING, logger="src.services.location_service"):
        with pytest.raises(HTTPException):
            get_location(mock_db, 999)

    assert len(caplog.records) >= 1
    record = caplog.records[-1]
    assert isinstance(record.getMessage(), str)
    assert not record.getMessage().startswith("{")
    assert record.event == "location_not_found"


def test_update_location_logs_string_message(caplog, _mock_location):
    """update_location must log a string message, not a dict."""
    from src.services.location_service import update_location

    mock_db = MagicMock()

    with patch(
        "src.services.location_service.get_location", return_value=_mock_location
    ):
        with caplog.at_level(logging.INFO, logger="src.services.location_service"):
            payload = LocationUpdate(name="Updated")
            update_location(mock_db, 1, payload)

    assert len(caplog.records) >= 1
    record = caplog.records[-1]
    assert isinstance(record.getMessage(), str)
    assert not record.getMessage().startswith("{")
    assert record.event == "location_updated"


def test_delete_location_logs_string_message(caplog, _mock_location):
    """delete_location must log a string message, not a dict."""
    from src.services.location_service import delete_location

    mock_db = MagicMock()

    with patch(
        "src.services.location_service.get_location", return_value=_mock_location
    ):
        with caplog.at_level(logging.INFO, logger="src.services.location_service"):
            delete_location(mock_db, 1)

    assert len(caplog.records) >= 1
    record = caplog.records[-1]
    assert isinstance(record.getMessage(), str)
    assert not record.getMessage().startswith("{")
    assert record.event == "location_deleted"
