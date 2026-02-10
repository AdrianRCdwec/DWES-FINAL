from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    PeliculaViewSet,
    CategoriaViewSet,
    EtiquetaViewSet,
    ResenaViewSet,
    PerfilViewSet,
)

router = DefaultRouter()
router.register(r'peliculas', PeliculaViewSet, basename='pelicula')
router.register(r'categorias', CategoriaViewSet, basename='categoria')
router.register(r'etiquetas', EtiquetaViewSet, basename='etiqueta')
router.register(r'resenas', ResenaViewSet, basename='resena')
router.register(r'perfiles', PerfilViewSet, basename='perfil')

urlpatterns = [
    path('', include(router.urls)),
]

