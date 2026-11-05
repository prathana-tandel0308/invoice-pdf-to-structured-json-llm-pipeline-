
from pathlib import Path

from src.llm_extractor import extract_invoice_data


# Select one filtered Markdown file
filtered_file = Path("filtered_text/invoice_01_simple.md")

# Read Markdown
markdown_text = filtered_file.read_text(encoding="utf-8")

# Extract invoice information using Gemini
invoice_data = extract_invoice_data(markdown_text)

# Display extracted information
print("\nGEMINI EXTRACTED INVOICE DATA")
print("=============================")

print(invoice_data.model_dump(mode="json"))
