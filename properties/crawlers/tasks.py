from django.db.models import F
from celery import shared_task
from .scripts.nethouseprices import crawl_nethouseprices
from .scripts.nethouseprices_archive import crawl_nethouseprices_archive
from .scripts.onthemarket import crawl_onthemarket
from .scripts.rightmove import crawl_rightmove
from .scripts.zoopla import crawl_zoopla
from .scripts.home import crawl_home
from .models import Crawler, Property
from time import time


@shared_task
def run_all_crawlers():
    crawlers = Crawler.objects.all()
    for obj in crawlers:
        crawler_url = obj.url
        if "onthemarket" in crawler_url:
            onthemarket.delay(crawler_url)
        elif "zoopla" in crawler_url:
            zoopla.delay(crawler_url)
        elif "rightmove" in crawler_url:
            rightmove.delay(crawler_url)
        elif "home" in crawler_url:
            home.delay(crawler_url)
        elif "nethouseprices.com/house-prices" in crawler_url:
            nethouseprices_archive.delay(crawler_url)
        elif "nethouseprices.com/properties-for-sale" in crawler_url:
            nethouseprices.delay(crawler_url)


@shared_task
def onthemarket(url: str):
    data = crawl_onthemarket(url)
    for el in data:
        Property.objects.create(
            url=el[0],
            head_image=[1],
            title=el[2],
            address=el[3],
            price=el[4],
            date=el[5],
            agent_name=el[6],
            agent_phone=el[7],
            agent_address=el[8],
            description=el[9],
            key_features=el[10],
            stations=el[11],
        )


@shared_task
def zoopla(url: str):
    data = crawl_zoopla(url)
    for el in data:
        Property.objects.create(
            url=el[0],
            head_image=el[1],
            title=el[2],
            address=el[3],
            price=el[4],
            date=el[5],
            agent_name=el[6],
            agent_phone=el[7],
            agent_address=el[8],
            property_type=el[9],
            bedrooms=el[10],
            bathrooms=el[11],
            receptionrooms=el[12],
            key_features=el[13],
            description=el[14],
        )


@shared_task
def rightmove(url: str):
    data = crawl_rightmove(url)
    for el in data:
        Property.objects.create(
            url=el[0],
            head_image=el[1],
            title=el[2],
            address=el[3],
            price=el[4],
            date=el[5],
            agent_name=el[6],
            agent_phone=el[7],
            agent_address=el[8],
            property_type=el[9],
            bedrooms=el[10],
            bathrooms=el[11],
            sqft=el[12],
            key_features=el[13],
            description=el[14],
        )


@shared_task
def nethouseprices(url: str):
    data = crawl_nethouseprices(url)
    for el in data:
        Property.objects.create(
            url=el[0],
            head_image=el[1],
            title=el[2],
            address=el[3],
            price=el[4],
            date=el[5],
            agent_name=el[6],
            agent_phone=el[7],
            agent_address=el[8],
            key_features=el[9],
            description=el[10],
            stations=el[11],
        )


@shared_task
def nethouseprices_archive(url: str):
    data = crawl_nethouseprices_archive(url)
    for el in data:
        Property.objects.create(
            url=el[0],
            title=el[1],
            price=el[2],
            address=el[3],
            agent_name=el[4],
            agent_phone=el[5],
            agent_address=el[6],
            description=el[7],
            key_features=el[8],
            listing_history=el[9],
        )


@shared_task
def home(url: str):
    data = crawl_home(url)
    for el in data:
        Property.objects.create(
            url=el[0],
            head_image=el[1],
            title=el[2],
            price=el[3],
            address=el[4],
            agent_name=el[5],
            agent_phone=el[6],
            agent_address=el[7],
            description=el[8],
            key_features=el[9],
            listing_history=el[10],
        )