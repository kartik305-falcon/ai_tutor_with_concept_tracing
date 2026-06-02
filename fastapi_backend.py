from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import Response
from pydantic import BaseModel
from typing import List, Optional
import tempfile
import os
from dotenv import load_dotenv
load_dotenv()

from rag_llm import ask_tutor
from auto_grader import grade_code
from concept_analytics import compute_mastery
from file_loader import load_pdf, load_image
from ingest import ingest_raw_text
from quiz_generator import generate_adaptive_quiz, generate_practice_scenario
from gamification import award_xp, get_xp_summary, init_gamification_tables
from study_notes import generate_study_notes, export_pdf
from image_debugger import debug_image
from github_fetcher import fetch_github_code, review_github_code
from curriculum_planner import generate_learning_path
from trace_db import init_db

# Initialize DB tables
init_db()
init_gamification_tables()

app = FastAPI(title="CodeTutor AI API")

# CORS configuration
_raw_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000")
ALLOWED_ORIGINS = [o.strip() for o in _raw_origins.split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type", "Authorization"],
)

# ============================================
# Request/Response Models
# ============================================

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    message: str
    history: Optional[List[ChatMessage]] = None
    language: Optional[str] = "c"
    socratic_mode: Optional[bool] = False

class ChatResponse(BaseModel):
    response: str

class TestCase(BaseModel):
    input: str
    expected: str

class GradeRequest(BaseModel):
    code: str
    test_cases: List[TestCase]
    language: Optional[str] = "c"

class GradeResponse(BaseModel):
    passed: int
    total: int
    score: float
    details: List[dict]
    pro_tip: Optional[str] = None

class MasteryResponse(BaseModel):
    concepts: List[dict]

class HintRequest(BaseModel):
    code: str
    test_input: str
    test_expected: str
    error_or_got: str
    language: str = "c"

class HintResponse(BaseModel):
    hint: str

class StudyNotesRequest(BaseModel):
    history: List[ChatMessage]
    language: Optional[str] = "c"

class GitHubReviewRequest(BaseModel):
    url: str
    language: Optional[str] = "python"

# ============================================
# API Endpoints
# ============================================

@app.get("/api/health")
async def health():
    return {"status": "ok", "message": "AI Tutor API is running"}

# ----- Chat (Feature 1: Socratic Mode) -----

