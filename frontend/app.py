import os

import requests
import streamlit as st

from dotenv import load_dotenv


load_dotenv()


BACKEND_URL = os.getenv(
    "BACKEND_URL",
    "http://127.0.0.1:8000"
).rstrip("/")


TIMEOUT = int(
    os.getenv(
        "REQUEST_TIMEOUT_SECONDS",
        "120"
    )
)


st.set_page_config(
    page_title="LegalEaseAI",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded",
)


st.markdown(
    """
    <style>

    .main-title {
        font-size: 2.6rem;
        font-weight: 800;
        margin-bottom: 0.2rem;
    }

    .subtitle {
        font-size: 1.05rem;
        color: #6b7280;
        margin-bottom: 1.5rem;
    }

    .legal-note {
        padding: 0.9rem 1rem;
        border-left: 4px solid #7c3aed;
        background: #f5f3ff;
        border-radius: 6px;
        margin: 1rem 0;
    }

    </style>
    """,
    unsafe_allow_html=True
)


if "document" not in st.session_state:

    st.session_state.document = ""


if "last_title" not in st.session_state:

    st.session_state.last_title = (
        "Legal Document"
    )


st.markdown(
    '<div class="main-title">⚖️ LegalEaseAI</div>',
    unsafe_allow_html=True
)


st.markdown(
    """
    <div class="subtitle">
    AI-assisted legal document drafting, editing and export.
    </div>
    """,
    unsafe_allow_html=True
)


with st.sidebar:

    st.header(
        "Document Setup"
    )

    document_type = st.selectbox(
        "Document type",
        [
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
    )

    title = st.text_input(
        "Document title",
        value=document_type,
        max_chars=200
    )

    jurisdiction = st.text_input(
        "Jurisdiction",
        value="India"
    )

    language = st.selectbox(
        "Language",
        [
            "English",
            "Tamil",
            "Hindi"
        ]
    )

    parties = st.text_area(
        "Parties",
        placeholder=(
            "Example:\n"
            "Party 1: ABC Technologies Pvt Ltd\n"
            "Party 2: Ravi Kumar"
        ),
        height=120
    )

    key_terms = st.text_area(
        "Key terms / facts",
        placeholder=(
            "Enter important facts, payment terms, "
            "duration, responsibilities, confidentiality "
            "requirements, etc."
        ),
        height=180
    )

    additional = st.text_area(
        "Additional instructions",
        placeholder=(
            "Any special clauses or formatting "
            "requirements..."
        ),
        height=120
    )

    generate = st.button(
        "✨ Generate Document",
        type="primary",
        use_container_width=True
    )

    if st.button(
        "🗑️ Clear",
        use_container_width=True
    ):

        st.session_state.document = ""

        st.rerun()

    st.divider()

    st.caption(
        f"Backend: {BACKEND_URL}"
    )


if generate:

    payload = {
        "document_type": document_type,
        "title": title,
        "jurisdiction": jurisdiction,
        "language": language,
        "parties": parties,
        "key_terms": key_terms,
        "additional_instructions": additional,
    }

    try:

        with st.spinner(
            "Generating your document..."
        ):

            response = requests.post(
                f"{BACKEND_URL}/generate",
                json=payload,
                timeout=TIMEOUT
            )

        response.raise_for_status()

        data = response.json()

        st.session_state.document = (
            data["document"]
        )

        st.session_state.last_title = (
            title or document_type
        )

        provider = data.get(
            "provider",
            "unknown"
        )

        if provider == "gemini":

            st.success(
                "Document generated with Gemini."
            )

        else:

            st.info(
                "Demo mode generated the document. "
                "Add GEMINI_API_KEY for AI generation."
            )

    except requests.exceptions.ConnectionError:

        st.error(
            "Cannot connect to the FastAPI backend.\n\n"
            "Start it with:\n\n"
            "uvicorn backend.main:app "
            "--reload --host 127.0.0.1 --port 8000"
        )

    except requests.exceptions.RequestException as exc:

        st.error(
            f"Backend request failed: {exc}"
        )

    except Exception as exc:

        st.error(
            f"Unexpected error: {exc}"
        )


left, right = st.columns(
    [1.15, 1]
)


with left:

    st.subheader(
        "📝 Editable Document"
    )

    edited = st.text_area(
        "Edit the generated document directly",
        value=st.session_state.document,
        height=620,
        label_visibility="collapsed",
        placeholder=(
            "Your generated legal document "
            "will appear here..."
        )
    )

    st.session_state.document = edited


with right:

    st.subheader(
        "👁️ Preview"
    )

    if st.session_state.document:

        st.markdown(
            st.session_state.document
        )

    else:

        st.info(
            "Generate a document to see the preview."
        )


st.divider()


st.subheader(
    "📥 Export"
)


if st.session_state.document:

    export_col1, export_col2, export_col3 = (
        st.columns(3)
    )

    export_payload = {
        "filename": (
            st.session_state.last_title
            or "legalease_document"
        ).replace(" ", "_"),

        "title": (
            st.session_state.last_title
        ),

        "document": (
            st.session_state.document
        ),
    }


    with export_col1:

        if st.button(
            "Export TXT",
            use_container_width=True
        ):

            try:

                r = requests.post(
                    f"{BACKEND_URL}/export/txt",
                    json=export_payload,
                    timeout=TIMEOUT
                )

                r.raise_for_status()

                st.download_button(
                    "⬇️ Download TXT",
                    data=r.content,
                    file_name="legalease_document.txt",
                    mime="text/plain",
                    use_container_width=True
                )

            except Exception as exc:

                st.error(
                    f"TXT export failed: {exc}"
                )


    with export_col2:

        if st.button(
            "Export DOCX",
            use_container_width=True
        ):

            try:

                r = requests.post(
                    f"{BACKEND_URL}/export/docx",
                    json=export_payload,
                    timeout=TIMEOUT
                )

                r.raise_for_status()

                st.download_button(
                    "⬇️ Download DOCX",
                    data=r.content,
                    file_name="legalease_document.docx",
                    mime=(
                        "application/"
                        "vnd.openxmlformats-officedocument."
                        "wordprocessingml.document"
                    ),
                    use_container_width=True
                )

            except Exception as exc:

                st.error(
                    f"DOCX export failed: {exc}"
                )


    with export_col3:

        if st.button(
            "Export PDF",
            use_container_width=True
        ):

            try:

                r = requests.post(
                    f"{BACKEND_URL}/export/pdf",
                    json=export_payload,
                    timeout=TIMEOUT
                )

                r.raise_for_status()

                st.download_button(
                    "⬇️ Download PDF",
                    data=r.content,
                    file_name="legalease_document.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )

            except Exception as exc:

                st.error(
                    f"PDF export failed: {exc}"
                )

else:

    st.caption(
        "Generate a document first to enable export."
    )


st.markdown(
    """
    <div class="legal-note">
    <b>Important:</b> LegalEaseAI provides AI-assisted drafting,
    not legal advice. Review every document with a qualified legal
    professional before signing or relying on it.
    </div>
    """,
    unsafe_allow_html=True
)