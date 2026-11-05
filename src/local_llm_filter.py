
from pathlib import Path
import re

import ollama

from config.settings import (
    LOCAL_LLM_MODEL,
    OLLAMA_HOST
)

from src.prompt_builder import build_local_filter_prompt
from src.markdown_block_splitter import split_markdown_into_blocks


# Connect to the local Ollama server
client = ollama.Client(host=OLLAMA_HOST)


# Number of blocks sent to Llama in each request
BATCH_SIZE = 12


def get_block_batches(numbered_blocks, batch_size):
    """
    Divide Markdown blocks into smaller batches.
    """

    block_items = list(numbered_blocks.items())

    batches = []

    for start in range(0, len(block_items), batch_size):

        batch_items = block_items[
            start:start + batch_size
        ]

        batches.append(dict(batch_items))

    return batches


def get_selected_block_ids(response_text, valid_ids):
    """
    Extract valid block IDs from Llama's response.
    """

    selected_ids = re.findall(
        r"(?m)^\s*(?:BLOCK\s*)?(\d{3})\s*$",
        response_text,
        flags=re.IGNORECASE
    )

    return {
        block_id
        for block_id in selected_ids
        if block_id in valid_ids
    }


def ask_llama(prompt):
    """
    Send a prompt to Llama and return its response.
    """

    response = client.chat(
        model=LOCAL_LLM_MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        options={
            "temperature": 0
        }
    )

    return response.message.content.strip()


def ask_llama_to_select_blocks(batch, batch_number):
    """
    Ask Llama to select relevant blocks from one batch.
    """

    prompt = build_local_filter_prompt(batch)

    print(f"\nProcessing batch {batch_number}...")
    print(f"Blocks in this batch: {len(batch)}")

    response_text = ask_llama(prompt)

    print("\nLlama response:")
    print(response_text)

    valid_ids = set(batch.keys())

    if response_text.upper() == "NONE":
        return set()

    selected_ids = get_selected_block_ids(
        response_text,
        valid_ids
    )

    # Retry once if Llama does not return valid IDs
    if not selected_ids:

        print("\nNo valid block IDs found. Retrying...")

        retry_prompt = prompt + """

IMPORTANT CORRECTION:

Return ONLY valid block IDs from the current input.

Use one ID per line.

Do not summarize or extract invoice information.

If no relevant blocks exist, return exactly:

NONE
"""

        response_text = ask_llama(retry_prompt)

        print("\nLlama retry response:")
        print(response_text)

        if response_text.upper() == "NONE":
            return set()

        selected_ids = get_selected_block_ids(
            response_text,
            valid_ids
        )

    if not selected_ids:
        raise ValueError(
            f"Llama failed to return valid block IDs "
            f"for batch {batch_number}."
        )

    return selected_ids


def filter_invoice_markdown(markdown_text):
    """
    Filter invoice Markdown using one selection pass.

    Llama selects relevant block IDs.
    Python reconstructs the original Markdown blocks.
    """

    # Step 1: Split Markdown into numbered blocks
    numbered_blocks = split_markdown_into_blocks(
        markdown_text
    )

    if not numbered_blocks:
        raise ValueError("No Markdown blocks were found.")

    print(f"Total original blocks: {len(numbered_blocks)}")

    # Step 2: Divide blocks into batches
    batches = get_block_batches(
        numbered_blocks,
        BATCH_SIZE
    )

    print(f"Total batches: {len(batches)}")

    # Step 3: Select relevant blocks
    all_selected_ids = set()

    for batch_number, batch in enumerate(batches, start=1):

        selected_ids = ask_llama_to_select_blocks(
            batch,
            batch_number
        )

        all_selected_ids.update(selected_ids)

        print(
            f"Selected blocks in batch {batch_number}: "
            f"{len(selected_ids)}"
        )

    # Step 4: Reconstruct Markdown from original blocks
    filtered_blocks = []

    for block_id, block_content in numbered_blocks.items():

        if block_id in all_selected_ids:
            filtered_blocks.append(
                block_content.rstrip("\n")
            )

    filtered_text = "\n\n".join(filtered_blocks)

    # Restore final newline if present in original Markdown
    if markdown_text.endswith("\n") and filtered_text:
        filtered_text += "\n"

    # Step 5: Display summary
    print("\n========== FILTERING SUMMARY ==========")

    print(f"Original blocks: {len(numbered_blocks)}")
    print(f"Selected blocks: {len(all_selected_ids)}")
    print(f"Total batches: {len(batches)}")

    return filtered_text


def save_filtered_markdown(filtered_text, output_path):
    """
    Save selected original Markdown blocks.
    """

    output_file = Path(output_path)

    output_file.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    output_file.write_text(
        filtered_text,
        encoding="utf-8"
    )

    return output_file
