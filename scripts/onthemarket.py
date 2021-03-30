import re
from datetime import datetime

from .base import request

BASE = "https://www.onthemarket.com"


def get_article_data(soup):

    url_and_price = soup.select_one("div.details.gradient p.price-text a.price")
    title = soup.select_one(".title a")
    address = soup.select_one(".address a")
    agent_name = soup.select_one(".agent .marketed-by .marketed-by-link")
    agent_phone = soup.select_one(".marketed-by-contact .call strong")

    url = None
    price = None
    if url_and_price:
        url = BASE + url_and_price.get("href")
        url_and_price = url_and_price.text.strip()
        if "" in url_and_price.lower():
            price = 0
        else:
            price = eval(re.sub(r"\D", "", url_and_price))
    if title:
        title = title.text.strip()
    if address:
        address = address.text.strip()
    if agent_name:
        agent_name = agent_name.text.strip()
    if agent_phone:
        agent_phone = agent_phone.text.strip()

    soup = request(url)

    key_features = soup.select(".property-features li")
    agent_address = soup.select(".agent-info-address") + soup.select(".agent-address")
    description = soup.select(".description") + soup.select(".property-description")
    stations = soup.select(".poi-name") + soup.select(".station-data-row")

    if agent_address:
        agent_address = "".join([i.text + " " for i in agent_address])
    if description:
        description = "".join([i.text + " " for i in description])
    if key_features:
        key_features = [i.text for i in key_features]
    if stations:
        stations = [i.text.strip() for i in stations]

    return [
        url,
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
        except:
            print("ONTHEMARKET GOES BRRR...", article)

    return results


def crawl_onthemarket(url: str):

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
        "stations": [],
    }

    while True:
        soup = request(url)

        results = get_page_data(soup)
        for i, key in enumerate(data):
            data[key] += [j[i] for j in results]

        url = soup.find("a", {"title": "Next page"})
        if not url:
            break

        url = BASE + url.get("href")

    return data


if __name__ == "__main__":
    import pandas as pd

    URL = ""
    data = crawl_onthemarket(URL)
    df = pd.DataFrame.from_dict(data)
    df.to_excel("onthemarket.xlsx")