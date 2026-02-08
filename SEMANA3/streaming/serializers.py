from django.contrib.auth.models import User
from rest_framework import serializers

from .models import (
    Pelicula,
    Etiqueta,
    Categoria,
    Resena,
    Perfil,
)

# Si has añadido FichaTecnica en models.py, descomenta estas líneas:
# from .models import FichaTecnica


class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ["id", "nombre", "descripcion"]
        read_only_fields = ["id"]


class EtiquetaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Etiqueta
        fields = ["id", "nombre"]
        read_only_fields = ["id"]


class PerfilSerializer(serializers.ModelSerializer):
    class Meta:
        model = Perfil
        fields = ["avatar", "fecha_nacimiento"]


class UserSerializer(serializers.ModelSerializer):
    # 1:1 anidado (solo lectura): en GET te devuelve el perfil completo
    perfil = PerfilSerializer(read_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "perfil"]
        read_only_fields = ["id"]


class ResenaSerializer(serializers.ModelSerializer):
    # opcional: para lectura “rica”
    usuario_detalle = UserSerializer(source="usuario", read_only=True)
    pelicula_titulo = serializers.ReadOnlyField(source="pelicula.titulo")

    class Meta:
        model = Resena
        fields = [
            "id",
            "pelicula",
            "pelicula_titulo",
            "usuario",
            "usuario_detalle",
            "puntuacion",
            "comentario",
            "fecha_resena",
        ]
        read_only_fields = ["id", "fecha_resena", "pelicula_titulo"]


# Si has añadido FichaTecnica, usa este serializer:
# class FichaTecnicaSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = FichaTecnica
#         fields = ["id", "pelicula", "idioma_original", "pais", "trailer_url"]
#         read_only_fields = ["id"]


class PeliculaSerializer(serializers.ModelSerializer):
    # --------
    # PATRÓN MIXTO 1:N (ForeignKey)
    # Escritura: ID (categoria)
    # Lectura: objeto (categoria_detalle)
    # --------
    categoria = serializers.PrimaryKeyRelatedField(
        queryset=Categoria.objects.all(),
        allow_null=True,
        required=False
    )
    categoria_detalle = CategoriaSerializer(source="categoria", read_only=True)

    # --------
    # PATRÓN MIXTO N:M simple (etiquetas)
    # Escritura: lista de IDs (etiquetas)
    # Lectura: lista de objetos (etiquetas_detalle)
    # --------
    etiquetas = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Etiqueta.objects.all(),
        required=False
    )
    etiquetas_detalle = EtiquetaSerializer(source="etiquetas", many=True, read_only=True)

    # --------
    # N:M con modelo intermedio (through): Resena
    # Exponemos la “relación-entidad” como lista en la película (solo lectura)
    # --------
    resenas = ResenaSerializer(many=True, read_only=True)

    # --------
    # 1:1 con ficha técnica (si existe en tu models.py)
    # --------
    # ficha_tecnica = FichaTecnicaSerializer(read_only=True)

    class Meta:
        model = Pelicula
        fields = [
            "id",
            "titulo",
            "descripcion",

            "categoria",
            "categoria_detalle",

            "etiquetas",
            "etiquetas_detalle",

            "usuarios",     # OJO: este es el M2M through; normalmente lo dejamos read_only
            "resenas",      # lectura rica del through

            "precio",
            "fecha_estreno",
            "duracion",
            "activa",
            "created_at",
            "updated_at",

            # "ficha_tecnica",
        ]
        read_only_fields = ["id", "created_at", "updated_at", "usuarios"]

    def validate_precio(self, value):
        if value < 0:
            raise serializers.ValidationError("El precio no puede ser negativo")
        return value

