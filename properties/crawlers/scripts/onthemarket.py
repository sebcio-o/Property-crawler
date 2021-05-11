import re
import json

from datetime import datetime

from .base import request

BASE = "https://www.onthemarket.com"


def get_article_data(soup):

    url_and_price = soup.select_one("div.details.gradient p.price-text a.price")
    head_image = soup.select_one(".lazyload-wrapper img")
    title = soup.select_one(".title a")
    address = soup.select_one(".address a")
    agent_name = soup.select_one(".agent .marketed-by .marketed-by-link")
    agent_phone = soup.select_one(".marketed-by-contact .call strong")

    url = None
    price = None
    if url_and_price:
        url = BASE + url_and_price.get("href")
        url_and_price = url_and_price.text.strip()
        if url_and_price == "":
            price = 0
        else:
            price = int(re.sub(r"\D", "", url_and_price))
    if head_image:
        head_image = head_image.get("src")
    if title:
        title = title.text.strip()
    if address:
        address = address.text.strip()
    if agent_name:
        agent_name = agent_name.text.strip()
    if agent_phone:
        agent_phone = agent_phone.text.strip()

    soup = request(url)

    agent_address = soup.select_one(".agent-info-address")
    description = soup.select(".description") + soup.select(".property-description")
    key_features = soup.select(".property-features li")
    stations = soup.select(".poi-name") + soup.select(".station-data-row")

    if agent_address:
        agent_address = agent_address.text.strip()
    if description:
        description = "".join([i.text + " " for i in description])
    if key_features:
        key_features = [i.text for i in key_features]
    if stations:
        stations = [i.text.strip() for i in stations]

    return [
        url,
        head_image,
        title,
        address,
        price,
        datetime.now(),
        agent_name,
        agent_phone,
        agent_address,
        description,
        key_features,
        stations,
    ]


def get_page_data(soup):

    results = []
    articles = soup.select("#properties.list-tabcontent .result.property-result.panel")
    for article in articles:
        if article.select_one(".exclusive-banner-text"):
            continue
        try:
            data = get_article_data(article)
            results.append(data)
        except Exception as e:
            print("ONTHEMARKET GOES BRRR...", e, article)

    return results


def crawl_onthemarket(url: str):

    data = []

    while True:
        soup = request(url)

        data += get_page_data(soup)

        url = soup.find("a", {"title": "Next page"})
        if not url:
            break

        url = BASE + url.get("href")

    return data