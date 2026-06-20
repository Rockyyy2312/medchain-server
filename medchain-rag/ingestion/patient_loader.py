"""
Patient Intelligence Loader
============================
Reads structured patient JSON files from data/patients/ and converts
each section into text documents suitable for the RAG ingestion pipeline.

Each document follows the existing schema:
    {text, patient_id, source_type, source_id}
"""

import json
import logging
from pathlib import Path
from typing import Dict, Any, List

from config import BASE_DIR

logger = logging.getLogger(__name__)

PATIENTS_DIR = BASE_DIR / "data" / "patients"


# ── Section → Text converters ─────────────────────────────────────────────────

def _demographics_to_text(patient: Dict[str, Any]) -> str:
    d = patient.get("demographics", {})
    lifestyle = patient.get("lifestyle", {})
    return (
        f"Patient Intelligence Profile — {d.get('full_name', 'Unknown')}\n"
        f"Patient ID: {patient.get('patient_id', '')}\n"
        f"Age: {d.get('age', 'N/A')} | Gender: {d.get('gender', 'N/A')} | Blood Group: {d.get('blood_group', 'N/A')}\n"
        f"Date of Birth: {d.get('date_of_birth', 'N/A')}\n"
        f"Occupation: {d.get('occupation', 'N/A')}\n"
        f"Marital Status: {d.get('marital_status', 'N/A')}\n"
        f"City: {d.get('address', {}).get('city', 'N/A')}, "
        f"{d.get('address', {}).get('state', '')}, "
        f"{d.get('address', {}).get('country', '')}\n"
        f"Smoking: {lifestyle.get('smoking', {}).get('status', 'N/A')} — "
        f"{lifestyle.get('smoking', {}).get('details', '')}\n"
        f"Alcohol: {lifestyle.get('alcohol', {}).get('status', 'N/A')} — "
        f"{lifestyle.get('alcohol', {}).get('details', '')}\n"
        f"Diet: {lifestyle.get('diet', {}).get('type', 'N/A')} — "
        f"{lifestyle.get('diet', {}).get('details', '')}\n"
        f"Exercise: {lifestyle.get('exercise', {}).get('status', 'N/A')} — "
        f"{lifestyle.get('exercise', {}).get('details', '')}\n"
        f"Sleep: {lifestyle.get('sleep', {}).get('average_hours', 'N/A')} hours/night — "
        f"{lifestyle.get('sleep', {}).get('quality', '')}\n"
        f"Stress Level: {lifestyle.get('stress_level', 'N/A')}\n"
    )


def _allergies_to_text(patient: Dict[str, Any]) -> str:
    allergies = patient.get("allergies", [])
    if not allergies:
        return ""
    pid = patient.get("patient_id", "")
    name = patient.get("demographics", {}).get("full_name", "Unknown")
    lines = [f"Allergies — Patient: {name} (ID: {pid})\n"]
    for a in allergies:
        lines.append(
            f"  • {a.get('allergen', 'Unknown')}: {a.get('reaction', 'N/A')} | "
            f"Severity: {a.get('severity', 'N/A')} | Status: {a.get('status', 'N/A')} | "
            f"Diagnosed: {a.get('diagnosed_date', 'N/A')}\n"
        )
    return "".join(lines)


def _family_history_to_text(patient: Dict[str, Any]) -> str:
    fh = patient.get("family_history", [])
    if not fh:
        return ""
    pid = patient.get("patient_id", "")
    name = patient.get("demographics", {}).get("full_name", "Unknown")
    lines = [f"Family Medical History — Patient: {name} (ID: {pid})\n"]
    for f in fh:
        lines.append(
            f"  • {f.get('relation', 'Unknown')}: {f.get('condition', 'N/A')} | "
            f"Diagnosed at age {f.get('age_at_diagnosis', 'N/A')} | "
            f"Status: {f.get('current_status', 'N/A')}\n"
            f"    Notes: {f.get('notes', '')}\n"
        )
    return "".join(lines)


