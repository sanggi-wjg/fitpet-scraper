import pytest

from app.util.util_string import clean_html_tags


class TestUtilString:

    @pytest.mark.parametrize(
        "given_text,expected",
        [
            pytest.param("<a href='https://dev.com'>dev.com</a>", "dev.com"),
            pytest.param('<div class="iam-class"\>what</a>', "what"),
            pytest.param("", ""),
        ],
    )
    def test_clean_html_tags(self, given_text: str, expected: str):
        assert clean_html_tags(given_text) == expected
