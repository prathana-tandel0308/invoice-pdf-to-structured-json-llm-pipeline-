
import tiktoken


# Load the OpenAI tokenizer
encoding = tiktoken.get_encoding("cl100k_base")


def count_tokens(text):
    """
    Count the number of tokens in a text.
    """
    return len(encoding.encode(text))


def count_tokens_in_file(file_path):
    """
    Read a Markdown file and count its tokens.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        text = file.read()

    return count_tokens(text)


def calculate_token_reduction(original_tokens, filtered_tokens):
    """
    Calculate token reduction percentage.
    """

    if original_tokens == 0:
        return 0

    reduction = (
        (original_tokens - filtered_tokens)
        / original_tokens
    ) * 100

    return round(reduction, 2)
