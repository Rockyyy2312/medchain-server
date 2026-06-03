"""
Unit tests for DB connector (uses the actual SQLite DB if available, falls back gracefully).
Run with: pytest tests/test_db.py -v
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import pytest
from unittest.mock import patch, MagicMock


# ── UUID normalization tests ───────────────────────────────────────────────────

def test_normalize_uuid_lowercase():
    from db.connector import _normalize_uuid
    assert _normalize_uuid("ABC-123") == "abc-123"


def test_normalize_uuid_strips_braces():
    from db.connector import _normalize_uuid
    assert _normalize_uuid("{some-uuid}") == "some-uuid"


def test_normalize_uuid_none():
    from db.connector import _normalize_uuid
    assert _normalize_uuid(None) == ""


def test_normalize_uuid_standard():
    from db.connector import _normalize_uuid
    uid = "550e8400-e29b-41d4-a716-446655440000"
    assert _normalize_uuid(uid) == uid.lower()


# ── DB fetch tests (mocked) ────────────────────────────────────────────────────

def test_fetch_all_patients_returns_list():
    """fetch_all_patients should always return a list, even on DB error."""
    from db.connector import fetch_all_patients
    # If DB doesn't exist or is empty, should return []
    with patch("db.connector._get_conn") as mock_conn:
        mock_conn.return_value.__enter__ = MagicMock()
        mock_conn.return_value.execute.side_effect = Exception("DB error")
        mock_conn.return_value.close = MagicMock()
        result = fetch_all_patients()
    assert isinstance(result, list)


def test_fetch_all_records_returns_list():
    """fetch_all_records should always return a list, even on DB error."""
    from db.connector import fetch_all_records
    with patch("db.connector._get_conn") as mock_conn:
        mock_conn.return_value.__enter__ = MagicMock()
        mock_conn.return_value.execute.side_effect = Exception("DB error")
        mock_conn.return_value.close = MagicMock()
        result = fetch_all_records()
    assert isinstance(result, list)


def test_fetch_patient_by_id_not_found():
    """fetch_patient_by_id should return empty dict if patient not found."""
    from db.connector import fetch_patient_by_id
    with patch("db.connector._get_conn") as mock_conn:
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = None
        mock_conn.return_value.execute.return_value = mock_cursor
        mock_conn.return_value.close = MagicMock()
        result = fetch_patient_by_id("non-existent-uuid")
    assert result == {}