def _chronic_conditions_to_text(patient: Dict[str, Any]) -> str:
    conditions = patient.get("chronic_conditions", [])
    if not conditions:
        return ""
    pid = patient.get("patient_id", "")
    name = patient.get("demographics", {}).get("full_name", "Unknown")
    lines = [f"Chronic Conditions — Patient: {name} (ID: {pid})\n"]
    for c in conditions:
        lines.append(
            f"  • {c.get('condition', 'Unknown')} (ICD: {c.get('icd_code', 'N/A')})\n"
            f"    Diagnosed: {c.get('diagnosed_date', 'N/A')} (age {c.get('diagnosed_age', 'N/A')})\n"
            f"    Status: {c.get('status', 'N/A')} | Severity: {c.get('severity', 'N/A')}\n"
            f"    Doctor: {c.get('managing_doctor', 'N/A')} ({c.get('specialty', '')})\n"
            f"    Notes: {c.get('notes', '')}\n"
        )
    return "".join(lines)


def _timeline_to_text(patient: Dict[str, Any]) -> str:
    """Convert the full medical timeline into a single rich text document."""
    timeline = patient.get("medical_history_timeline", [])
    if not timeline:
        return ""
    pid = patient.get("patient_id", "")
    name = patient.get("demographics", {}).get("full_name", "Unknown")
    lines = [f"Complete Medical History Timeline — Patient: {name} (ID: {pid})\n\n"]
    for year_entry in timeline:
        year = year_entry.get("year", "")
        age = year_entry.get("age", "")
        lines.append(f"--- Year {year} (Age {age}) ---\n")
        for ev in year_entry.get("events", []):
            lines.append(
                f"  [{ev.get('category', 'General')}] {ev.get('event', 'N/A')}\n"
                f"    {ev.get('details', '')}\n"
            )
        lines.append("\n")
    return "".join(lines)


def _report_to_text(report: Dict[str, Any], patient: Dict[str, Any]) -> str:
    """Convert a single medical report into a text document."""
    pid = patient.get("patient_id", "")
    name = patient.get("demographics", {}).get("full_name", "Unknown")

    findings_lines = []
    findings = report.get("detailed_findings", {})
    for key, val in findings.items():
        if isinstance(val, dict):
            value = val.get("value", val.get("latency", val.get("systolic", "")))
            unit = val.get("unit", "")
            status = val.get("status", "")
            ref = val.get("reference_range", "")
            findings_lines.append(
                f"    {key}: {value} {unit} (Ref: {ref}) — {status}"
            )
        else:
            findings_lines.append(f"    {key}: {val}")
    findings_text = "\n".join(findings_lines) if findings_lines else "    No detailed findings recorded."

    return (
        f"Medical Report — Patient: {name} (ID: {pid})\n"
        f"Report ID: {report.get('report_id', 'N/A')}\n"
        f"Date: {report.get('date', 'N/A')}\n"
        f"Type: {report.get('type', 'N/A')}\n"
        f"Category: {report.get('category', 'N/A')}\n"
        f"Facility: {report.get('facility', 'N/A')}\n"
        f"Ordering Doctor: {report.get('ordering_doctor', 'N/A')}\n"
        f"Specialist: {report.get('specialist', 'N/A')}\n"
        f"Detailed Findings:\n{findings_text}\n"
        f"Doctor Notes: {report.get('doctor_notes', 'N/A')}\n"
        f"Severity Level: {report.get('severity_level', 'N/A')}\n"
        f"Recommended Action: {report.get('recommended_action', 'N/A')}\n"
    )


def _diagnoses_to_text(patient: Dict[str, Any]) -> str:
    diagnoses = patient.get("diagnoses", {})
    pid = patient.get("patient_id", "")
    name = patient.get("demographics", {}).get("full_name", "Unknown")
    lines = [f"Diagnoses Summary — Patient: {name} (ID: {pid})\n\nPrimary Diagnoses:\n"]
    for d in diagnoses.get("primary", []):
        lines.append(
            f"  • {d.get('condition', 'Unknown')} (ICD: {d.get('icd_code', 'N/A')})\n"
            f"    Diagnosed: {d.get('diagnosed_date', 'N/A')} | Status: {d.get('status', 'N/A')}\n"
            f"    Severity: {d.get('severity', 'N/A')} | Doctor: {d.get('managing_doctor', 'N/A')}\n"
            f"    Notes: {d.get('notes', '')}\n"
        )
    lines.append("\nSecondary Diagnoses:\n")
    for d in diagnoses.get("secondary", []):
        lines.append(
            f"  • {d.get('condition', 'Unknown')} (ICD: {d.get('icd_code', 'N/A')})\n"
            f"    Diagnosed: {d.get('diagnosed_date', 'N/A')} | Status: {d.get('status', 'N/A')}\n"
            f"    Notes: {d.get('notes', '')}\n"
        )
    return "".join(lines)


