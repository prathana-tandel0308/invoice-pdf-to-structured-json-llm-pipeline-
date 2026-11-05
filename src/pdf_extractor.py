
import pymupdf4llm
from pathlib import Path


def convert_pdf_to_markdown(pdf_path, output_path):

    # Convert PDF content into Markdown with OCR support
    markdown_text = pymupdf4llm.to_markdown(
        pdf_path,
        use_ocr=True,
        force_ocr=False,
        ocr_language="eng"
    )

    # Create output folder if it does not exist
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    # Save Markdown content into a .md file
    output_file.write_text(markdown_text, encoding="utf-8")

    return markdown_text
