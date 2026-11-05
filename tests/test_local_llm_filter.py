
from pathlib import Path

from src.local_llm_filter import (
    filter_invoice_markdown,
    save_filtered_markdown
)


# Input Markdown file
input_file = Path("cleaned_markdown/invoice_05_complex_calculations.md")

# Output Markdown file
output_file = Path("filtered_text/invoice_05_complex_calculations.md")


# Check whether the input file exists
if not input_file.exists():
    print("Input Markdown file not found!")
    raise SystemExit(1)


print("Reading invoice Markdown...")

# Read the cleaned Markdown
markdown_text = input_file.read_text(encoding="utf-8")


print("Sending invoice to Llama 3.2...")
print("Please wait...\n")

# Filter relevant invoice evidence
filtered_text = filter_invoice_markdown(markdown_text)


# Save the filtered Markdown
saved_file = save_filtered_markdown(
    filtered_text,
    output_file
)


print("Local LLM filtering completed!")
print(f"Filtered file saved: {saved_file}")

print("\nFiltered invoice evidence:\n")
print(filtered_text)
