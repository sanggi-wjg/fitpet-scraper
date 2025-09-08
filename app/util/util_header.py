import random

from fake_useragent import UserAgent


def get_fake_headers() -> dict[str, str]:
    fake_ua = UserAgent()
    return {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9",
        "Accept-Language": get_fake_accept_language(),
        "Upgrade-Insecure-Requests": "1",
        "Referer": get_fake_referer(),
        "User-Agent": fake_ua.random,
    }


def get_fake_referer() -> str:
    return random.choice(
        [
            "https://google.com",
            "https://naver.com",
            "https://daum.net",
            "https://bing.com",
            "https://yahoo.com",
            "https://duckduckgo.com",
            "https://baidu.com",
            "https://ask.com",
            "https://zum.com",
            "https://nate.com",
            "https://reddit.com",
            "https://facebook.com",
            "https://twitter.com",
            "https://instagram.com",
            "https://linkedin.com",
            "https://youtube.com",
            "https://tistory.com",
            "https://medium.com",
            "https://quora.com",
            "https://wikipedia.org",
            "https://stackoverflow.com",
            "https://github.com",
            "https://pinterest.com",
        ]
    )


def get_fake_accept_language() -> str:
    return random.choice(
        [
            "ko,en-US;q=0.9,en;q=0.8",
            "en-US,en;q=0.9",
            "ja-JP,ja;q=0.9,en;q=0.8",
        ]
    )
