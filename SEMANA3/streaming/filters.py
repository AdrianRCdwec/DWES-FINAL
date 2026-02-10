import django_filters
from .models import Pelicula

class PeliculaFilter(django_filters.FilterSet):
    duracion_min = django_filters.NumberFilter(field_name="duracion", lookup_expr="gte")
    duracion_max = django_filters.NumberFilter(field_name="duracion", lookup_expr="lte")

    class Meta:
        model = Pelicula
        fields = ["categoria"]
