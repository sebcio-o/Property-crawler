from django.contrib import admin

from .models import Property, Crawler


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "address",
        "price",
        "date",
        "bedrooms",
        "bathrooms",
        "cordinates",
    )


@admin.register(Crawler)
class CrawlerAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "url",
    )
