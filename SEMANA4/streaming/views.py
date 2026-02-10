from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import IntegrityError
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
    filterset_fields = ["categoria"]
    search_fields = ["titulo", "descripcion"]
    ordering_fields = ["titulo", "fecha_estreno", "duracion"]
    ordering = ["titulo"]
    
    def get_permissions(self):
        """
        PUBLICO: GET list/retrieve (ver películas)
        PRIVADO: POST/PUT/PATCH/DELETE (crear/editar/borrar)
        """
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAuthenticated()]

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def valorar(self, request, pk=None):
        # ... tu código existente del Bloque 6
        pelicula = self.get_object()
        serializer = ValorarPeliculaSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        usuario_id = serializer.validated_data['usuario_id']
        puntuacion = serializer.validated_data['puntuacion']
        comentario = serializer.validated_data.get('comentario', '')
        
        try:
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
        except IntegrityError:
            return Response(
                {"error": "Ya has valorado esta película"},
                status=status.HTTP_409_CONFLICT
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

