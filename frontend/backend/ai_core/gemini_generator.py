from __future__ import annotations

import re

from backend.config import settings
from backend.schemas import GenerateRequest


try:
    from google import genai
    from google.genai import types
except ImportError:
    genai = None
    types = None


SYSTEM_INSTRUCTION = """
You are LegalEaseAI, an AI-assisted legal document drafting engine.

Your task is to draft clear, professional legal documents based only on
information supplied by the user.

You are not a lawyer and must not claim that a generated document is legally
binding, complete, or appropriate for a particular legal matter without
professional review.

Rules:

1. Never invent names, dates, amounts, addresses, statutes, case numbers,
   legal authorities, or facts.

2. If information is missing, use placeholders such as:

[INSERT DATE]
[INSERT PARTY NAME]
[INSERT ADDRESS]
[INSERT AMOUNT]

3. Use professional and neutral legal language.

4. Organize the document using a title and numbered sections.

5. Include practical clauses relevant to the requested document.

6. Include signature blocks where appropriate.

7. Do not fabricate laws or legal citations.

8. Do not give a legal opinion.

9. Output the document directly without unnecessary introductory discussion.

10. End with a short Review Notice explaining that a qualified legal
professional should review the document before signing or relying on it.
"""


def demo_document(
    payload: GenerateRequest
) -> str:

    title = (
        payload.title
        or payload.document_type
    )

    parties = (
        payload.parties
        or "[INSERT PARTY DETAILS]"
    )

    terms = (
        payload.key_terms
        or "[INSERT KEY TERMS]"
    )

    return f"""# {title}

**Document Type:** {payload.document_type}

**Jurisdiction:** {payload.jurisdiction}

**Language:** {payload.language}

## 1. Parties

This {payload.document_type} is entered into by and between:

{parties}

## 2. Purpose

The parties intend to establish the terms and conditions described in this
document and to record their mutual understanding.

## 3. Key Terms

{terms}

## 4. Responsibilities

Each party shall perform its agreed responsibilities in good faith and within
the time periods agreed by the parties.

## 5. Confidentiality

Where confidential information is exchanged, each party shall use reasonable
care to protect that information and shall not disclose it except as permitted
by the agreement or applicable law.

## 6. Term and Termination

The term shall begin on [INSERT START DATE] and continue until
[INSERT END DATE], unless terminated earlier in accordance with the agreed
terms.

## 7. Dispute Resolution

The parties should specify the applicable dispute-resolution procedure,
location, and governing law before execution.

## 8. Signatures

**Party 1**

Signature: ______________________________

Name: [INSERT NAME]

Date: [INSERT DATE]


**Party 2**

Signature: ______________________________

Name: [INSERT NAME]

Date: [INSERT DATE]


## Review Notice

This draft is AI-generated for assistance and should be reviewed and adapted
by a qualified legal professional before signing or relying on it.
"""


class GeminiGenerator:

    def __init__(self):

        self.client = None

        if (
            settings.GEMINI_API_KEY
            and genai is not None
        ):
            self.client = genai.Client(
                api_key=settings.GEMINI_API_KEY
            )

    def generate(
        self,
        payload: GenerateRequest
    ) -> dict:

        if settings.AI_PROVIDER != "gemini":

            return self._fallback(
                payload,
                "mock"
            )

        if self.client is None:

            if settings.MOCK_ON_MISSING_KEY:

                return self._fallback(
                    payload,
                    "demo"
                )

            raise ValueError(
                "GEMINI_API_KEY is missing. "
                "Add it to your .env file or "
                "enable MOCK_ON_MISSING_KEY=true."
            )

        prompt = self._build_prompt(
            payload
        )

        try:

            response = (
                self.client.models.generate_content(
                    model=settings.GEMINI_MODEL,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        system_instruction=SYSTEM_INSTRUCTION,
                        temperature=settings.TEMPERATURE,
                        max_output_tokens=12000,
                    ),
                )
            )

            text = (
                response.text or ""
            ).strip()

            if not text:

                raise ValueError(
                    "Gemini returned an empty response."
                )

            return {
                "document": self._clean_output(text),
                "provider": "gemini",
                "model": settings.GEMINI_MODEL,
                "disclaimer": (
                    "AI-generated draft. Review with a qualified "
                    "legal professional before signing or relying on it."
                ),
            }

        except Exception as exc:

            if settings.MOCK_ON_MISSING_KEY:

                return self._fallback(
                    payload,
                    f"demo-after-error: {exc}"
                )

            raise

    def _build_prompt(
        self,
        payload: GenerateRequest
    ) -> str:

        total_input = (
            len(payload.parties)
            + len(payload.key_terms)
            + len(payload.additional_instructions)
        )

        if total_input > settings.MAX_INPUT_CHARS:

            raise ValueError(
                f"Input is too large. Keep the combined "
                f"input under {settings.MAX_INPUT_CHARS} characters."
            )

        return f"""
Draft a {payload.document_type}.

Title:
{payload.title or payload.document_type}

Jurisdiction:
{payload.jurisdiction}

Language:
{payload.language}

Parties:
{payload.parties or "[NOT PROVIDED]"}

Key terms / facts:
{payload.key_terms or "[NOT PROVIDED]"}

Additional instructions:
{payload.additional_instructions or "[NONE]"}

Output requirements:

- Start immediately with the document title.
- Use Markdown headings.
- Use numbered sections.
- Include appropriate legal clauses.
- Use placeholders for missing information.
- Include signature blocks where appropriate.
- Do not invent laws or legal cases.
- Do not provide a legal opinion.
- End with a concise Review Notice.
"""

    @staticmethod
    def _clean_output(
        text: str
    ) -> str:

        text = text.replace(
            "\x00",
            ""
        )

        text = re.sub(
            r"\n{4,}",
            "\n\n\n",
            text
        )

        return text.strip()

    @staticmethod
    def _fallback(
        payload: GenerateRequest,
        provider: str
    ) -> dict:

        return {
            "document": demo_document(payload),
            "provider": provider,
            "model": settings.GEMINI_MODEL,
            "disclaimer": (
                "Demo draft only. Add a Gemini API key for AI generation. "
                "Review with a qualified legal professional before signing."
            ),
        }