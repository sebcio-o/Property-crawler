from rest_framework import serializers

from crawlers.models import Property, Crawler


class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = "cordinates"


class CrawlerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crawler
        fields = "__all__"
