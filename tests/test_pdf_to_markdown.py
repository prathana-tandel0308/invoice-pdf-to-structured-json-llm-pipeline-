
from src.pdf_extractor import convert_pdf_to_markdown

pdf_path = "new invoices\\zoho-invoice-simple-template.pdf"
output_path = "markdown_output\\zoho-invoice-simple-template.md"

# pdf_path = "invoices/invoice_08_scanned.pdf"
# output_path = "markdown_output/invoice_08_scanned_ocr.md"

# Convert PDF into Markdown
markdown_text = convert_pdf_to_markdown(
    pdf_path,
    output_path
)

# Display results
print("PDF converted successfully!")

print("Markdown characters:", len(markdown_text))

print("\nEXTRACTED MARKDOWN:")
print(markdown_text)
