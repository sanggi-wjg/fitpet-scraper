import re
from html import unescape


def clean_html_tags(text: str) -> str:
    if not text:
        return ""

    clean_text = re.sub(r"<[^>]+>", "", text)
    clean_text = unescape(clean_text)
    clean_text = re.sub(r"\s+", " ", clean_text)
    return clean_text.strip()
