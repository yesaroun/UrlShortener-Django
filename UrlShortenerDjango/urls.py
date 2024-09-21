from django.contrib import admin
from django.conf.urls import include
from django.urls import path

from UrlShortenerDjango.settings import DEBUG
from shortener.urls.views import url_redirect
from shortener.urls.urls import router as url_router

if DEBUG:
    import debug_toolbar

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("shortener.index.urls")),
    path("urls/", include("shortener.urls.urls")),
    path("api/", include(url_router.urls)),
    path("<str:prefix>/<str:url>", url_redirect),
]

if DEBUG:
    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),
    ]