def _medications_to_text(patient: Dict[str, Any]) -> str:
    meds = patient.get("medications", {})
    pid = patient.get("patient_id", "")
    name = patient.get("demographics", {}).get("full_name", "Unknown")
    lines = [f"Medications — Patient: {name} (ID: {pid})\n\nCurrent Medications:\n"]
    for m in meds.get("current", []):
        lines.append(
            f"  • {m.get('medication_name', 'Unknown')} ({m.get('generic_name', '')})\n"
            f"    Dosage: {m.get('dosage', 'N/A')} | Frequency: {m.get('frequency', 'N/A')}\n"
            f"    Route: {m.get('route', 'N/A')} | Started: {m.get('start_date', 'N/A')}\n"
            f"    Indication: {m.get('indication', 'N/A')}\n"
            f"    Prescribing Doctor: {m.get('prescribing_doctor', 'N/A')}\n"
            f"    Notes: {m.get('notes', '')}\n"
        )
    lines.append("\nPast Medications:\n")
    for m in meds.get("past", []):
        lines.append(
            f"  • {m.get('medication_name', 'Unknown')} — {m.get('dosage', 'N/A')}\n"
            f"    Period: {m.get('start_date', 'N/A')} to {m.get('end_date', 'N/A')}\n"
            f"    Indication: {m.get('indication', 'N/A')}\n"
            f"    Notes: {m.get('notes', '')}\n"
        )
    return "".join(lines)


def _risk_factors_to_text(patient: Dict[str, Any]) -> str:
    risks = patient.get("risk_factors", {})
    pid = patient.get("patient_id", "")
    name = patient.get("demographics", {}).get("full_name", "Unknown")
    lines = [f"Risk Factors — Patient: {name} (ID: {pid})\n"]
    for category, factors in risks.items():
        lines.append(f"\n{category.replace('_', ' ').title()} Risk Factors:\n")
        for r in factors:
            lines.append(
                f"  • {r.get('factor', 'Unknown')} — Risk Level: {r.get('risk_level', 'N/A')}\n"
                f"    {r.get('details', '')}\n"
                f"    Modifiable: {'Yes' if r.get('modifiable') else 'No'}\n"
            )
    return "".join(lines)


def _symptoms_to_text(patient: Dict[str, Any]) -> str:
    symptoms = patient.get("symptoms_history", [])
    if not symptoms:
        return ""
    pid = patient.get("patient_id", "")
    name = patient.get("demographics", {}).get("full_name", "Unknown")
    lines = [f"Symptoms History — Patient: {name} (ID: {pid})\n"]
    for s in symptoms:
        lines.append(
            f"  • {s.get('symptom', 'Unknown')}\n"
            f"    First Reported: {s.get('first_reported', 'N/A')} | "
            f"Frequency: {s.get('frequency', 'N/A')} | Severity: {s.get('severity', 'N/A')}\n"
            f"    Status: {s.get('status', 'N/A')}\n"
            f"    Related Condition: {s.get('related_condition', 'N/A')}\n"
            f"    Notes: {s.get('notes', '')}\n"
        )
    return "".join(lines)


def _hospital_visits_to_text(patient: Dict[str, Any]) -> str:
    visits = patient.get("hospital_visits", [])
    if not visits:
        return ""
    pid = patient.get("patient_id", "")
    name = patient.get("demographics", {}).get("full_name", "Unknown")
    lines = [f"Hospital Visits — Patient: {name} (ID: {pid})\n"]
    for v in visits:
        lines.append(
            f"  • {v.get('date', 'N/A')} — {v.get('type', 'N/A')}\n"
            f"    Facility: {v.get('facility', 'N/A')}\n"
            f"    Reason: {v.get('reason', 'N/A')}\n"
            f"    Doctor: {v.get('doctor', 'N/A')}\n"
            f"    Outcome: {v.get('outcome', 'N/A')}\n"
            f"    Duration: {v.get('duration', 'N/A')}\n"
        )
    return "".join(lines)


def _preventive_care_to_text(patient: Dict[str, Any]) -> str:
    care = patient.get("preventive_care", [])
    if not care:
        return ""
    pid = patient.get("patient_id", "")
    name = patient.get("demographics", {}).get("full_name", "Unknown")
    lines = [f"Preventive Care — Patient: {name} (ID: {pid})\n"]
    for c in care:
        lines.append(
            f"  • {c.get('action', 'Unknown')}\n"
            f"    Frequency: {c.get('frequency', 'N/A')} | Status: {c.get('status', 'N/A')}\n"
            f"    Last Done: {c.get('last_done', 'N/A')} | Next Due: {c.get('next_due', 'N/A')}\n"
            f"    Notes: {c.get('notes', '')}\n"
        )
    return "".join(lines)


