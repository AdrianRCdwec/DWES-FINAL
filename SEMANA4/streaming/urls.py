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
router.register(r'peliculas', PeliculaViewSet)
router.register(r'categorias', CategoriaViewSet)
router.register(r'etiquetas', EtiquetaViewSet)
router.register(r'resenas', ResenaViewSet)
router.register(r'perfiles', PerfilViewSet)

urlpatterns = router.urls

