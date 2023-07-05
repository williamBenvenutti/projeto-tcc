from django.urls import path
from .views import MostraColabs, CadastraColabs, EditarColab

urlpatterns = [
    path('mostra_colabs/', MostraColabs, name='mostra_colabs'),
    path('cadastra_colabs/', CadastraColabs, name='cadastra_colabs'),
    path('editar_colab/<int:colab_id>/', EditarColab, name='editar_colab'),
]