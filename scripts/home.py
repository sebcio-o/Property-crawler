import re
from datetime import datetime

from .base import request

BASE = "https://www.home.co.uk/"


def get_article_data(soup):

    price = soup.select_one(".property-listing__price")
    title = soup.select_one(".property-listing__type")
    address = soup.select_one(".house_link")
    description = soup.select_one(".property-listing__desc")
    key_features = soup.select(".property-listing__info li")

    if price:
        price = price.text.strip()
        if "poa" in price.lower():
            price = 0
        else:
            price = eval(re.sub(r"\D", "", price))

    if title:
        title = title.text.strip().lower()
        property_type = re.sub(
            r"\b\d+\b", "", title.replace("bed", "").replace("s", "").strip()
        )
        if "bed" in title:
            bedrooms = eval(re.sub(r"\D", "", title))
        elif "studio" in title:
            bedrooms = 1
    else:
        bedrooms = None
        property_type = None

    if address:
        url = address.get("href")
        address = address.text.strip()
    else:
        url = None
    if description:
        description = description.text.strip()
    if key_features:
        key_features = [i.text for i in key_features]

    soup = request(url)
    url = soup.select_one("#link")

    if url:
        url = url.get("href")

    return [
        url,
        title,
        address,
        price,
        bedrooms,
        property_type,
        description,
        key_features,
    ]


def get_page_data(soup):

    results = []
    articles = soup.select(".property-listing-container")

    for article in articles:
        try:
            data = get_article_data(article)
            results.append(data)
        except Exception as e:
            print("WENT WRONG", e)

    return results


def get_pages_number(soup):

    results_number = soup.select_one(
        ".homeco_pr_content > p:nth-child(1) > span:nth-child(1)"
    )
    if results_number:
        pages_number = int(results_number.text.strip().replace("\n", "")) / 10
        if pages_number % 10 != 0:
            pages_number += 1
        if pages_number > 50:
            pages_number = 50
        return int(pages_number)
    else:
        return 1


def crawl_home(url: str):

    data = {
        "url": [],
        "title": [],
        "address": [],
        "price": [],
        "bedrooms": [],
        "property_type": [],
        "description": [],
        "key_features": [],
    }

    soup = request(url)
    number_of_pages = get_pages_number(soup)

    for i in range(1, number_of_pages + 1):

        print(url)

        results = get_page_data(soup)
        for n, key in enumerate(data):
            data[key] += [j[n] for j in results]

        if not url:
            break
        url = f"{url}&page{i}"

    return data