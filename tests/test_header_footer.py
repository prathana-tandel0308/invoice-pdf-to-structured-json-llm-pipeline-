
from pathlib import Path

from src.header_footer_remover import remove_repeated_headers_footers


input_file = Path("cleaned_markdown/invoice_09_large.md")
output_file = Path("cleaned_markdown/invoice_09_large_no_headers.md")

# Read the existing cleaned Markdown
markdown_text = input_file.read_text(encoding="utf-8")

# Remove repeated headers and footers
cleaned_text = remove_repeated_headers_footers(markdown_text)

# Save the result separately
output_file.write_text(cleaned_text, encoding="utf-8")

print("Header and footer removal completed!")
print(f"Original characters: {len(markdown_text)}")
print(f"Updated characters: {len(cleaned_text)}")
print(f"Saved to: {output_file}")
