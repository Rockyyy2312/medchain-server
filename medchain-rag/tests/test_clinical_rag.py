"""
Unit tests for the new clinical RAG integration (Vitals, Diagnoses, and Prescriptions).
Run with: pytest tests/test_clinical_rag.py -v
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from ingestion.transformer import vitals_to_text, diagnosis_to_text, prescription_to_text
from db.connector import fetch_all_vitals, fetch_all_diagnoses, fetch_all_prescriptions


def test_vitals_to_text():
    row = {
        "patient_email": "laukikparashare@gmail.com",
        "first_name": "Laukik",
        "last_name": "Parashar",
        "recorded_at": "2026-05-26 10:45:00",
        "weight_kg": 72.5,
        "height_cm": 175.0,
        "blood_pressure_sys": 135,
        "blood_pressure_dia": 85,
        "heart_rate_bpm": 78,
        "temperature_c": 36.8,
        "notes": "Feeling great.",
        "patient_id": "patient-uuid-123",
        "id": "vitals-uuid-456",
    }
    text = vitals_to_text(row)
    assert "Laukik Parashar" in text
    assert "72.5 kg" in text
    assert "135/85 mmHg" in text
    assert "Feeling great." in text
    assert "patient-uuid-123" in text


def test_diagnosis_to_text():
    row = {
        "patient_email": "laukikparashare@gmail.com",
        "first_name": "Laukik",
        "last_name": "Parashar",
        "condition_name": "Mild Hypertension",
        "icd_code": "I10",
        "diagnosed_date": "2026-03-24",
        "status": "Active",
        "severity": "Mild",
        "notes": "Low sodium recommended.",
        "patient_id": "patient-uuid-123",
        "id": "diag-uuid-456",
    }
    text = diagnosis_to_text(row)
    assert "Laukik Parashar" in text
    assert "Mild Hypertension" in text
    assert "ICD-10 Code: I10" in text
    assert "Status: Active | Severity: Mild" in text
    assert "Low sodium recommended." in text


def test_prescription_to_text():
    row = {
        "patient_email": "laukikparashare@gmail.com",
        "first_name": "Laukik",
        "last_name": "Parashar",
        "medication_name": "Lisinopril 10mg",
        "dosage": "10mg",
        "frequency": "Once daily",
        "start_date": "2026-03-24",
        "end_date": "2026-09-24",
        "refills_remaining": 5,
        "instructions": "Take with water.",
        "patient_id": "patient-uuid-123",
        "id": "pres-uuid-456",
    }
    text = prescription_to_text(row)
    assert "Laukik Parashar" in text
    assert "Lisinopril 10mg" in text
    assert "Dosage: 10mg | Frequency: Once daily" in text
    assert "Refills Remaining: 5" in text
    assert "Take with water." in text


def test_clinical_database_fetching():
    # Verify that database fetching functions return list types and run without syntax errors
    vitals = fetch_all_vitals()
    diagnoses = fetch_all_diagnoses()
    prescriptions = fetch_all_prescriptions()
    
    assert isinstance(vitals, list)
    assert isinstance(diagnoses, list)
    assert isinstance(prescriptions, list)
    
    # Since we successfully seeded the DB, they should all contain clinical rows!
    assert len(vitals) >= 3
    assert len(diagnoses) >= 2
    assert len(prescriptions) >= 2
