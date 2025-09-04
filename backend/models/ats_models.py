from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

class FileType(str, Enum):
    PDF = "pdf"
    DOCX = "docx"

class AnalysisStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class GrammarIssue(BaseModel):
    text: str
    line_number: int
    suggestion: str
    severity: str  # low, medium, high

class RepetitionIssue(BaseModel):
    word: str
    count: int
    positions: List[int]

class FormatIssue(BaseModel):
    issue_type: str
    description: str
    suggestion: str

class ATSScore(BaseModel):
    percentage: float
    category: str
    description: str

class AnalysisResult(BaseModel):
    id: str
    percentage_score: float
    jd_match: float
    missing_keywords: List[str]
    profile_summary: str
    grammar_mistakes: List[GrammarIssue]
    word_repetitions: List[RepetitionIssue]
    format_issues: List[FormatIssue]
    readability_score: float
    timestamp: datetime
    status: AnalysisStatus

class ResumeUpload(BaseModel):
    file_type: FileType
    job_description: str

class JobDescription(BaseModel):
    title: str
    company: str
    description: str
    requirements: List[str]
    skills: List[str]

class ResumeAnalysisRequest(BaseModel):
    job_description: str
    resume_text: str
    file_type: FileType

class APIResponse(BaseModel):
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None