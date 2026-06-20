from typing import Dict, Any, List
from db.connector import (
    fetch_all_records,
    fetch_all_appointments,
    fetch_all_patients,
    fetch_all_vitals,
    fetch_all_diagnoses,
    fetch_all_prescriptions,
    fetch_all_parsed_data,
    fetch_all_access_grants,
    fetch_all_access_requests,
)
from ingestion.patient_loader import load_patient_files


def _normalize_id(val: Any) -> str:
    """Normalize UUID to lowercase string."""
    if val is None:
        return ""
    return str(val).lower().strip("{}")


def _patient_name(row: Dict[str, Any]) -> str:
    first = row.get("first_name") or ""
    last  = row.get("last_name")  or ""
    email = row.get("patient_email") or row.get("email") or "Unknown"
    name  = f"{first} {last}".strip()
    return name if name else email


def record_to_text(row: Dict[str, Any]) -> str:
    """Convert a medical record DB row into a readable text chunk."""
    name   = _patient_name(row)
    rtype  = row.get("record_type") or "General"
    date   = row.get("record_date")  or "unknown date"
    doctor = row.get("doctor_name")  or "unknown doctor"
    email  = row.get("patient_email") or ""

    return (
        f"Medical Record — Patient: {name} ({email})\n"
        f"Record Type: {rtype}\n"
        f"Date of Record: {date}\n"
        f"Treating Doctor: {doctor}\n"
        f"Patient ID: {row.get('patient_id', '')}\n"
        f"Record ID: {row.get('id', '')}\n"
    )


def appointment_to_text(row: Dict[str, Any]) -> str:
    """Convert an appointment DB row into a readable text chunk."""
    name      = _patient_name(row)
    email     = row.get("patient_email") or ""
    doctor    = row.get("doctor_name")   or "unknown doctor"
    specialty = row.get("specialty")     or "General"
    date      = row.get("appointment_date") or "unknown date"
    time      = row.get("appointment_time") or ""
    reason    = row.get("reason")           or "No reason specified"
    status    = row.get("status")           or "Unknown"

    return (
        f"Appointment — Patient: {name} ({email})\n"
        f"Doctor: {doctor} | Specialty: {specialty}\n"
        f"Date: {date} at {time}\n"
        f"Reason: {reason}\n"
        f"Status: {status}\n"
        f"Patient ID: {row.get('patient_id', '')}\n"
        f"Appointment ID: {row.get('id', '')}\n"
    )


def patient_profile_to_text(row: Dict[str, Any]) -> str:
    """Convert a patient profile row into a short identity chunk."""
    first  = row.get("first_name") or ""
    last   = row.get("last_name")  or ""
    email  = row.get("email") or ""
    joined = row.get("date_joined") or ""
    name   = f"{first} {last}".strip() or email
    return (
        f"Patient Profile — Name: {name}\n"
        f"Email: {email}\n"
        f"Joined: {joined}\n"
        f"Patient ID: {row.get('id', '')}\n"
    )


def vitals_to_text(row: Dict[str, Any]) -> str:
    """Convert a vitals DB row into a readable text chunk."""
    name = _patient_name(row)
    email = row.get("patient_email") or ""
    date = row.get("recorded_at") or "unknown date"
    
    # Format date if it contains a timestamp
    if isinstance(date, str) and " " in date:
        date = date.split(" ")[0]
        
    weight = f"{row.get('weight_kg')} kg" if row.get("weight_kg") else "N/A"
    height = f"{row.get('height_cm')} cm" if row.get("height_cm") else "N/A"
    bp = f"{row.get('blood_pressure_sys')}/{row.get('blood_pressure_dia')} mmHg" if row.get("blood_pressure_sys") and row.get("blood_pressure_dia") else "N/A"
    hr = f"{row.get('heart_rate_bpm')} bpm" if row.get("heart_rate_bpm") else "N/A"
    temp = f"{row.get('temperature_c')} °C" if row.get("temperature_c") else "N/A"
    notes = row.get("notes") or "No notes specified."

    return (
        f"Vitals Log — Patient: {name} ({email})\n"
        f"Recorded Date: {date}\n"
        f"Weight: {weight} | Height: {height}\n"
        f"Blood Pressure: {bp}\n"
        f"Heart Rate: {hr}\n"
        f"Temperature: {temp}\n"
        f"Notes: {notes}\n"
        f"Patient ID: {row.get('patient_id', '')}\n"
        f"Vitals ID: {row.get('id', '')}\n"
    )


