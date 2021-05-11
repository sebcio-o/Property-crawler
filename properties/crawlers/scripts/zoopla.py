import re
from datetime import datetime

from .base import request

BASE = "https://www.zoopla.co.uk"

PROPERTY_TYPES = {
    "setached house",
    "semi-detached house",
    "terraced house",
    "bungalow",
    "detached bungalow",
    "semi-detached bungalow",
    "terraced bungalow",
    "cottage",
    "mobile/park home",
    "flat",
    "farm",
    "land",
}


def get_article_data(soup):

    url = soup.select_one(".e2uk8e4.e33dvwd0")
    head_image = soup.select_one(
        ".e2uk8e1.css-v3r7g4-StyledImg-Image-CustomStyledImage.e1kasqha0"
    )
    title = soup.select_one(".css-qwtjnc-Heading2-StyledAddress.e2uk8e14")
    price = soup.select_one(".css-6v9gpl-Text.eczcs4p0")
    address = soup.select_one(".css-3hse11-Text.eczcs4p0")
    date = soup.select_one(".css-1xux213-Text.eczcs4p0")
    main_informations = soup.select(".css-58bgfg-WrapperFeatures.e2uk8e15")

    if url:
        url = BASE + url.get("href")
        identifier_index = url.find("?search_identifier")
        if identifier_index != -1:
            url = url[:identifier_index]
    if head_image:
        head_image = head_image.get("src")

    property_type = None
    if title:
        title = title.text.strip()
        for el in PROPERTY_TYPES:
            if el in title.lower():
                property_type = el
                break

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

    bedrooms = None
    bathrooms = None
    receptionrooms = None
    for el in main_informations:
        el_name = el.select_one("span span").get("data-testid")
        el_data = el.select_one("p").text.strip()
        if "bed" in el_name:
            bedrooms = int(re.sub(r"\D", "", el_data))
        elif "bath" in el_name:
            bathrooms = int(re.sub(r"\D", "", el_data))
        elif "chair" in el_name:
            receptionrooms = int(re.sub(r"\D", "", el_data))

    soup = request(url)

    key_features = soup.select(".e1q7jq6s2 li")
    description = soup.select_one(".e13tdjjp0 span")
    agent_name = soup.select_one(".e11937k16")
    agent_phone = soup.select_one(
        ".e11937k18.css-v1mvgf-StyledLink-Link-AgentNumber.e33dvwd0"
    )
    agent_address = soup.select_one(".e11937k19")

    if key_features:
        key_features = [i.text for i in key_features]
    if description:
        description = description.text.strip()
    if agent_name:
        agent_name = agent_name.find(text=True).strip()
    if agent_phone:
        agent_phone = agent_phone.get("href").replace("tel:", "")
    if agent_address:
        agent_address = agent_address.text.strip()

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
        receptionrooms,
        key_features,
        description,
    ]


def get_page_data(soup):

    results = []
    articles = soup.select(".e2uk8e10")

    for article in articles:
        try:
            data = get_article_data(article)
            results.append(data)
        except Exception as e:
            print("WENT WRONG", e)

    return results


def get_page_number(soup):

    result_count = soup.select_one(".egjkayq7")
    number_of_pages = int(result_count.text.replace(" results", "").replace("+", ""))
    page_number = number_of_pages // 25

    if number_of_pages / 25 % 1 != 0:
        page_number += 1
    if page_number > 400:
        page_number = 400

    return page_number


def crawl_zoopla(start_url: str):

    data = []

    soup = request(start_url)
    data += get_page_data(soup)
    page_number = get_page_number(soup)

    for i in range(2, page_number + 1):

        url = f"{start_url}&pn={i}"
        soup = request(url)

        data += get_page_data(soup)

    return data