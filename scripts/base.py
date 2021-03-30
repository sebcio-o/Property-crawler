from bs4 import BeautifulSoup
from fake_headers import Headers
from requests_html import HTMLSession
from time import sleep

headers = Headers(headers=True, os="win")
session = HTMLSession()


def request(url: str):
    sleep(2)
    print(url)
    r = session.get(url, headers=headers.generate())
    r.html.render(timeout=20)
    return BeautifulSoup(r.html.html, "html.parser")
