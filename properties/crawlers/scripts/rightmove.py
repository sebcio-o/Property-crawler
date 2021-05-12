import re
from datetime import datetime

from .base import request

BASE = "https://www.rightmove.co.uk"


def get_article_data(soup):

    url = soup.select_one(".propertyCard-link")
    head_image = soup.select_one(".propertyCard-img img")
    title = soup.select_one(".propertyCard-title")
    price = soup.select_one(".propertyCard-priceValue")
    address = soup.select_one(".propertyCard-address")
    date = soup.select_one(".propertyCard-branchSummary-addedOrReduced")
    agent_name = soup.select_one(
        ".propertyCard-branchLogo .propertyCard-branchLogo-link"
    )
    agent_phone = soup.select_one(".propertyCard-contactsPhoneNumber")

    if url:
        url = BASE + url.get("href")
    if head_image:
        head_image = head_image.get("src")
    if title:
        title = title.text.strip()
    if price:
        if "POA" in price:
            price = 0
        else:
            price = eval(re.sub(r"\D", "", price.text.strip()))
    if address:
        address = address.text.strip()
    if (date := re.match(r"(\d{2}\/\d{2}\/\d{4})", str(date))) :
        date = date.group()[0]
        date = datetime.strptime(date, "%d/%m/%Y")
    else:
        date = datetime.now()
    if agent_name:
        agent_name = agent_name.get("title")
    if agent_phone:
        agent_phone = agent_phone.text.strip()

    soup = request(url)

    agent_address = None
    key_features = None
    description = None
    property_type = None
    bedrooms = None
    bathrooms = None
    sqft = None
    if "/properties/" in url:
        main_informations = soup.select("._1u12RxIYGx3c84eaGxI6_b")
        agent_address = soup.select_one(".OojFk4MTxFDKIfqreGNt0")
        key_features = soup.select_one("._1uI3IvdF5sIuBtRIvKrreQ")
        description = soup.select_one("div.OD0O7FWw1TjbTD4sdRi1_ > div > div")

        for el in main_informations:
            info_title = el.select_one(".tmJOVKTrHAB4bLpcMjzQ")
            info_data = el.select_one("._1fcftXUEbWfJOJzIUeIHKt")
            if "PROPERTY TYPE" in info_title:
                property_type = info_data.text.strip()
            elif "BEDROOMS" in info_title:
                bedrooms = int(info_data.text.strip().replace("x", ""))
            elif "BATHROOMS" in info_title:
                bathrooms = int(info_data.text.strip().replace("x", ""))
            elif "SIZE" in info_title:
                sqft = int(re.sub(r"\D", "", info_data.text.strip()))

        if agent_address:
            agent_address = agent_address.get("title").replace("\n", " ")
        if key_features:
            key_features = [
                i.text for i in key_features.select(".lIhZ24u1NHMa5Y6gDH90A")
            ]
        if description:
            description = description.text.strip()

    return [
        url,
        head_image,
        title,
        address,
        price,
        date,
        agent_name,
        agent_phone,
        agent_address,
        property_type,
        bedrooms,
        bathrooms,
        sqft,
        key_features,
        description,
    ]


def get_page_data(soup):

    results = []
    articles = soup.select(".propertyCard-wrapper")

    for article in articles:
        try:
            data = get_article_data(article)
            results.append(data)
        except Exception as e:
            print("WENT WRONG", e)

    return results


def get_page_number(soup):

    result_count = soup.select_one(".searchHeader-resultCount")
    number_of_pages = int(result_count.text.replace(",", ""))
    page_number = number_of_pages // 24

    if number_of_pages / 24 % 1 != 0:
        page_number += 1
    if page_number > 42:
        page_number = 41

    return page_number


def crawl_rightmove(start_url: str):

    data = []

    soup = request(start_url)
    data += get_page_data(soup)
    page_number = get_page_number(soup)

    for i in range(0, page_number + 1):

        url = f"{start_url}&index={i*24}"
        soup = request(url)
        data += get_page_data(soup)

    return data