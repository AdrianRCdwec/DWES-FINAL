from rest_framework import serializers
from .models import Pelicula, Etiqueta, Categoria

class PeliculaSerializer(serializers.ModelSerializer):
    # En GET: devolvemos etiquetas como lista de IDs
    etiquetas = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Pelicula
        fields = [
            "id", "titulo", "descripcion",
            "categoria", "etiquetas",
            "precio", "fecha_estreno", "duracion", "activa",
            "created_at", "updated_at",
        ]
        extra_kwargs = {
            "id": {"read_only": True},
            "created_at": {"read_only": True},
            "updated_at": {"read_only": True},
        }


class PeliculaCreateSerializer(serializers.ModelSerializer):
    etiquetas = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Etiqueta.objects.all(),
        required=False
    )

    class Meta:
        model = Pelicula
        fields = [
            "titulo", "descripcion", "categoria",
            "precio", "fecha_estreno", "duracion", "activa",
            "etiquetas",
        ]

    def validate_precio(self, value):
        if value < 0:
            raise serializers.ValidationError("El precio no puede ser negativo")
        return value


class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ["id", "nombre", "descripcion"]
        extra_kwargs = {"id": {"read_only": True}}