def diagnosis_to_text(row: Dict[str, Any]) -> str:
    """Convert a diagnosis DB row into a readable text chunk."""
    name = _patient_name(row)
    email = row.get("patient_email") or ""
    condition = row.get("condition_name") or "Unknown Condition"
    icd = row.get("icd_code") or "N/A"
    date = row.get("diagnosed_date") or "unknown date"
    status = row.get("status") or "Active"
    severity = row.get("severity") or "Moderate"
    notes = row.get("notes") or "No notes specified."

    return (
        f"Diagnosis Record — Patient: {name} ({email})\n"
        f"Diagnosed Condition: {condition}\n"
        f"ICD-10 Code: {icd}\n"
        f"Diagnosed Date: {date}\n"
        f"Status: {status} | Severity: {severity}\n"
        f"Notes: {notes}\n"
        f"Patient ID: {row.get('patient_id', '')}\n"
        f"Diagnosis ID: {row.get('id', '')}\n"
    )


def prescription_to_text(row: Dict[str, Any]) -> str:
    """Convert a prescription DB row into a readable text chunk."""
    name = _patient_name(row)
    email = row.get("patient_email") or ""
    med = row.get("medication_name") or "Unknown Medication"
    dose = row.get("dosage") or "N/A"
    freq = row.get("frequency") or "N/A"
    start = row.get("start_date") or "N/A"
    end = row.get("end_date") or "Ongoing"
    refills = row.get("refills_remaining") or 0
    inst = row.get("instructions") or "Take as directed."

    return (
        f"Prescription Record — Patient: {name} ({email})\n"
        f"Medication: {med}\n"
        f"Dosage: {dose} | Frequency: {freq}\n"
        f"Active Period: {start} to {end}\n"
        f"Refills Remaining: {refills}\n"
        f"Instructions: {inst}\n"
        f"Patient ID: {row.get('patient_id', '')}\n"
        f"Prescription ID: {row.get('id', '')}\n"
    )


def parsed_data_to_text(row: Dict[str, Any]) -> str:
    """Convert a parsed medical document key-value pair into a readable text chunk."""
    first = row.get("patient_first_name") or ""
    last = row.get("patient_last_name") or ""
    name = f"{first} {last}".strip() or row.get("patient_email") or "Unknown"
    email = row.get("patient_email") or ""
    
    key = row.get("key") or "N/A"
    value = row.get("value") or "N/A"
    extracted = row.get("extracted_at") or "unknown date"

    return (
        f"Parsed Document Data — Patient: {name} ({email})\n"
        f"Key: {key}\n"
        f"Value: {value}\n"
        f"Extracted Date: {extracted}\n"
        f"Associated Record ID: {row.get('record_id', '')}\n"
        f"Patient ID: {row.get('patient_id', '')}\n"
        f"Parsed Data ID: {row.get('id', '')}\n"
    )


def access_grant_to_text(row: Dict[str, Any]) -> str:
    """Convert an access grant into a readable text chunk."""
    pat_first = row.get("patient_first_name") or ""
    pat_last = row.get("patient_last_name") or ""
    pat_name = f"{pat_first} {pat_last}".strip() or row.get("patient_email") or "Unknown"
    pat_email = row.get("patient_email") or ""
    
    doc_first = row.get("doctor_first_name") or ""
    doc_last = row.get("doctor_last_name") or ""
    doc_name = f"{doc_first} {doc_last}".strip() or row.get("doctor_email") or "Unknown"
    doc_email = row.get("doctor_email") or ""
    
    created = row.get("created_at") or "unknown date"

    return (
        f"Access Grant Details — Patient: {pat_name} ({pat_email})\n"
        f"Granted To Doctor: {doc_name} ({doc_email})\n"
        f"Doctor ID: {row.get('doctor_id', '')}\n"
        f"Granted Date: {created}\n"
        f"Patient ID: {row.get('patient_id', '')}\n"
        f"Grant ID: {row.get('id', '')}\n"
    )


