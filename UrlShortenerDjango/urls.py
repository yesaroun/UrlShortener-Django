from django.contrib import admin
from django.conf.urls import include
from django.urls import path
from UrlShortenerDjango.settings import DEBUG

if DEBUG:
    import debug_toolbar
from shortener.views import (
    index,
    get_user,
    register,
    login_view,
    logout_view,
    list_view,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", index, name="index"),
    path("register", register, name="register"),
    path("login", login_view, name="login"),
    path("logout", logout_view, name="logout"),
    path("list", list_view, name="list_view"),
    path("get_user/<int:user_id>", get_user),
    path("urls/", include("shortener.urls.urls")),
]

if DEBUG:
    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),
    ]
