from pydantic import BaseModel, Field
from typing import Optional, List


class QueryRequest(BaseModel):
    query: str = Field(..., min_length=3, max_length=1000, description="Natural language question")
    patient_id: Optional[str] = Field(None, description="Scope results to a specific patient UUID")
    top_k: Optional[int] = Field(5, ge=1, le=20, description="Number of context chunks to retrieve")
    question_category: Optional[str] = Field(None, description="Optional category of the question")


class SourceChunk(BaseModel):
    text: str
    source_type: str   # "profile" | "record" | "appointment" | "vital" | "diagnosis" | "prescription" | "parsed_data" | "access_grant" | "access_request"
    source_id: str
    patient_id: str
    score: float


class QueryResponse(BaseModel):
    answer: str
    sources: List[SourceChunk]
    query: str
    answer_mode: str = Field("record_grounded", description="Answering mode: record_grounded or general_medical")
    follow_up_questions: List[str] = Field(default_factory=list, description="AI suggested follow-up questions")


class QuestionInfo(BaseModel):
    id: int
    question_text: str
    requires_records: bool
    category: str


class QuestionCategory(BaseModel):
    category_name: str
    questions: List[QuestionInfo]


class QuestionBankResponse(BaseModel):
    categories: List[QuestionCategory]



class ReindexResponse(BaseModel):
    status: str
    total_chunks: int
    message: str


class HealthResponse(BaseModel):
    status: str
    index_loaded: bool
    total_vectors: int
    llm_provider: str
    embedding_model: str


class CompareRequest(BaseModel):
    patient_id_1: str = Field(..., description="First patient ID (e.g. P001)")
    patient_id_2: str = Field(..., description="Second patient ID (e.g. P002)")
    aspects: Optional[List[str]] = Field(
        None,
        description="Optional list of aspects to compare (e.g. ['risk_factors', 'medications', 'lifestyle']). If empty, compares all."
    )


class CompareResponse(BaseModel):
    comparison: str
    patient_1_summary: str
    patient_2_summary: str
    query: str

