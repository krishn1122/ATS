from fastapi import FastAPI, File, UploadFile, Form, HTTPException, BackgroundTasks, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
import logging
from typing import Optional, Dict, Any
import uuid
from datetime import datetime
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
load_dotenv()

try:
    from ..models.ats_models import AnalysisResult, APIResponse, ResumeAnalysisRequest, AnalysisStatus
    from ..services.ai_service import AIAnalysisService, AnalysisCache
    from ..utils.document_parser import DocumentParser
except ImportError:
    # For running standalone or tests
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from models.ats_models import AnalysisResult, APIResponse, ResumeAnalysisRequest, AnalysisStatus
    from services.ai_service import AIAnalysisService, AnalysisCache
    from utils.document_parser import DocumentParser

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Smart ATS API",
    description="Professional ATS (Application Tracking System) API for resume analysis",
    version="2.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# Mount static files and templates for frontend integration
# Check multiple possible paths for frontend files
frontend_paths = [
    Path("frontend"),  # Standard path
    Path("../frontend"),  # From backend directory
    Path("../../frontend"),  # From backend/app directory
]

static_path = None
templates_path = None

# Find the correct frontend path
for base_path in frontend_paths:
    if (base_path / "static").exists() and (base_path / "templates").exists():
        static_path = base_path / "static"
        templates_path = base_path / "templates"
        logger.info(f"Found frontend files at: {base_path}")
        break

if static_path and static_path.exists():
    app.mount("/static", StaticFiles(directory=str(static_path)), name="static")
    logger.info(f"Mounted static files from: {static_path}")

if templates_path and templates_path.exists():
    templates = Jinja2Templates(directory=str(templates_path))
    logger.info(f"Loaded templates from: {templates_path}")
else:
    templates = None
    logger.warning("Frontend templates not found")

# CORS middleware for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for Railway deployment
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services (delayed initialization)
ai_service = None
analysis_cache = None
document_parser = None

def get_ai_service():
    global ai_service
    if ai_service is None:
        ai_service = AIAnalysisService()
    return ai_service

def get_analysis_cache():
    global analysis_cache
    if analysis_cache is None:
        analysis_cache = AnalysisCache()
    return analysis_cache

def get_document_parser():
    global document_parser
    if document_parser is None:
        document_parser = DocumentParser()
    return document_parser

