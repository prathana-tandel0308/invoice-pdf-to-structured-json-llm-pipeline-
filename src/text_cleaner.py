
import html
import re


def clean_markdown(markdown_text):

    # Decode HTML entities such as &#x20;
    markdown_text = html.unescape(markdown_text)

    # Normalize line endings
    markdown_text = markdown_text.replace("\r\n", "\n")

    # Remove unnecessary spaces at the end of lines
    markdown_text = "\n".join(
        line.rstrip() for line in markdown_text.split("\n")
    )

    # Reduce excessive blank lines to a maximum of two
    markdown_text = re.sub(r"\n{3,}", "\n\n", markdown_text)

    return markdown_text
