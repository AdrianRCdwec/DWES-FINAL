from rest_framework import viewsets
from .filters import PeliculaFilter
from .models import Pelicula, Categoria, Etiqueta, Resena, Perfil
from .serializers import (
    PeliculaSerializer,
    CategoriaSerializer,
    EtiquetaSerializer,
    ResenaSerializer,
    PerfilSerializer,
)

class PeliculaViewSet(viewsets.ModelViewSet):
    queryset = Pelicula.objects.all()
    serializer_class = PeliculaSerializer
    
    filterset_class = PeliculaFilter
    
    # Filtros simples (elige campos que existan en tu modelo):
    filterset_fields = ["categoria"]  # ejemplo FK

    # Búsqueda textual (elige campos de texto reales):
    search_fields = ["titulo", "descripcion"]  # ejemplo

    # Ordenación (limita campos expuestos):
    ordering_fields = ["titulo", "fecha_estreno", "duracion"]  # ejemplo
    ordering = ["titulo"]  # orden por defecto

class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer

class EtiquetaViewSet(viewsets.ModelViewSet):
    queryset = Etiqueta.objects.all()
    serializer_class = EtiquetaSerializer

class ResenaViewSet(viewsets.ModelViewSet):
    queryset = Resena.objects.all()
    serializer_class = ResenaSerializer

class PerfilViewSet(viewsets.ModelViewSet):
    queryset = Perfil.objects.all()
    serializer_class = PerfilSerializer