def _summary_insights_to_text(patient: Dict[str, Any]) -> str:
    si = patient.get("summary_insights", {})
    if not si:
        return ""
    pid = patient.get("patient_id", "")
    name = patient.get("demographics", {}).get("full_name", "Unknown")

    risks = "\n".join(f"  • {r}" for r in si.get("key_risks", []))
    future = []
    for fr in si.get("predicted_future_risks", []):
        if isinstance(fr, dict):
            future.append(
                f"  • {fr.get('risk', 'N/A')} — Probability: {fr.get('probability', 'N/A')}\n"
                f"    Mitigation: {fr.get('mitigation', 'N/A')}"
            )
        else:
            future.append(f"  • {fr}")
    future_text = "\n".join(future)

    return (
        f"Summary Insights — Patient: {name} (ID: {pid})\n\n"
        f"Overall Health Status:\n{si.get('overall_health_status', 'N/A')}\n\n"
        f"Key Risks:\n{risks}\n\n"
        f"Progression Pattern:\n{si.get('progression_pattern', 'N/A')}\n\n"
        f"Predicted Future Risks:\n{future_text}\n"
    )


# ── Main loader ────────────────────────────────────────────────────────────────

def _build_docs_from_patient(patient: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Convert a single patient JSON into a list of text documents for indexing."""
    pid = patient.get("patient_id", "unknown")
    docs: List[Dict[str, Any]] = []

    def _add(text: str, source_type: str, source_id: str):
        if text and text.strip():
            docs.append({
                "text": text,
                "patient_id": pid,
                "source_type": source_type,
                "source_id": source_id,
            })

    # Demographics + Lifestyle
    _add(_demographics_to_text(patient), "intel_profile", f"{pid}_profile")

    # Allergies
    _add(_allergies_to_text(patient), "intel_allergy", f"{pid}_allergies")

    # Family History
    _add(_family_history_to_text(patient), "intel_family_history", f"{pid}_family_history")

    # Chronic Conditions
    _add(_chronic_conditions_to_text(patient), "intel_chronic_condition", f"{pid}_chronic_conditions")

    # Medical History Timeline
    _add(_timeline_to_text(patient), "intel_timeline", f"{pid}_timeline")

    # Individual Medical Reports
    for report in patient.get("medical_reports", []):
        rid = report.get("report_id", "unknown")
        _add(_report_to_text(report, patient), "intel_report", rid)

    # Diagnoses
    _add(_diagnoses_to_text(patient), "intel_diagnosis", f"{pid}_diagnoses")

    # Medications
    _add(_medications_to_text(patient), "intel_medication", f"{pid}_medications")

    # Risk Factors
    _add(_risk_factors_to_text(patient), "intel_risk_factor", f"{pid}_risk_factors")

    # Symptoms History
    _add(_symptoms_to_text(patient), "intel_symptom", f"{pid}_symptoms")

    # Hospital Visits
    _add(_hospital_visits_to_text(patient), "intel_hospital_visit", f"{pid}_hospital_visits")

    # Preventive Care
    _add(_preventive_care_to_text(patient), "intel_preventive_care", f"{pid}_preventive_care")

    # Summary Insights
    _add(_summary_insights_to_text(patient), "intel_summary", f"{pid}_summary_insights")

    return docs


def load_patient_files() -> List[Dict[str, Any]]:
    """
    Read all patient_*.json files from data/patients/ and convert
    them into text documents for the RAG index.

    Returns list of {text, patient_id, source_type, source_id}.
    """
    if not PATIENTS_DIR.exists():
        logger.warning(f"Patients directory not found: {PATIENTS_DIR}")
        return []

    all_docs: List[Dict[str, Any]] = []
    for json_file in sorted(PATIENTS_DIR.glob("patient_*.json")):
        try:
            with open(json_file, "r", encoding="utf-8") as f:
                patient = json.load(f)
            docs = _build_docs_from_patient(patient)
            logger.info(f"Loaded {len(docs)} documents from {json_file.name}")
            all_docs.extend(docs)
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in {json_file}: {e}")
        except Exception as e:
            logger.error(f"Error loading {json_file}: {e}")

    logger.info(f"Total patient intelligence documents loaded: {len(all_docs)}")
    return all_docs
