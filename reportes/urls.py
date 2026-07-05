from django.urls import path

from . import views

app_name = "reportes"

urlpatterns = [
    path("pdf/", views.reporte_pdf, name="pdf"),
    path("excel/", views.reporte_excel, name="excel"),
]
