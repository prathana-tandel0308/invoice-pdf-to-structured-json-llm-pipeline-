
import json
import tempfile
import time
from pathlib import Path

import streamlit as st

from src.pdf_extractor import convert_pdf_to_markdown
from src.text_cleaner import clean_markdown
from src.local_llm_filter import filter_invoice_markdown
import src.llm_extractor as extractor


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Invoice AI Extractor",
    page_icon="📄",
    layout="wide"
)


# --------------------------------------------------
# APPLICATION HEADER
# --------------------------------------------------

st.title("📄 Invoice PDF to Structured JSON")

st.write(
    "Extract structured invoice information using "
    "local and cloud Large Language Models."
)

st.divider()


# --------------------------------------------------
# PDF UPLOAD
# --------------------------------------------------

uploaded_file = st.file_uploader(
    "Upload your invoice PDF",
    type=["pdf"]
)


if uploaded_file is not None:

    st.success(f"Uploaded: {uploaded_file.name}")

    if st.button("Process Invoice", type="primary"):

        try:

            start_time = time.time()

            with st.spinner(
                "Processing invoice... Please wait."
            ):

                with tempfile.TemporaryDirectory() as temp_dir:

                    temp_dir = Path(temp_dir)

                    # Save uploaded PDF temporarily
                    pdf_path = temp_dir / uploaded_file.name

                    pdf_path.write_bytes(
                        uploaded_file.getvalue()
                    )

                    # STEP 1: PDF to Markdown
                    markdown_text = convert_pdf_to_markdown(
                        str(pdf_path),
                        str(temp_dir / "invoice.md")
                    )

                    # STEP 2: Clean Markdown
                    cleaned_text = clean_markdown(
                        markdown_text
                    )

                    # STEP 3: Local LLM filtering
                    filtered_text = filter_invoice_markdown(
                        cleaned_text
                    )

                    # STEP 4: Gemini extraction
                    invoice_data = extractor.extract_invoice_data(
                        filtered_text
                    )

                    # STEP 5: Pydantic validation
                    validated_data = invoice_data.model_dump(
                        mode="json"
                    )

                    # Capture Gemini token usage
                    usage = dict(
                        extractor.last_usage_metadata
                    )

            processing_time = time.time() - start_time

            # --------------------------------------------------
            # DISPLAY RESULTS
            # --------------------------------------------------

            st.success("Invoice processed successfully!")

            st.subheader("Extracted Invoice Information")

            st.json(validated_data)

            # --------------------------------------------------
            # GEMINI TOKEN USAGE
            # --------------------------------------------------

            st.subheader("Gemini API Token Usage")

            col1, col2, col3 = st.columns(3)

            col1.metric(
                "Input Tokens",
                usage.get("prompt_token_count") or 0
            )

            col2.metric(
                "Output Tokens",
                usage.get("candidates_token_count") or 0
            )

            col3.metric(
                "Total Reported Tokens",
                usage.get("total_token_count") or 0
            )

            st.metric(
                "Processing Time",
                f"{processing_time:.2f} seconds"
            )

            # --------------------------------------------------
            # DOWNLOAD JSON
            # --------------------------------------------------

            json_output = json.dumps(
                validated_data,
                indent=4,
                ensure_ascii=False
            )

            st.download_button(
                label="Download JSON",
                data=json_output,
                file_name="invoice_output.json",
                mime="application/json"
            )

        except Exception as error:

            st.error(
                f"Invoice processing failed: {error}"
            )
