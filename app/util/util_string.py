import re
from html import unescape
from urllib.parse import urlparse


def clean_html_tags(text: str) -> str:
    if not text:
        return ""

    clean_text = re.sub(r"<[^>]+>", "", text)
    clean_text = unescape(clean_text)
    clean_text = re.sub(r"\s+", " ", clean_text)
    return clean_text.strip()


def extract_product_id_from_pet_friends_product_detail_url(url: str) -> str:
    parsed_url = urlparse(url)
    path = parsed_url.path
    match = re.search(r"/product/detail/(\d+)", path)

    if match:
        return match.group(1)
    else:
        raise ValueError(f"URL에서 product_id를 찾을 수 없습니다: {url}")
