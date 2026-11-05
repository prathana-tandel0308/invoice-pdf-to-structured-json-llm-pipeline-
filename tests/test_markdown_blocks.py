
from pathlib import Path

from src.markdown_block_splitter import (
    split_markdown_into_blocks
)


# Read an existing cleaned invoice
input_file = Path(
    "cleaned_markdown/invoice_09_large.md"
)

if not input_file.exists():
    print("Invoice Markdown file not found!")
    raise SystemExit(1)


markdown_text = input_file.read_text(encoding="utf-8")


# Split Markdown into numbered blocks
blocks = split_markdown_into_blocks(markdown_text)


# Display the results
print(f"Total blocks found: {len(blocks)}\n")

for block_id, block_content in blocks.items():

    print(f"\n========== BLOCK {block_id} ==========\n")

    print(block_content)
