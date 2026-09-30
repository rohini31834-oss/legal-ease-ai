from io import BytesIO

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

from backend.config import settings
from backend.schemas import (
    ExportRequest,
    GenerateRequest,
    GenerateResponse,
)

from backend.ai_core.gemini_generator import GeminiGenerator

from backend.document_utils.formatters import (
    build_docx,
    build_pdf,
    clean_filename,
    document_to_text,
)


router = APIRouter()

generator = GeminiGenerator()


@router.get("/health")
def health():
    return {
        "status": "ok",
        "app": settings.APP_NAME,
        "provider": settings.AI_PROVIDER,
        "model": settings.GEMINI_MODEL,
        "demo_mode": not bool(settings.GEMINI_API_KEY),
    }


@router.post(
    "/generate",
    response_model=GenerateResponse
)
def generate_document(
    payload: GenerateRequest
):
    try:
        result = generator.generate(payload)

        return result

    except ValueError as exc:

        raise HTTPException(
            status_code=400,
            detail=str(exc)
        ) from exc

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=f"Document generation failed: {exc}"
        ) from exc


@router.post("/export/txt")
def export_txt(
    payload: ExportRequest
):
    filename = clean_filename(
        payload.filename,
        "txt"
    )

    content = document_to_text(
        payload.document
    ).encode("utf-8")

    return StreamingResponse(
        BytesIO(content),
        media_type="text/plain; charset=utf-8",
        headers={
            "Content-Disposition":
            f'attachment; filename="{filename}"'
        },
    )


@router.post("/export/docx")
def export_docx(
    payload: ExportRequest
):
    filename = clean_filename(
        payload.filename,
        "docx"
    )

    buffer = build_docx(
        payload.title,
        payload.document
    )

    return StreamingResponse(
        buffer,
        media_type=(
            "application/vnd.openxmlformats-officedocument."
            "wordprocessingml.document"
        ),
        headers={
            "Content-Disposition":
            f'attachment; filename="{filename}"'
        },
    )


@router.post("/export/pdf")
def export_pdf(
    payload: ExportRequest
):
    filename = clean_filename(
        payload.filename,
        "pdf"
    )

    buffer = build_pdf(
        payload.title,
        payload.document
    )

    return StreamingResponse(
        buffer,
        media_type="application/pdf",
        headers={
            "Content-Disposition":
            f'attachment; filename="{filename}"'
        },
    )