from django.urls import path
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter

from .views import PropertyViewSet, CrawlerViewSet

router = DefaultRouter()
router.register("properties", PropertyViewSet, basename="properties")
router.register("crawlers", CrawlerViewSet, basename="crawlers")

urlpatterns = router.urls