@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Handle chat — supports Socratic Mode toggle."""
    try:
        history_list = None
        if request.history:
            history_list = [{"role": msg.role, "content": msg.content} for msg in request.history]

        lang = request.language or "c"
        mode = "socratic" if request.socratic_mode else "tutor"

        answer = ask_tutor(request.message, language=lang, history=history_list, mode=mode)

        # Award XP for chatting
        try:
            award_xp("chat")
        except Exception:
            pass

        return ChatResponse(response=answer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ----- File Upload -----

@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...), language: str = Form(default="c")):
    """Handle file uploads (PDF or Image) for knowledge ingestion."""
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as tmp:
            content = await file.read()
            tmp.write(content)
            tmp_path = tmp.name

        if file.content_type == "application/pdf":
            with open(tmp_path, 'rb') as f:
                extracted_text = load_pdf(f)
        elif file.content_type.startswith("image/"):
            extracted_text = load_image(tmp_path)
        else:
            raise HTTPException(status_code=400, detail="Unsupported file type")

        chunks_count = ingest_raw_text(extracted_text, source=file.filename, language=language)
        os.unlink(tmp_path)

        return {
            "success": True,
            "filename": file.filename,
            "chunks": chunks_count,
            "message": f"✅ '{file.filename}' indexed successfully!"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ----- Grade Code (Feature 2: Smart Error Explainer) -----

@app.post("/api/grade", response_model=GradeResponse)
async def grade(request: GradeRequest):
    """Grade code — details include plain_explanation from Smart Error Explainer."""
    try:
        test_cases = [{"input": tc.input, "expected": tc.expected} for tc in request.test_cases]
        lang = (request.language or "c").lower()
        result = grade_code(request.code, test_cases, language=lang)

        # Award XP based on result
        try:
            if result["passed"] == result["total"] and result["total"] > 0:
                award_xp("code_pass")
            elif result["passed"] > 0:
                award_xp("code_partial")
        except Exception:
            pass

        return GradeResponse(
            passed=result["passed"],
            total=result["total"],
            score=result["score"],
            details=result["details"],
            pro_tip=result.get("pro_tip")
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ----- AI Hint -----

@app.post("/api/hint", response_model=HintResponse)
async def get_hint(request: HintRequest):
    try:
        from auto_grader import get_ai_hint
        hint = get_ai_hint(
            request.code, request.test_input, request.test_expected,
            request.error_or_got, language=request.language
        )
        return HintResponse(hint=hint)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ----- Practice Scenario / Duel (Feature 7) -----

@app.get("/api/scenario")
async def get_scenario(language: str = "C", difficulty: str = "medium"):
    """Generate a practice challenge. Used by both AI Challenge and Code Duel."""
    try:
        scenario = generate_practice_scenario(language=language)
        if not scenario:
            raise Exception("Failed to generate scenario")

        # Attach time limit for Duel mode
        time_limits = {"easy": 300, "medium": 180, "hard": 120}
        scenario["time_limit"] = time_limits.get(difficulty.lower(), 180)
        scenario["difficulty"] = difficulty
        return scenario
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ----- Mastery -----

@app.get("/api/mastery", response_model=MasteryResponse)
async def get_mastery():
    try:
        mastery = compute_mastery()
        concepts = [
            {"concept": concept, "attempts": data["attempts"], "confidence": data["avg_confidence"]}
            for concept, data in mastery.items()
        ]
        return MasteryResponse(concepts=concepts)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ----- Quiz (Feature 5: award XP) -----

@app.get("/api/quiz")
async def get_quiz(language: str = "C"):
    try:
        quiz, weak = generate_adaptive_quiz(language=language)
        try:
            award_xp("quiz_complete")
        except Exception:
            pass
        return {"quiz": quiz, "weak_concepts": weak}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ----- XP & Streak (Feature 5) -----

@app.get("/api/xp")
async def get_xp():
    """Return current XP summary: total_xp, level, level_name, streak, progress_pct."""
    try:
        return get_xp_summary()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/xp/award")
async def award_xp_endpoint(event: str = "chat"):
    """Manually award XP for a specific event."""
    try:
        result = award_xp(event)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ----- Study Notes (Feature 4) -----

@app.post("/api/study-notes")
async def get_study_notes(request: StudyNotesRequest):
    """Generate structured study notes from chat history."""
    try:
        history = [{"role": msg.role, "content": msg.content} for msg in request.history]
        notes = generate_study_notes(history, language=request.language or "c")
        if "error" in notes:
            raise HTTPException(status_code=500, detail=notes["error"])
        try:
            award_xp("notes_gen")
        except Exception:
            pass
        return notes
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/study-notes/pdf")
async def get_study_notes_pdf(request: StudyNotesRequest):
    """Generate and return a PDF of study notes."""
    try:
        history = [{"role": msg.role, "content": msg.content} for msg in request.history]
        notes = generate_study_notes(history, language=request.language or "c")
        if "error" in notes:
            raise HTTPException(status_code=500, detail=notes["error"])
        pdf_bytes = export_pdf(notes)
        title_slug = notes.get("title", "study_notes").replace(" ", "_")[:40]
        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={"Content-Disposition": f'attachment; filename="{title_slug}.pdf"'}
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ----- Image Debugging (Feature 3) -----

@app.post("/api/debug-image")
async def debug_image_endpoint(
    file: UploadFile = File(...),
    language: str = Form(default="c")
):
    """Analyze a screenshot of code/error and explain the concept behind it."""
    try:
        ext = os.path.splitext(file.filename or "error.png")[1] or ".png"
        with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp:
            content = await file.read()
            tmp.write(content)
            tmp_path = tmp.name

        result = debug_image(tmp_path, language=language)
        os.unlink(tmp_path)

        if not result.get("success"):
            raise HTTPException(status_code=500, detail=result.get("error_detected", "Analysis failed"))

        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ----- GitHub Code Review (Feature 9) -----

@app.post("/api/review-github")
async def review_github(request: GitHubReviewRequest):
    """Fetch a public GitHub file and return an AI code review."""
    try:
        filename, code = fetch_github_code(request.url)
        review = review_github_code(code, request.language or "python", filename)
        if "error" in review:
            raise HTTPException(status_code=500, detail=review["error"])
        review["filename"] = filename
        review["code_preview"] = code[:2000] + ("..." if len(code) > 2000 else "")
        return review
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ----- Learning Path (Feature 14) -----

@app.get("/api/learning-path")
async def get_learning_path(language: str = "C"):
    """Generate personalized 7-day learning path based on mastery data."""
    try:
        mastery = compute_mastery()
        plan = generate_learning_path(mastery, language=language)
        return {"language": language, "plan": plan}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ============================================
# Serve Frontend Static Files
# ============================================
frontend_path = os.path.join(os.path.dirname(__file__), "frontend")
if os.path.exists(frontend_path):
    app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")
else:
    print(f"Warning: Frontend directory not found at {frontend_path}")


# ============================================
# Run with: uvicorn fastapi_backend:app --reload
# ============================================
