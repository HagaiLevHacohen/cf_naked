import asyncio
import zendriver as zd
from zendriver.core.cloudflare import cf_is_interactive_challenge_present, verify_cf

async def main():
    browser = await zd.start(
        headless=False,
        browser_args=[
            "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36"
        ]
    )
    
    page = await browser.get("https://www.scrapingcourse.com/cloudflare-challenge")

    await asyncio.sleep(10)

    challenge_present = await cf_is_interactive_challenge_present(page, timeout=5)

    if challenge_present:
        print("Challenge detected")
        await verify_cf(
            page,
            click_delay=5,
            timeout=15,
            challenge_selector=None,
            flash_corners=False
        )
    else:
        print("No challenge detected")


    # Wait for page load
    await page.wait_for_ready_state(until='complete', timeout=10)

    headers = await page.evaluate("""
    (() => {
        return {
            ua: navigator.userAgent,
            lang: navigator.language,
            platform: navigator.platform
        };
    })()
    """)

    print(headers)

    # Extract cookies
    cookies = await browser.cookies.get_all()

    # Convert cookies to "name=value" format
    cookie_strings = [f"{c.name}={c.value}" for c in cookies]

    # Join them with "; " as separator
    cookies_line = "; ".join(cookie_strings)

    # Write to cookies.txt
    with open("cookies.txt", "w", encoding="utf-8") as f:
        f.write(cookies_line)

    await browser.stop()


if __name__ == '__main__':
    zd.loop().run_until_complete(main())