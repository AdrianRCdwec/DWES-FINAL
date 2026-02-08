from rest_framework.viewsets import ModelViewSet
from .models import Pelicula, Categoria
from .serializers import PeliculaSerializer, PeliculaCreateSerializer, CategoriaSerializer

from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class PeliculaListAPIView(APIView):
    def get(self, request):
        peliculas = Pelicula.objects.all()
        serializer = PeliculaSerializer(peliculas, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PeliculaCreateSerializer(data=request.data)
        if serializer.is_valid():
            pelicula = serializer.save()
            return Response(PeliculaSerializer(pelicula).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PeliculaDetailAPIView(APIView):
    def get(self, request, pk):
        pelicula = get_object_or_404(Pelicula, pk=pk)
        serializer = PeliculaSerializer(pelicula)
        return Response(serializer.data)

class PeliculaViewSet(ModelViewSet):
    queryset = Pelicula.objects.all()

    def get_serializer_class(self):
        # En GET usamos el de lectura; en POST/PUT/PATCH el de escritura
        if self.action in ("list", "retrieve"):
            return PeliculaSerializer
        return PeliculaCreateSerializer


class CategoriaViewSet(ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
