import logging
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from api.schemas import QueryRequest, QueryResponse, ReindexResponse, HealthResponse, SourceChunk, QuestionBankResponse, CompareRequest, CompareResponse
from auth.jwt_validator import validate_token
from retrieval.retriever import retrieve, build_context
from llm.generator import generate_answer, classify_query_mode, generate_patient_answer
from ingestion.transformer import build_all_documents
from ingestion.chunker import chunk_documents
from embeddings.faiss_store import build_index, save_index, refresh_index, get_index
from config import LLM_PROVIDER, EMBEDDING_MODEL

logger = logging.getLogger(__name__)
router = APIRouter()
bearer = HTTPBearer(auto_error=False)


def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(bearer),
) -> dict:
    if not credentials:
        raise HTTPException(status_code=401, detail="Authorization header missing")
    return validate_token(credentials.credentials)


# ── /health ────────────────────────────────────────────────────────────────────

@router.get("/health", response_model=HealthResponse, tags=["System"])
async def health_check():
    """Health check — returns index status and system config."""
    try:
        index, _ = get_index()
        index_loaded  = True
        total_vectors = index.ntotal
    except FileNotFoundError:
        index_loaded  = False
        total_vectors = 0

    return HealthResponse(
        status="ok",
        index_loaded=index_loaded,
        total_vectors=total_vectors,
        llm_provider=LLM_PROVIDER,
        embedding_model=EMBEDDING_MODEL,
    )


# ── /reindex ───────────────────────────────────────────────────────────────────

def _do_reindex():
    """Background task: pull all DB data, chunk, embed, save FAISS index."""
    logger.info("Starting reindex …")
    docs   = build_all_documents()
    chunks = chunk_documents(docs)
    index, meta = build_index(chunks)
    save_index(index, meta)
    refresh_index(index, meta)
    logger.info(f"Reindex complete: {len(chunks)} chunks indexed.")


@router.post("/reindex", response_model=ReindexResponse, tags=["Admin"])
async def reindex(
    background_tasks: BackgroundTasks,
    user: dict = Depends(get_current_user),
):
    """
    Rebuild the FAISS index from the database.
    Runs synchronously so the caller knows when it's done.
    Doctors and admins only in production; any authenticated user here for demo.
    """
    logger.info(f"Reindex triggered by user: {user.get('email')}")
    docs   = build_all_documents()
    chunks = chunk_documents(docs)

    if not chunks:
        return ReindexResponse(
            status="warning",
            total_chunks=0,
            message="No data found in the database to index.",
        )

    index, meta = build_index(chunks)
    save_index(index, meta)
    refresh_index(index, meta)

    return ReindexResponse(
        status="success",
        total_chunks=len(chunks),
        message=f"Successfully indexed {len(chunks)} chunks from {len(docs)} documents.",
    )


# ── /query ─────────────────────────────────────────────────────────────────────

@router.post("/query", response_model=QueryResponse, tags=["RAG"])
async def query_records(
    body: QueryRequest,
    user: dict = Depends(get_current_user),
):
    """
    Main RAG endpoint.
    - Restricted to patients only. Reject doctor/admin requests with 403.
    - Standardizes patient_id scoping using patient's user_id from JWT.
    - Classifies the query: record_grounded or general_medical.
    - Fetches context from index if needed; otherwise calls general knowledge flow.
    """
    role = user.get("role", "PATIENT")
    user_id = user.get("user_id", "")

    # Reject non-patient users (e.g. Doctors) from accessing this AI endpoint
    if role != "PATIENT":
        raise HTTPException(
            status_code=403,
            detail="Access forbidden: The AI Assistant is restricted to patient accounts only."
        )

    patient_id = user_id
    logger.info(f"Query from patient {user.get('email')} | patient_id={patient_id} | q={body.query[:60]}")

    # Classify query mode
    mode = classify_query_mode(body.query)

    chunks = []
    context = ""
    
    # Try to retrieve records if available
    try:
        chunks = retrieve(body.query, patient_id=patient_id, top_k=body.top_k or 5)
        context = build_context(chunks)
    except FileNotFoundError:
        # If the FAISS index is not built yet, log a warning and proceed with empty context
        logger.warning("FAISS index not built yet. Answering from general knowledge.")
        if mode == "record_grounded":
            mode = "general_medical"
    except Exception as e:
        logger.error(f"Query retrieval error: {e}")
        if mode == "record_grounded":
            mode = "general_medical"

    try:
        answer = await generate_patient_answer(context, body.query, mode)
    except Exception as e:
        logger.error(f"LLM generation error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to generate answer: {str(e)}")

    sources = [
        SourceChunk(
            text=c.get("text", ""),
            source_type=c.get("source_type", ""),
            source_id=c.get("source_id", ""),
            patient_id=c.get("patient_id", ""),
            score=c.get("score", 0.0),
        )
        for c in chunks
    ]

    # Resolve follow-up questions
    from llm.question_bank import QUESTIONS, get_suggested_followups
    query_clean = body.query.strip().lower().rstrip("?")
    matched_id = None
    for q in QUESTIONS:
        if q["question_text"].strip().lower().rstrip("?") == query_clean:
            matched_id = q["id"]
            break
            
    if matched_id is not None:
        follow_ups = get_suggested_followups(matched_id)
    else:
        # Default follow-ups if patient enters custom free-text
        follow_ups = [
            "What diagnoses are in my records?",
            "What are my recent vitals?",
            "Show my active prescription list."
        ]

    return QueryResponse(
        answer=answer,
        sources=sources,
        query=body.query,
        answer_mode=mode,
        follow_up_questions=follow_ups
    )