def access_request_to_text(row: Dict[str, Any]) -> str:
    """Convert an access request into a readable text chunk."""
    pat_first = row.get("patient_first_name") or ""
    pat_last = row.get("patient_last_name") or ""
    pat_name = f"{pat_first} {pat_last}".strip() or row.get("patient_email") or "Unknown"
    pat_email = row.get("patient_email") or ""
    
    doc_first = row.get("doctor_first_name") or ""
    doc_last = row.get("doctor_last_name") or ""
    doc_name = f"{doc_first} {doc_last}".strip() or row.get("doctor_email") or "Unknown"
    doc_email = row.get("doctor_email") or ""
    
    reason = row.get("reason") or "No reason specified"
    status = row.get("status") or "Pending"
    created = row.get("created_at") or "unknown date"

    return (
        f"Access Request Details — Patient: {pat_name} ({pat_email})\n"
        f"Requested By Doctor: {doc_name} ({doc_email})\n"
        f"Doctor ID: {row.get('doctor_id', '')}\n"
        f"Request Status: {status}\n"
        f"Reason for Request: {reason}\n"
        f"Requested Date: {created}\n"
        f"Patient ID: {row.get('patient_id', '')}\n"
        f"Request ID: {row.get('id', '')}\n"
    )


def build_all_documents() -> List[Dict[str, Any]]:
    """
    Pull all data from DB and convert to text documents.
    Returns list of {text, patient_id, source_type, source_id}.
    """
    docs: List[Dict[str, Any]] = []

    # Patient profiles
    for p in fetch_all_patients():
        docs.append({
            "text":        patient_profile_to_text(p),
            "patient_id":  _normalize_id(p.get("id", "")),
            "source_type": "profile",
            "source_id":   _normalize_id(p.get("id", "")),
        })

    # Medical records
    for r in fetch_all_records():
        docs.append({
            "text":        record_to_text(r),
            "patient_id":  _normalize_id(r.get("patient_id", "")),
            "source_type": "record",
            "source_id":   _normalize_id(r.get("id", "")),
        })

    # Appointments
    for a in fetch_all_appointments():
        docs.append({
            "text":        appointment_to_text(a),
            "patient_id":  _normalize_id(a.get("patient_id", "")),
            "source_type": "appointment",
            "source_id":   _normalize_id(a.get("id", "")),
        })

    # Vitals
    for v in fetch_all_vitals():
        docs.append({
            "text":        vitals_to_text(v),
            "patient_id":  _normalize_id(v.get("patient_id", "")),
            "source_type": "vital",
            "source_id":   _normalize_id(v.get("id", "")),
        })

    # Diagnoses
    for d in fetch_all_diagnoses():
        docs.append({
            "text":        diagnosis_to_text(d),
            "patient_id":  _normalize_id(d.get("patient_id", "")),
            "source_type": "diagnosis",
            "source_id":   _normalize_id(d.get("id", "")),
        })

    # Prescriptions
    for pr in fetch_all_prescriptions():
        docs.append({
            "text":        prescription_to_text(pr),
            "patient_id":  _normalize_id(pr.get("patient_id", "")),
            "source_type": "prescription",
            "source_id":   _normalize_id(pr.get("id", "")),
        })

    # Parsed document key-values
    for pd in fetch_all_parsed_data():
        docs.append({
            "text":        parsed_data_to_text(pd),
            "patient_id":  _normalize_id(pd.get("patient_id", "")),
            "source_type": "parsed_data",
            "source_id":   _normalize_id(pd.get("id", "")),
        })

    # Access grants
    for g in fetch_all_access_grants():
        docs.append({
            "text":        access_grant_to_text(g),
            "patient_id":  _normalize_id(g.get("patient_id", "")),
            "source_type": "access_grant",
            "source_id":   _normalize_id(g.get("id", "")),
        })

    # Access requests
    for req in fetch_all_access_requests():
        docs.append({
            "text":        access_request_to_text(req),
            "patient_id":  _normalize_id(req.get("patient_id", "")),
            "source_type": "access_request",
            "source_id":   _normalize_id(req.get("id", "")),
        })

    # Patient intelligence JSON files
    intel_docs = load_patient_files()
    docs.extend(intel_docs)

    return docs

