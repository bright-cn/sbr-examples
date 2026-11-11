#!/usr/bin/env python3
import asyncio
from os import environ
from time import time
from playwright.async_api import async_playwright

AUTH = environ.get('AUTH', default='USER:PASS')
TARGET_URL = environ.get('TARGET_URL', default='https://www.w3schools.com/js/js_dates.asp')
BLOCK_MEDIA = environ.get('BLOCK_MEDIA', default='1')

# Resource types to block for bandwidth savings.
BLOCKED = ['image', 'media', 'font', 'stylesheet']


async def scrape(url=TARGET_URL):
    if AUTH == 'USER:PASS':
        raise Exception('Provide Scraping Browsers credentials in AUTH '
                        'environment variable or update the script.')
    print('Connecting to Browser...')
    browser_ws_endpoint = f'wss://{AUTH}@brd.superproxy.io:9222'
    async with async_playwright() as playwright:
        browser = await playwright.chromium.connect_over_cdp(browser_ws_endpoint)
        try:
            begin = time()
            print('Connected!')
            page = await browser.new_page()
            client = await page.context.new_cdp_session(page)
            result = await client.send('Browser.getSessionId')
            session_id = result['sessionId']
            print('Current session ID:', session_id)

            if BLOCK_MEDIA == '1':
                print(f'Blocking {", ".join(BLOCKED)} to save bandwidth...')
                # Intercept all requests
                async def handle_route(route):
                    if route.request.resource_type in BLOCKED:
                        await route.abort()
                    else:
                        await route.continue_()
                await page.route('**/*', handle_route)
                print('Media blocking enabled!')

            print(f'Navigating to {url}...')
            await page.goto(url, timeout=2 * 60 * 1000)

            data = await page.content()
            elapsed = time() - begin
            print(f'Done! Time: {elapsed}')
            return data

        finally:
            await browser.close()


if __name__ == '__main__':
    asyncio.run(scrape())
