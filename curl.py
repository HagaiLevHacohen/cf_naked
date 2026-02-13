"""
Requires cookies from the browser. create cookies.txt.
"""

import os
import sys
from pathlib import Path
from curl_cffi import requests


def parse_cookies(cookie_header: str) -> dict[str, str]:
    """Parse 'name=value; name2=value2' into a dict. Handles values containing '='."""
    cookies = {}
    for part in cookie_header.split("; "):
        part = part.strip()
        if not part:
            continue
        if "=" in part:
            name, _, value = part.partition("=")
            cookies[name.strip()] = value.strip()
    return cookies


def main() -> None:
    url = "https://www.scrapingcourse.com/cloudflare-challenge"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Cache-Control": "max-age=0",
        "Upgrade-Insecure-Requests": "1",
        "Sec-CH-UA": '"Not:A-Brand";v="99", "Google Chrome";v="145", "Chromium";v="145"',
        "Sec-CH-UA-Mobile": "?0",
        "Sec-CH-UA-Platform": '"Windows"',
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
    }


    cookie_str = Path("cookies.txt").read_text(encoding="utf-8").strip()

    if not cookie_str:
        print(
            "create cookies.txt",
            file=sys.stderr,
        )
        sys.exit(1)

    cookies = parse_cookies(cookie_str)

    print(cookies)

    with requests.Session(impersonate="chrome") as session:
        resp = session.get(
            url,
            headers=headers,
            cookies=cookies,
            timeout=30,
        )

    print(f"Status: {resp.status_code}")


if __name__ == "__main__":
    main()