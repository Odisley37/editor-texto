from django.urls import path
from . import views

app_name = "editor"

urlpatterns = [
    path("documento/novo/", views.document_create, name="document_create"),
    path("documento/<int:pk>/", views.document_edit, name="document_edit"),
    path("documento/<int:pk>/pdf/", views.document_pdf, name="document_pdf"),

    path("documentos/", views.document_list, name="document_list"),
]
