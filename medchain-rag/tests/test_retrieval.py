"""
Retrieval unit tests — tests context builder without requiring a real FAISS index.
Run with: pytest tests/test_retrieval.py -v
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from retrieval.retriever import build_context


def test_build_context_empty():
    ctx = build_context([])
    assert "No relevant" in ctx


def test_build_context_single_chunk():
    chunks = [
        {
            "text": "Patient Alice — Blood Test on 2024-01-15",
            "source_type": "record",
            "source_id": "r1",
            "patient_id": "p1",
            "score": 0.1,
        }
    ]
    ctx = build_context(chunks)
    assert "Alice" in ctx
    assert "Context 1" in ctx
    assert "Record" in ctx


def test_build_context_multiple_chunks():
    chunks = [
        {"text": "Chunk A", "source_type": "record",      "source_id": "r1", "patient_id": "p1", "score": 0.1},
        {"text": "Chunk B", "source_type": "appointment", "source_id": "a1", "patient_id": "p1", "score": 0.2},
    ]
    ctx = build_context(chunks)
    assert "Context 1" in ctx
    assert "Context 2" in ctx
    assert "Appointment" in ctx
    assert "---" in ctx  # separator between chunks
