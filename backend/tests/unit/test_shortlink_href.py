from __future__ import annotations

import html

import pytest

from jetlag.api.routes.shortlinks import safe_href_for_html


@pytest.mark.parametrize(
    ("url", "expected"),
    [
        ("javascript:alert(1)", "#"),
        ("JAVASCRIPT:alert(1)", "#"),
        ("data:text/html,<script>bad</script>", "#"),
        ("http://example.com/", "#"),
        ("https://example.com/path?q=a&b=1", None),
        ("myapp://open/foo", None),
    ],
)
def test_safe_href_for_html_scheme(url: str, expected: str | None) -> None:
    out = safe_href_for_html(url)
    if expected is not None:
        assert out == expected
    else:
        assert out == html.escape(url, quote=True)
    assert not out.lower().startswith("javascript:")
    assert 'href="javascript' not in f'<a href="{out}">'
