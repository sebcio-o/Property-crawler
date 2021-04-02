import re
from datetime import datetime

from .base import request

BASE = "https://nethouseprices.com"


def get_article_data(soup):

    url_and_price = soup.select_one(".price-main a")
    title = soup.select_one(".price-desc a")
    address = soup.select_one(".price-address")

    url = None
    price = None
    if url_and_price:
        url = BASE + url_and_price.get("href")
        url_and_price = url_and_price.text.strip()
        if "poa" in url_and_price.lower():
            price = 0
        else:
            price = eval(re.sub(r"\D", "", url_and_price))
    if title:
        title = title.text.strip()
    if address:
        address = address.text.strip()

    soup = request(url)

    date = soup.select_one(".listing-image-elem.listing-date")
    agent_name = soup.select_one("table:nth-child(2) img:nth-child(1)")
    agent_address = soup.select(
        "table:nth-child(2) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2) > div:nth-child(1) p"
    )
    agent_phone = soup.select_one(
        "div.content-section:nth-child(14) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > p:nth-child(4) > span:nth-child(3)"
    )
    description = soup.select(".property-main-description p")
    key_features = soup.select(".double-arrow-list li")

    if date:
        date = re.sub(r"(st|th|ed)", "", date.text.strip())
        date = datetime.strptime(date, "%d %B %Y")
    else:
        date = datetime.now()
    if agent_name:
        agent_name = agent_name.get("alt").replace("logo", "")
    if agent_phone:
        agent_phone = agent_phone.text
    if agent_address:
        agent_address = "".join([i.text + " " for i in agent_address])
    if description:
        description = "".join([i.text + " " for i in description]).strip()
    if key_features:
        key_features = [i.text for i in key_features]

    return [
        url,
        title,
        address,
        price,
        date,
        agent_name,
        agent_phone,
        agent_address,
        description,
        key_features,
    ]


def get_page_data(soup):

    results = []
    articles = soup.select(".address_bar.price-reduced-full")

    for article in articles:
        try:
            data = get_article_data(article)
            results.append(data)
        except Exception as e:
            print("WENT WRONG", e)

    return results


def crawl_nethouseprices(url: str):

    data = {
        "url": [],
        "title": [],
        "address": [],
        "price": [],
        "date": [],
        "agent_name": [],
        "agent_phone": [],
        "agent_address": [],
        "description": [],
        "key_features": [],
    }

    while True:
        soup = request(url)

        results = get_page_data(soup)
        for n, key in enumerate(data):
            data[key] += [j[n] for j in results]

        url = soup.find(attrs={"title": "Next Page"})
        if not url:
            break
        url = "http:/" + url.get("href")[1::]

    return data