from django.contrib import admin
from django.urls import include, path

admin.site.site_title = "UK Properties - Dashboard"
admin.site.site_header = "UK Properties - Dashboard"
admin.sites.AdminSite.index_title = "Database models"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("api.urls")),
    path("api/auth/", include("users.urls")),
]
