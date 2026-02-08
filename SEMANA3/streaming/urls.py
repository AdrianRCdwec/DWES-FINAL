from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PeliculaViewSet, CategoriaViewSet

router = DefaultRouter()
router.register(r'peliculas', PeliculaViewSet, basename='pelicula')
router.register(r'categorias', CategoriaViewSet, basename='categoria')

urlpatterns = [
    path('', include(router.urls)),
]

