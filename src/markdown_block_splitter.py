
import re


def split_markdown_into_blocks(markdown_text):
    """
    Split Markdown into blocks while preserving
    the original content of each block.
    """

    blocks = []

    lines = markdown_text.splitlines(keepends=True)

    current_block = []
    inside_table = False

    for line in lines:

        stripped_line = line.strip()

        # Detect Markdown table rows
        is_table_row = (
            stripped_line.startswith("|")
            and stripped_line.endswith("|")
        )

        if is_table_row:

            if current_block and not inside_table:
                blocks.append("".join(current_block))
                current_block = []

            inside_table = True
            current_block.append(line)

        else:

            if inside_table:
                blocks.append("".join(current_block))
                current_block = []
                inside_table = False

            if stripped_line == "":
                if current_block:
                    blocks.append("".join(current_block))
                    current_block = []

            else:
                current_block.append(line)

    # Save the final block
    if current_block:
        blocks.append("".join(current_block))

    # Assign unique IDs
    numbered_blocks = {}

    for index, block in enumerate(blocks, start=1):
        block_id = f"{index:03d}"
        numbered_blocks[block_id] = block

    return numbered_blocks