# In-memory storage for analysis results (in production, use a database)
analysis_results: Dict[str, AnalysisResult] = {}

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Serve the home page"""
    if templates:
        try:
            return templates.TemplateResponse("index.html", {"request": request})
        except Exception as e:
            logger.error(f"Error serving home page: {e}")
    
    # Fallback HTML if templates not available
    return HTMLResponse(content="""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Smart ATS</title>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body>
        <div class="container mt-5">
            <h1 class="text-center">Smart ATS - Resume Analysis</h1>
            <div class="alert alert-info">
                <p><strong>Backend API is running!</strong></p>
                <p>API Documentation: <a href="/api/docs">/api/docs</a></p>
                <p>Health Check: <a href="/api/health">/api/health</a></p>
            </div>
        </div>
    </body>
    </html>
    """)

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    """Serve the dashboard page"""
    if templates:
        try:
            return templates.TemplateResponse("dashboard.html", {"request": request})
        except Exception as e:
            logger.error(f"Error serving dashboard: {e}")
    return HTMLResponse(content="<h1>Dashboard not available</h1>")

@app.get("/about", response_class=HTMLResponse)
async def about(request: Request):
    """Serve the about page"""
    if templates:
        try:
            return templates.TemplateResponse("about.html", {"request": request})
        except Exception as e:
            logger.error(f"Error serving about page: {e}")
    return HTMLResponse(content="<h1>About page not available</h1>")

@app.get("/results", response_class=HTMLResponse)
async def results(request: Request):
    """Serve the results page"""
    if templates:
        try:
            return templates.TemplateResponse("results.html", {"request": request})
        except Exception as e:
            logger.error(f"Error serving results page: {e}")
    return HTMLResponse(content="<h1>Results page not available</h1>")

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.post("/api/analyze-resume", response_model=APIResponse)
async def analyze_resume(
    background_tasks: BackgroundTasks,
    resume_file: UploadFile = File(...),
    job_description: str = Form(...)
):
    """
    Analyze resume against job description
    Supports PDF and DOCX formats
    """
    try:
        # Validate file type
        if not resume_file.filename:
            raise HTTPException(status_code=400, detail="No file provided")
        
        file_extension = resume_file.filename.split('.')[-1].lower()
        if file_extension not in ['pdf', 'docx']:
            raise HTTPException(
                status_code=400, 
                detail="Unsupported file format. Please upload PDF or DOCX files only."
            )
        
        # Read file content
        file_content = await resume_file.read()
        
        # Extract text from document
        resume_text = get_document_parser().parse_document(file_content, file_extension)
        
        if not resume_text:
            raise HTTPException(
                status_code=400, 
                detail="Failed to extract text from the document. Please ensure the file is not corrupted."
            )
        
        # Check cache first
        cache_key = get_analysis_cache().generate_cache_key(resume_text, job_description)
        cached_result = get_analysis_cache().get(cache_key)
        
        if cached_result:
            logger.info(f"Returning cached result for key: {cache_key[:8]}...")
            return APIResponse(
                success=True,
                message="Analysis completed (cached)",
                data=cached_result.dict()
            )
        
        # Create analysis ID for tracking
        analysis_id = str(uuid.uuid4())
        
        # Create initial pending result
        pending_result = AnalysisResult(
            id=analysis_id,
            percentage_score=0,
            jd_match=0,
            missing_keywords=[],
            profile_summary="Analysis in progress...",
            grammar_mistakes=[],
            word_repetitions=[],
            format_issues=[],
            readability_score=0,
            timestamp=datetime.now(),
            status=AnalysisStatus.PROCESSING
        )
        
        analysis_results[analysis_id] = pending_result
        
        # Start background analysis
        background_tasks.add_task(
            perform_analysis, 
            analysis_id, 
            resume_text, 
            job_description, 
            cache_key
        )
        
        return APIResponse(
            success=True,
            message="Analysis started",
            data={
                "analysis_id": analysis_id,
                "status": "processing",
                "estimated_time": "30-60 seconds"
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in analyze_resume: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

async def perform_analysis(analysis_id: str, resume_text: str, job_description: str, cache_key: str):
    """Background task to perform comprehensive analysis"""
    try:
        logger.info(f"Starting analysis for ID: {analysis_id}")
        
        # Perform comprehensive analysis
        result = get_ai_service().analyze_resume_comprehensive(resume_text, job_description)
        result.id = analysis_id  # Ensure correct ID
        
        # Store result
        analysis_results[analysis_id] = result
        
        # Cache the result
        get_analysis_cache().set(cache_key, result)
        
        logger.info(f"Analysis completed for ID: {analysis_id}")
        
    except Exception as e:
        logger.error(f"Error in background analysis for ID {analysis_id}: {str(e)}")
        
        # Create error result
        error_result = AnalysisResult(
            id=analysis_id,
            percentage_score=0,
            jd_match=0,
            missing_keywords=[],
            profile_summary=f"Analysis failed: {str(e)}",
            grammar_mistakes=[],
            word_repetitions=[],
            format_issues=[],
            readability_score=0,
            timestamp=datetime.now(),
            status=AnalysisStatus.FAILED
        )
        
        analysis_results[analysis_id] = error_result

@app.get("/api/analysis/{analysis_id}", response_model=APIResponse)
async def get_analysis_result(analysis_id: str):
    """Get analysis result by ID"""
    try:
        result = analysis_results.get(analysis_id)
        
        if not result:
            raise HTTPException(status_code=404, detail="Analysis not found")
        
        return APIResponse(
            success=True,
            message="Analysis result retrieved",
            data=result.dict()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving analysis {analysis_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to retrieve analysis result")

@app.get("/api/analysis/{analysis_id}/status")
async def get_analysis_status(analysis_id: str):
    """Get analysis status"""
    try:
        result = analysis_results.get(analysis_id)
        
        if not result:
            raise HTTPException(status_code=404, detail="Analysis not found")
        
        return {
            "analysis_id": analysis_id,
            "status": result.status.value,
            "timestamp": result.timestamp.isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting analysis status {analysis_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get analysis status")

@app.post("/api/analyze-text", response_model=APIResponse)
async def analyze_resume_text(request: ResumeAnalysisRequest):
    """Analyze resume from text input (for testing purposes)"""
    try:
        # Check cache first
        cache_key = get_analysis_cache().generate_cache_key(request.resume_text, request.job_description)
        cached_result = get_analysis_cache().get(cache_key)
        
        if cached_result:
            return APIResponse(
                success=True,
                message="Analysis completed (cached)",
                data=cached_result.dict()
            )
        
        # Perform analysis
        result = get_ai_service().analyze_resume_comprehensive(request.resume_text, request.job_description)
        
        # Cache the result
        get_analysis_cache().set(cache_key, result)
        
        # Store result
        analysis_results[result.id] = result
        
        return APIResponse(
            success=True,
            message="Analysis completed",
            data=result.dict()
        )
        
    except Exception as e:
        logger.error(f"Error in analyze_resume_text: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.get("/api/supported-formats")
async def get_supported_formats():
    """Get supported file formats"""
    return {
        "supported_formats": ["PDF", "DOCX"],
        "max_file_size": "10MB",
        "restrictions": [
            "File must contain readable text",
            "Password-protected files are not supported",
            "Scanned images without OCR are not supported"
        ]
    }

@app.delete("/api/analysis/{analysis_id}")
async def delete_analysis(analysis_id: str):
    """Delete analysis result"""
    try:
        if analysis_id not in analysis_results:
            raise HTTPException(status_code=404, detail="Analysis not found")
        
        del analysis_results[analysis_id]
        
        return {"message": "Analysis deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting analysis {analysis_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to delete analysis")

@app.get("/api/analytics/summary")
async def get_analytics_summary():
    """Get analytics summary of all analyses"""
    try:
        if not analysis_results:
            return {
                "total_analyses": 0,
                "average_score": 0,
                "common_issues": [],
                "success_rate": 0
            }
        
        completed_analyses = [r for r in analysis_results.values() if r.status == AnalysisStatus.COMPLETED]
        
        if not completed_analyses:
            return {
                "total_analyses": len(analysis_results),
                "average_score": 0,
                "common_issues": [],
                "success_rate": 0
            }
        
        # Calculate statistics
        total_score = sum(r.percentage_score for r in completed_analyses)
        average_score = total_score / len(completed_analyses)
        
        # Collect common issues
        all_grammar_issues = []
        all_format_issues = []
        for result in completed_analyses:
            all_grammar_issues.extend([issue.text for issue in result.grammar_mistakes])
            all_format_issues.extend([issue.issue_type for issue in result.format_issues])
        
        # Calculate success rate
        success_rate = len(completed_analyses) / len(analysis_results) * 100
        
        return {
            "total_analyses": len(analysis_results),
            "completed_analyses": len(completed_analyses),
            "average_score": round(average_score, 2),
            "success_rate": round(success_rate, 2),
            "common_grammar_issues": list(set(all_grammar_issues))[:5],
            "common_format_issues": list(set(all_format_issues))
        }
        
    except Exception as e:
        logger.error(f"Error getting analytics summary: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get analytics summary")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)