from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect


def home(request):
    return redirect("editor:document_create")


urlpatterns = [
    path("", home, name="home"),                 # redireciona para novo documento
    path("admin/", admin.site.urls),
    path("", include("editor.urls")),
]
