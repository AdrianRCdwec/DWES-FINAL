from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .filters import PeliculaFilter
from .models import Pelicula, Categoria, Etiqueta, Resena, Perfil
from .serializers import (
    PeliculaSerializer,
    CategoriaSerializer,
    EtiquetaSerializer,
    ResenaSerializer,
    PerfilSerializer,
    ValorarPeliculaSerializer,
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
    
    @action(detail=True, methods=['post'])  # quito permission_classes por ahora (opcional)
    def valorar(self, request, pk=None):
        pelicula = self.get_object()
        
        serializer = ValorarPeliculaSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        usuario_id = serializer.validated_data['usuario_id']
        puntuacion = serializer.validated_data['puntuacion']
        comentario = serializer.validated_data.get('comentario', '')
        
        # Lógica de negocio: get_or_create en Resena (through)
        resena, creada = Resena.objects.get_or_create(
            pelicula=pelicula,
            usuario_id=usuario_id,
            defaults={'puntuacion': puntuacion, 'comentario': comentario}
        )
        
        if not creada:
            return Response(
                {"error": "Ya has valorado esta película"},
                status=status.HTTP_409_CONFLICT
            )
        
        return Response(
            {"mensaje": "Película valorada correctamente", "resena_id": resena.id},
            status=status.HTTP_201_CREATED
        )


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

