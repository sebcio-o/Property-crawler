import re
from datetime import datetime

from .base import request

BASE = "https://nethouseprices.com"


def get_article_data(soup):

    url_and_address = soup.select_one(".street-details-head-row a")
    key_features = soup.select_one(".street-details-row")

    if not url_and_address:
        return

    url = BASE + url_and_address.get("href")
    address = url_and_address.text.strip()
    if key_features:
        key_features = key_features.text.split(", ")

    soup = request(url)

    title = soup.select_one(".address-header")
    description = soup.select_one(".property-details")
    agent_name = soup.select_one(".push-left > h5:nth-child(2) > a:nth-child(1)")
    agent_phone = soup.select_one(".revealNumber")
    agent_address = soup.select_one(".push-left > p")
    listing_history_dates = soup.select(".listing-table td:nth-child(1)")
    listing_history_values = soup.select(".listing-table td:nth-child(2)")

    if title:
        title = title.text.strip()
    if description:
        description = description.text.strip()
    if agent_name:
        agent_name = agent_name.text.strip()
    if agent_phone:
        agent_phone = agent_phone.text.strip()
    if agent_address:
        agent_address = [i + " " for i in agent_address]
    if listing_history_dates and listing_history_values:
        listing_history = [
            [i.text, j.text]
            for i, j in zip(listing_history_dates, listing_history_values)
        ]

    return [
        url,
        title,
        address,
        agent_name,
        agent_phone,
        agent_address,
        description,
        key_features,
        listing_history,
    ]


def get_page_data(soup):

    results = []
    articles = soup.select(".sold_price_row")

    for article in articles:
        try:
            data = get_article_data(article)
            results.append(data)
        except Exception as e:
            print("WENT WRONG", e)

    return results


def crawl_nethouseprices_archive(url: str):

    data = {
        "url": [],
        "title": [],
        "address": [],
        "agent_name": [],
        "agent_phone": [],
        "agent_address": [],
        "description": [],
        "key_features": [],
        "listing_history": [],
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