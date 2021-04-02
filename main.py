from threading import Thread

import pandas as pd

from scripts.nethouseprices import crawl_nethouseprices
from scripts.nethouseprices_archive import crawl_nethouseprices_archive
from scripts.onthemarket import crawl_onthemarket
from scripts.rightmove import crawl_rightmove
from scripts.zoopla import crawl_zoopla

URL_ONTHEMARKET = "https://www.onthemarket.com/for-sale/property/peterborough/?recently-added=3-days&sort-field=update_date&view=grid"
URL_ZOOPLA = "https://www.zoopla.co.uk/for-sale/property/peterborough/?added=3_days&page_size=25&q=Peterborough&radius=0&results_sort=newest_listings&search_source=facets"
URL_RIGHTMOVE = "https://www.rightmove.co.uk/property-for-sale/find.html?locationIdentifier=REGION%5E1061&propertyTypes=&maxDaysSinceAdded=3&includeSSTC=false&mustHave=&dontShow=&furnishTypes=&keywords="
URL_NETHOUSEPRICES = "https://nethouseprices.com/properties-for-sale/Peterborough,%20Cambridgeshire?added=last_3_days"
URL_NETHOUSEPRICES_ARCHIVE = "https://nethouseprices.com/house-prices/Peterborough,%20Cambridgeshire?sale_date=three"


def onthemarket():
    data = crawl_onthemarket(URL_ONTHEMARKET)
    df = pd.DataFrame.from_dict(data)
    df.to_csv("onthemarket.csv")


def zoopla():
    data = crawl_zoopla(URL_ZOOPLA)
    df = pd.DataFrame.from_dict(data)
    df.to_csv("zoopla.csv")


def rightmove():
    data = crawl_rightmove(URL_RIGHTMOVE)
    df = pd.DataFrame.from_dict(data)
    df.to_csv("rightmove.csv")


def nethouseprices():
    data = crawl_nethouseprices(URL_NETHOUSEPRICES)
    df = pd.DataFrame.from_dict(data)
    df.to_csv("nethouseprices.csv")


def nethouseprices_archive():
    data = crawl_nethouseprices_archive(URL_NETHOUSEPRICES_ARCHIVE)
    df = pd.DataFrame.from_dict(data)
    df.to_csv("nethouseprices_archive.csv")


onthemarket()
zoopla()
rightmove()
nethouseprices_archive()
nethouseprices()