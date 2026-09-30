from typing import Literal

from pydantic import BaseModel, Field, field_validator


DocumentType = Literal[
    "NDA",
    "Employment Agreement",
    "Freelance Agreement",
    "Rental Agreement",
    "Service Agreement",
    "Partnership Agreement",
    "Sales Agreement",
    "Privacy Policy",
    "Memorandum of Understanding",
    "Custom",
]


class GenerateRequest(BaseModel):
    document_type: DocumentType

    title: str = Field(
        default="",
        max_length=200
    )

    jurisdiction: str = Field(
        default="India",
        max_length=200
    )

    language: str = Field(
        default="English",
        max_length=50
    )

    parties: str = Field(
        default="",
        max_length=4000
    )

    key_terms: str = Field(
        default="",
        max_length=8000
    )

    additional_instructions: str = Field(
        default="",
        max_length=4000
    )

    @field_validator(
        "parties",
        "key_terms",
        "additional_instructions"
    )
    @classmethod
    def strip_text(cls, value: str) -> str:
        return value.strip()


class GenerateResponse(BaseModel):
    document: str
    provider: str
    model: str
    disclaimer: str


class ExportRequest(BaseModel):
    filename: str = Field(
        default="legalease_document",
        max_length=100
    )

    title: str = Field(
        default="Legal Document",
        max_length=200
    )

    document: str = Field(
        min_length=1,
        max_length=100000
    )