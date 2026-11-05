
import json
from pathlib import Path

from src.pdf_extractor import convert_pdf_to_markdown
from src.text_cleaner import clean_markdown
from src.local_llm_filter import (
    filter_invoice_markdown,
    save_filtered_markdown
)
from src.token_counter import (
    count_tokens,
    calculate_token_reduction
)
from src.llm_extractor import extract_invoice_data


# Input and output folders
input_folder = Path("new invoices")
output_folder = Path("markdown_output")
cleaned_folder = Path("cleaned_markdown")
filtered_folder = Path("filtered_text")
json_folder = Path("json_output")


# Create output folders if they do not exist
output_folder.mkdir(parents=True, exist_ok=True)
cleaned_folder.mkdir(parents=True, exist_ok=True)
filtered_folder.mkdir(parents=True, exist_ok=True)
json_folder.mkdir(parents=True, exist_ok=True)


# Find all PDF files
pdf_files = sorted(input_folder.glob("*.pdf"))

print(f"Found {len(pdf_files)} PDF files.\n")


# Total token counts
total_original_tokens = 0
total_cleaned_tokens = 0
total_filtered_tokens = 0


# Process each invoice
for pdf_file in pdf_files:

    print("\n" + "=" * 55)
    print(f"PROCESSING: {pdf_file.name}")
    print("=" * 55)

    # STEP 1: Convert PDF into Markdown
    markdown_text = convert_pdf_to_markdown(
        str(pdf_file),
        str(output_folder / f"{pdf_file.stem}.md")
    )

    # STEP 2: Count original Markdown tokens
    original_tokens = count_tokens(markdown_text)
    total_original_tokens += original_tokens

    # STEP 3: Clean Markdown
    cleaned_text = clean_markdown(markdown_text)

    # Save cleaned Markdown
    cleaned_file = cleaned_folder / f"{pdf_file.stem}.md"

    cleaned_file.write_text(
        cleaned_text,
        encoding="utf-8"
    )

    # STEP 4: Count cleaned Markdown tokens
    cleaned_tokens = count_tokens(cleaned_text)
    total_cleaned_tokens += cleaned_tokens

    # STEP 5: Send cleaned Markdown to local Llama
    print("\nSending invoice to local Llama 3.2...")

    filtered_text = filter_invoice_markdown(cleaned_text)

    # STEP 6: Save filtered Markdown
    filtered_file = save_filtered_markdown(
        filtered_text,
        filtered_folder / f"{pdf_file.stem}.md"
    )

    # STEP 7: Count filtered Markdown tokens
    filtered_tokens = count_tokens(filtered_text)
    total_filtered_tokens += filtered_tokens

    # STEP 8: Send filtered Markdown to Gemini
    print("\nSending filtered invoice to Gemini...")

    invoice_data = extract_invoice_data(filtered_text)

    # STEP 9: Save extracted invoice data as JSON
    json_file = json_folder / f"{pdf_file.stem}.json"

    json_file.write_text(
        json.dumps(
            invoice_data.model_dump(mode="json"),
            indent=4,
            ensure_ascii=False
        ),
        encoding="utf-8"
    )

    # Calculate token reduction
    reduction = calculate_token_reduction(
        cleaned_tokens,
        filtered_tokens
    )

    # Display invoice results
    print("\n========== INVOICE SUMMARY ==========")

    print(f"Original tokens:       {original_tokens}")
    print(f"Cleaned tokens:        {cleaned_tokens}")
    print(f"Filtered tokens:       {filtered_tokens}")
    print(f"Filtering reduction:   {reduction}%")

    print(f"\nSaved Markdown: {cleaned_file}")
    print(f"Saved filtered text: {filtered_file}")
    print(f"Saved JSON: {json_file}")

    print("\nEXTRACTED INVOICE DATA")
    print("=====================")
    print(invoice_data.model_dump(mode="json"))


# Calculate overall token reduction
overall_reduction = calculate_token_reduction(
    total_cleaned_tokens,
    total_filtered_tokens
)


# Display final summary
print("\n" + "=" * 55)
print("ALL INVOICES PROCESSED!")
print("=" * 55)

print(f"Total PDFs:              {len(pdf_files)}")
print(f"Total original tokens:   {total_original_tokens}")
print(f"Total cleaned tokens:    {total_cleaned_tokens}")
print(f"Total filtered tokens:   {total_filtered_tokens}")
print(f"Overall filtering reduction: {overall_reduction}%")

print(f"\nJSON files saved in: {json_folder}")
