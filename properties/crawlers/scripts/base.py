import logging
import os
from datetime import date
from time import sleep

from bs4 import BeautifulSoup
from fake_headers import Headers
from requests_html import HTMLSession

headers = Headers(headers=True, os="win")
session = HTMLSession()


def request(url: str):
    while True:
        try:
            sleep(10)
            logging.info(f"SENDING REQUEST {url}")
            r = session.get(url, headers=headers.generate())
            r.html.render(timeout=20)
            return BeautifulSoup(r.html.html, "html.parser")
        except Exception as e:
            logging.critical(f"SMTH WENT WRONG {e} {url}")
            sleep(20)