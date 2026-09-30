# LegalEaseAI

LegalEaseAI is an AI-assisted legal document drafting application.

It uses:

- Streamlit
- FastAPI
- Google Gemini
- Python
- DOCX generation
- PDF generation

The application allows users to:

1. Select a legal document type.
2. Enter parties and facts.
3. Enter important terms.
4. Generate a legal document.
5. Edit the generated document.
6. Preview the document.
7. Export the document as TXT.
8. Export the document as DOCX.
9. Export the document as PDF.

---

# Architecture

```text
Streamlit Frontend
        |
        v
FastAPI Backend
        |
        v
Gemini AI
        |
        v
Generated Legal Document
        |
        +------> Edit
        |
        +------> Preview
        |
        +------> TXT
        |
        +------> DOCX
        |
        +------> PDF