@router.get("/questions", response_model=QuestionBankResponse, tags=["RAG"])
async def get_questions(user: dict = Depends(get_current_user)):
    """
    Get the list of questions organized by category for the patient.
    Restricted to patients only.
    """
    role = user.get("role", "PATIENT")
    if role != "PATIENT":
        raise HTTPException(
            status_code=403,
            detail="Access forbidden: The Question Bank is restricted to patient accounts only."
        )
    
    from llm.question_bank import get_questions_by_category
    categories_dict = get_questions_by_category()
    
    categories_list = []
    for cat_name, qs in categories_dict.items():
        categories_list.append({
            "category_name": cat_name,
            "questions": [
                {
                    "id": q["id"],
                    "question_text": q["question_text"],
                    "requires_records": q["requires_records"],
                    "category": q["category"]
                }
                for q in qs
            ]
        })
    return QuestionBankResponse(categories=categories_list)


# ── /compare ───────────────────────────────────────────────────────────────────

@router.post("/compare", response_model=CompareResponse, tags=["RAG"])
async def compare_patients(
    body: CompareRequest,
    user: dict = Depends(get_current_user),
):
    """
    Compare two patients based on their intelligence data.
    Retrieves summaries for both patients from the index and generates
    a structured comparative analysis via the LLM.
    """
    logger.info(f"Compare request: {body.patient_id_1} vs {body.patient_id_2} by {user.get('email')}")

    aspects_text = ""
    if body.aspects:
        aspects_text = f" Focus on these aspects: {', '.join(body.aspects)}."

    # Retrieve context for both patients
    try:
        chunks_1 = retrieve(f"summary insights risk factors medications", patient_id=body.patient_id_1, top_k=10)
        chunks_2 = retrieve(f"summary insights risk factors medications", patient_id=body.patient_id_2, top_k=10)
    except FileNotFoundError:
        raise HTTPException(status_code=503, detail="FAISS index not built. Call POST /reindex first.")

    context_1 = build_context(chunks_1)
    context_2 = build_context(chunks_2)

    compare_query = (
        f"Compare the following two patients comprehensively.{aspects_text}\n\n"
        f"=== PATIENT 1 ({body.patient_id_1}) ===\n{context_1}\n\n"
        f"=== PATIENT 2 ({body.patient_id_2}) ===\n{context_2}\n\n"
        f"Provide a structured comparison covering: demographics, lifestyle, chronic conditions, "
        f"risk factors, medications, report findings, prognosis, and overall health status."
    )

    try:
        comparison = await generate_patient_answer("", compare_query, "record_grounded")
    except Exception as e:
        logger.error(f"Compare LLM error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to generate comparison: {str(e)}")

    # Generate brief individual summaries
    summary_1 = f"Patient {body.patient_id_1}: {len(chunks_1)} context chunks retrieved."
    summary_2 = f"Patient {body.patient_id_2}: {len(chunks_2)} context chunks retrieved."

    return CompareResponse(
        comparison=comparison,
        patient_1_summary=summary_1,
        patient_2_summary=summary_2,
        query=f"Compare {body.patient_id_1} vs {body.patient_id_2}",
    )

