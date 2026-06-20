import logging
from typing import Optional
import httpx

from config import LLM_PROVIDER, GEMINI_API_KEY, GEMINI_MODEL, OLLAMA_URL, OLLAMA_MODEL

logger = logging.getLogger(__name__)

# Unified Patient-Focused System Prompt
PATIENT_SYSTEM_PROMPT = """You are MedChain AI — a secure, empathetic patient health assistant.

Your goal is to help the patient understand their medical records and provide general health education.

Rules:
1. Address BOTH the patient's specific records (our system) AND general medical information:
   - **From Your Records (System)**: Summarize and explain any relevant information found in the provided Context. State the dates, findings, doctors, or measurements clearly.
   - **General Health Info**: Provide general educational context, definitions, symptoms, or standard management/prevention practices for the conditions/medications/topics mentioned.
2. If the provided Context does NOT contain any records relevant to the query, explicitly state: "I do not see any record of this in your MedChain files. However, generally speaking..." and then proceed to explain the general medical/health information related to their question.
3. If the query is entirely educational (e.g. "What is diabetes?"), explain the general medical concept in detail.
4. The Context may contain DETAILED PATIENT INTELLIGENCE DATA including:
   - Comprehensive medical reports with specific lab values, findings, and reference ranges
   - Risk factor assessments (cardiovascular, metabolic, lifestyle-based) with risk levels
   - Complete medication histories with dosages, frequencies, and doctor notes
   - Medical history timelines spanning multiple years with categorized events
   - Family medical history with hereditary risk patterns
   - Summary insights with overall health status, progression patterns, and predicted future risks
   - Hospital visit logs, symptom histories, and preventive care schedules
   When this intelligence data is available, use it to provide thorough, medically nuanced answers. Reference specific dates, lab values, and doctor recommendations.
5. Explanations should be simple, clear, structured, and easy for patients to read.
6. At the very end of your response, you MUST include this exact disclaimer on a new line:
   "Disclaimer: This information is for educational purposes only. Please consult a healthcare professional for clinical advice."
7. NEVER include internal database identifiers, UUIDs, or raw database keys in your response.
8. Format dates and times in a human-friendly way.
9. When comparing patients or analyzing multiple records, present findings in a structured format with clear headings.
"""

# Base prompt alias for backward compatibility/tests
SYSTEM_PROMPT = PATIENT_SYSTEM_PROMPT


def _build_prompt(context: str, query: str, mode: str = "record_grounded") -> str:
    return f"""{PATIENT_SYSTEM_PROMPT}

--- Patient Health Records Context ---
{context}
--- End of Context ---

Patient Question: {query}

Answer:"""


async def _call_gemini(prompt: str) -> str:
    if not GEMINI_API_KEY:
        return "Gemini API key is not configured. Please set GEMINI_API_KEY in the .env file."

    url = (
        f"https://generativelanguage.googleapis.com/v1beta/models/"
        f"{GEMINI_MODEL}:generateContent?key={GEMINI_API_KEY}"
    )
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": 0.2,
            "topK": 40,
            "topP": 0.95,
            "maxOutputTokens": 2048,
        },
    }
    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.post(url, json=payload)
        data = resp.json()

    try:
        return data["candidates"][0]["content"]["parts"][0]["text"].strip()
    except (KeyError, IndexError):
        logger.error(f"Gemini unexpected response: {data}")
        return "The AI model returned an unexpected response. Please try again."


async def _call_ollama(prompt: str) -> str:
    url = f"{OLLAMA_URL}/api/generate"
    payload = {
        "model":  OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False,
    }
    async with httpx.AsyncClient(timeout=60.0) as client:
        resp = await client.post(url, json=payload)
        data = resp.json()
    return data.get("response", "").strip()


def classify_query_mode(query: str) -> str:
    """Classifies query into either 'record_grounded' or 'general_medical'."""
    from llm.question_bank import QUESTIONS
    query_clean = query.strip().lower().rstrip("?")
    
    # 1. Check exact match in question bank
    for q in QUESTIONS:
        if q["question_text"].strip().lower().rstrip("?") == query_clean:
            return "record_grounded" if q["requires_records"] else "general_medical"
            
    # 2. Rule-based check for patient-specific keywords
    record_keywords = [
        "my record", "my doctor", "my diagnosis", "my prescription", "my vitals",
        "my appointment", "my bp", "my weight", "my blood pressure", "who has access",
        "my grant", "my request", "my file", "my result", "my test", "my name", "my age",
        "prescribed to me", "my active", "my list"
    ]
    if any(k in query_clean for k in record_keywords) or any(query_clean.startswith(x) for x in ["do i", "am i", "have i", "when was my", "what is my", "who is my"]):
        return "record_grounded"
        
    # Default to record_grounded unless it looks like a general concept question
    general_keywords = ["what is", "causes of", "symptoms of", "how does", "why do", "define", "explain"]
    if any(query_clean.startswith(gk) for gk in general_keywords):
        return "general_medical"
        
    return "record_grounded"


async def generate_answer(context: str, query: str) -> str:
    return await generate_patient_answer(context, query, "record_grounded")


async def generate_patient_answer(context: str, query: str, mode: str) -> str:
    """
    Build the prompt and call configured LLM.
    """
    prompt = _build_prompt(context, query, mode)
    logger.info(f"Calling LLM provider: {LLM_PROVIDER}")
    try:
        if LLM_PROVIDER == "ollama":
            return await _call_ollama(prompt)
        else:
            return await _call_gemini(prompt)
    except httpx.TimeoutException:
        logger.error("LLM request timed out")
        return "The AI service timed out. Please try again in a moment."
    except Exception as e:
        logger.error(f"LLM call failed: {e}")
        return f"An error occurred while generating the response: {str(e)}"
