from django.urls import path
from reports.views import MostraReport


urlpatterns = [
    path('mostra_reports/', MostraReport, name='mostra_reporst')
]