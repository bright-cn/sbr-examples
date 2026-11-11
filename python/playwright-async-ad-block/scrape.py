#!/usr/bin/env python3
import asyncio
from os import environ
from time import time
from playwright.async_api import async_playwright

AUTH = environ.get('AUTH', default='USER:PASS')
TARGET_URL = environ.get('TARGET_URL', default='https://www.w3schools.com/js/js_dates.asp')
AD_BLOCK = environ.get('AD_BLOCK', default='1')

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
            if AD_BLOCK == '1':
                print('Enabling AdBlock...')
                client = await page.context.new_cdp_session(page)
                await client.send('Unblocker.enableAdBlock')
                print('Enabled!')
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
