#!/usr/bin/env python3
from os import environ
from time import time
from selenium.webdriver import Remote, ChromeOptions as Options
from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection as Connection

AUTH = environ.get('AUTH', 'USER:PASS')
TARGET_URL = environ.get('TARGET_URL', 'https://www.w3schools.com/js/js_dates.asp')
BLOCK_MEDIA = environ.get('BLOCK_MEDIA', '1')

# URL patterns to block for bandwidth savings.
BLOCKED_URLS = [
    '*.png', '*.jpg', '*.jpeg',
]


def scrape(url=TARGET_URL):
    if AUTH == 'USER:PASS':
        raise Exception(
            'Provide Scraping Browsers credentials in AUTH '
            'environment variable or update the script.'
        )

    print('Connecting to Browser...')
    server = f'https://{AUTH}@brd.superproxy.io:9515'
    connection = Connection(server, 'goog', 'chrome')
    driver = Remote(connection, options=Options())
    try:
        begin = time()
        print('Connected!')
        result = driver.execute_cdp_cmd('Browser.getSessionId', {})
        session_id = result['sessionId']
        print('Current session ID:', session_id)
        if BLOCK_MEDIA == '1':
            print(f'Blocking {len(BLOCKED_URLS)} URL patterns to save bandwidth...')
            driver.execute_cdp_cmd('Network.enable', {})
            driver.execute_cdp_cmd('Network.setBlockedURLs', {'urls': BLOCKED_URLS})
            print('Blocking enabled!')

        print(f'Navigating to {url}...')
        driver.get(url)

        data = driver.page_source
        elapsed = int((time() - begin) * 1000)
        print(f'Done! Time: {elapsed}')
        return data

    finally:
        driver.quit()


if __name__ == '__main__':
    try:
        scrape()
    except Exception as error:
        print(error)
        raise SystemExit(1)
