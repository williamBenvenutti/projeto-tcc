from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('usuarios.urls')),
    path('colaboradores/', include('colaboradores.urls')),
    path('produtos/', include('produtos.urls')),
    path('compras/', include('compras.urls')),
    path('relatorios/', include('relatorios.urls')),
    path('estoque/', include('estoque.urls')),
    path('reports/', include('reports.urls')),
]