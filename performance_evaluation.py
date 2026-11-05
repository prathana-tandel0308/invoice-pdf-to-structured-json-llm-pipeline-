
import json
from pathlib import Path

from src.token_counter import count_tokens, calculate_token_reduction


# Input folders
full_text_folder = Path("cleaned_markdown")
filtered_text_folder = Path("filtered_text")

# Output file
results_folder = Path("performance_results")
results_folder.mkdir(parents=True, exist_ok=True)

results_file = results_folder / "token_comparison.json"


# Find Markdown files
full_files = sorted(full_text_folder.glob("*.md"))

print("\n========== PERFORMANCE EVALUATION ==========")

if not full_files:
    raise FileNotFoundError(
        "No Markdown files found in cleaned_markdown."
    )


total_full_tokens = 0
total_filtered_tokens = 0

invoice_results = []


for full_file in full_files:

    filtered_file = filtered_text_folder / full_file.name

    print(f"\nInvoice: {full_file.name}")
    print("-" * 45)

    if not filtered_file.exists():
        print("Filtered Markdown not found. Skipping.")
        continue

    # Read full cleaned Markdown
    full_text = full_file.read_text(encoding="utf-8")

    # Read filtered Markdown
    filtered_text = filtered_file.read_text(encoding="utf-8")

    # Count tokens
    full_tokens = count_tokens(full_text)
    filtered_tokens = count_tokens(filtered_text)

    # Calculate reduction
    reduction = calculate_token_reduction(
        full_tokens,
        filtered_tokens
    )

    # Update totals
    total_full_tokens += full_tokens
    total_filtered_tokens += filtered_tokens

    invoice_results.append({
        "invoice": full_file.name,
        "full_markdown_tokens": full_tokens,
        "filtered_markdown_tokens": filtered_tokens,
        "tokens_saved": full_tokens - filtered_tokens,
        "token_reduction_percentage": reduction
    })

    print(f"Full Markdown tokens:     {full_tokens}")
    print(f"Filtered Markdown tokens: {filtered_tokens}")
    print(f"Tokens saved:             {full_tokens - filtered_tokens}")
    print(f"Token reduction:          {reduction}%")


# Overall reduction
overall_reduction = calculate_token_reduction(
    total_full_tokens,
    total_filtered_tokens
)

total_tokens_saved = total_full_tokens - total_filtered_tokens


# Final report
print("\n========== OVERALL PERFORMANCE ==========")

print(f"Total invoices processed: {len(invoice_results)}")
print(f"Full Markdown tokens:     {total_full_tokens}")
print(f"Filtered Markdown tokens: {total_filtered_tokens}")
print(f"Total tokens saved:       {total_tokens_saved}")
print(f"Overall token reduction:  {overall_reduction}%")


# Save results
report = {
    "total_invoices": len(invoice_results),
    "full_markdown_tokens": total_full_tokens,
    "filtered_markdown_tokens": total_filtered_tokens,
    "tokens_saved": total_tokens_saved,
    "overall_token_reduction_percentage": overall_reduction,
    "invoice_results": invoice_results
}

results_file.write_text(
    json.dumps(report, indent=4),
    encoding="utf-8"
)

print(f"\nPerformance report saved to: {results_file}")
