from django.shortcuts import render, get_object_or_404
from rest_framework import status, mixins, viewsets
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.decorators import action

from django.contrib.gis.geos import Point, Polygon

import requests
from time import sleep

from crawlers.models import Property, Crawler

from .serializers import (
    PropertySerializer,
    CrawlerSerializer,
)

from crawlers import tasks


class PropertyViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer

    def list(self, request):

        address = request.query_params.get("address")
        if not address:
            return Response(status=status.HTTP_404_NOT_FOUND)
        address_osm_id = (
            requests.get(
                f"https://nominatim.openstreetmap.org/search?q={address}&format=json"
            )
            .json()[0]
            .get("osm_id")
        )
        bbox = requests.get(
            f"https://nominatim.openstreetmap.org/reverse?osm_id={address_osm_id}&format=json&polygon_geojson=1&osm_type=R"
        ).json()["geojson"]["coordinates"]
        if not bbox:
            return Response(status=status.HTTP_404_NOT_FOUND)

        poly = Polygon(tuple((x, y) for x, y in bbox[0]))
        query = Property.objects.filter(cordinates__intersects=poly)
        serializer = PropertySerializer(query, many=True)
        ctx = {
            "properties": serializer.data,
            "cordinates": bbox,
        }
        return Response(ctx, status=status.HTTP_200_OK)


class CrawlerViewSet(viewsets.ModelViewSet):
    queryset = Crawler.objects.all()
    serializer_class = CrawlerSerializer

    @action(detail=False, methods=["GET"], url_path="run")
    def run_all_crawlers(self, request):
        crawlers = Crawler.objects.all()
        tasks.run_all_crawlers()
        serializer = CrawlerSerializer(crawlers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["GET"], url_path="run")
    def run_crawler_by_id(self, request, pk):
        crawler = get_object_or_404(Crawler, pk=pk)
        crawler_url = crawler.url

        if "onthemarket" in crawler_url:
            tasks.onthemarket.delay(crawler_url)
        elif "zoopla" in crawler_url:
            tasks.zoopla.delay(crawler_url)
        elif "rightmove" in crawler_url:
            tasks.rightmove.delay(crawler_url)
        elif "home" in crawler_url:
            tasks.home.delay(crawler_url)
        elif "nethouseprices.com/house-prices" in crawler_url:
            tasks.nethouseprices_archive.delay(crawler_url)
        elif "nethouseprices.com/properties-for-sale" in crawler_url:
            tasks.nethouseprices.delay(crawler_url)

        serializer = CrawlerSerializer(crawler)
        return Response(serializer.data, status=status.HTTP_200_OK)