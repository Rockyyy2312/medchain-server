"""
Unit tests for LLM generator (mocked).
Run with: pytest tests/test_generator.py -v
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import pytest
from unittest.mock import AsyncMock, patch, MagicMock


# ── Prompt builder tests ───────────────────────────────────────────────────────

def test_build_prompt_contains_context():
    from llm.generator import _build_prompt
    prompt = _build_prompt("Patient has blood pressure issues.", "What is my blood pressure?")
    assert "blood pressure" in prompt
    assert "Patient Question" in prompt
    assert "Answer:" in prompt


def test_build_prompt_contains_system_prompt():
    from llm.generator import _build_prompt, SYSTEM_PROMPT
    prompt = _build_prompt("some context", "some query")
    assert "MedChain AI" in prompt


# ── Gemini call test (mocked) ──────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_call_gemini_success():
    """Test that _call_gemini correctly parses Gemini API response."""
    from llm.generator import _call_gemini

    mock_response = MagicMock()
    mock_response.json.return_value = {
        "candidates": [
            {
                "content": {
                    "parts": [{"text": "Your blood pressure is 120/80."}]
                }
            }
        ]
    }

    with patch("httpx.AsyncClient") as mock_client_class:
        mock_client = AsyncMock()
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=None)
        mock_client.post = AsyncMock(return_value=mock_response)
        mock_client_class.return_value = mock_client

        with patch("llm.generator.GEMINI_API_KEY", "test-key"):
            result = await _call_gemini("test prompt")

    assert "blood pressure" in result.lower()


@pytest.mark.asyncio
async def test_call_gemini_no_api_key():
    """When GEMINI_API_KEY is empty, returns config error message."""
    from llm.generator import _call_gemini
    with patch("llm.generator.GEMINI_API_KEY", ""):
        result = await _call_gemini("test prompt")
    assert "not configured" in result.lower() or "api key" in result.lower()


@pytest.mark.asyncio
async def test_generate_answer_timeout():
    """Timeout should return a user-friendly message."""
    import httpx
    from llm.generator import generate_answer

    with patch("llm.generator._call_gemini", side_effect=httpx.TimeoutException("timeout")):
        with patch("llm.generator.LLM_PROVIDER", "gemini"):
            result = await generate_answer("context", "query")
    assert "timed out" in result.lower() or "timeout" in result.lower()
