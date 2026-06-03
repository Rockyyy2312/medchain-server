"""
Unit tests for ingestion: transformer and chunker.
Run with: pytest tests/test_ingestion.py -v
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from ingestion.transformer import record_to_text, appointment_to_text, patient_profile_to_text
from ingestion.chunker import chunk_text, chunk_documents


# ── Transformer tests ──────────────────────────────────────────────────────────

def test_record_to_text_full():
    row = {
        "patient_email": "alice@test.com",
        "first_name": "Alice",
        "last_name": "Smith",
        "record_type": "Blood Test",
        "record_date": "2024-01-15",
        "doctor_name": "Dr. Laukik Parashare",
        "patient_id": "uuid-123",
        "id": "rec-456",
    }
    text = record_to_text(row)
    assert "Alice Smith" in text
    assert "Blood Test" in text
    assert "Dr. Laukik Parashare" in text
    assert "2024-01-15" in text


def test_appointment_to_text():
    row = {
        "patient_email": "bob@test.com",
        "first_name": "Bob",
        "last_name": "Jones",
        "doctor_name": "Dr. Harsh Shah",
        "specialty": "Cardiology",
        "appointment_date": "2024-03-10",
        "appointment_time": "10:30:00",
        "reason": "Chest pain",
        "status": "Confirmed",
        "patient_id": "uuid-789",
        "id": "apt-012",
    }
    text = appointment_to_text(row)
    assert "Bob Jones" in text
    assert "Cardiology" in text
    assert "Confirmed" in text
    assert "Chest pain" in text


def test_patient_profile_to_text_no_name():
    row = {
        "email": "anon@test.com",
        "first_name": "",
        "last_name": "",
        "date_joined": "2023-06-01",
        "id": "uuid-000",
    }
    text = patient_profile_to_text(row)
    assert "anon@test.com" in text  # Falls back to email


# ── Chunker tests ──────────────────────────────────────────────────────────────

def test_chunk_text_short():
    short = "Hello world"
    chunks = chunk_text(short)
    assert chunks == [short]


def test_chunk_text_long():
    long_text = "A" * 1000
    chunks = chunk_text(long_text)
    assert len(chunks) > 1
    for chunk in chunks:
        assert len(chunk) <= 400 + 10  # CHUNK_SIZE with a small buffer


def test_chunk_documents_preserves_metadata():
    docs = [
        {
            "text": "A" * 500,
            "patient_id": "p1",
            "source_type": "record",
            "source_id": "r1",
        }
    ]
    chunked = chunk_documents(docs)
    assert all(c["patient_id"] == "p1" for c in chunked)
    assert all(c["source_type"] == "record" for c in chunked)
    assert all("chunk_index" in c for c in chunked)
