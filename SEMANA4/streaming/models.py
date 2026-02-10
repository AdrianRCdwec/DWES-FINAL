from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Categoria(models.Model):
    nombre = models.CharField(
        max_length=100,
        unique=True,
        help_text="Nombre de la categoría (único)"
    )
    descripcion = models.TextField(
        blank=True,
        help_text="Descripción de la categoría (opcional)"
    )

    class Meta:
        verbose_name_plural = "Categorías"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


class Etiqueta(models.Model):
    nombre = models.CharField(
        max_length=50,
        unique=True,
        help_text="Nombre de la etiqueta (único)"
    )

    class Meta:
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


class Pelicula(models.Model):
    titulo = models.CharField(max_length=200, help_text="Título de la película")
    descripcion = models.TextField(help_text="Descripción de la película")

    # 1:N (ForeignKey)
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="peliculas",
        help_text="Categoría a la que pertenece la película"
    )

    # N:M simple (ManyToMany)
    etiquetas = models.ManyToManyField(
        Etiqueta,
        blank=True,
        related_name="peliculas",
        help_text="Etiquetas asociadas a la película"
    )

    # N:M con modelo intermedio (through)
    usuarios = models.ManyToManyField(
        User,
        through="Resena",
        related_name="peliculas_resenadas",
        blank=True,
        help_text="Usuarios que han reseñado la película"
    )

    precio = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=0.00,
        validators=[MinValueValidator(0)],
        help_text="Precio de la película"
    )
    fecha_estreno = models.DateField(help_text="Fecha de estreno de la película")
    duracion = models.PositiveIntegerField(help_text="Duración de la película en minutos")
    activa = models.BooleanField(default=True, help_text="Indica si la película está activa")

    created_at = models.DateTimeField(auto_now_add=True, help_text="Fecha de creación de la película")
    updated_at = models.DateTimeField(auto_now=True, help_text="Fecha de última actualización de la película")

    class Meta:
        verbose_name = "Película"
        verbose_name_plural = "Películas"
        ordering = ["-fecha_estreno"]

    def __str__(self):
        return self.titulo


# 1:1 (además del Perfil, dejo uno 1:1 dentro del dominio de Película para que puedas exponerlo fácil en la API)
class FichaTecnica(models.Model):
    pelicula = models.OneToOneField(
        Pelicula,
        on_delete=models.CASCADE,
        related_name="ficha_tecnica",
        help_text="Ficha técnica asociada (1:1)"
    )
    idioma_original = models.CharField(max_length=30, blank=True)
    pais = models.CharField(max_length=60, blank=True)
    trailer_url = models.URLField(blank=True)

    def __str__(self):
        return f"Ficha técnica - {self.pelicula.titulo}"


class Resena(models.Model):
    # Through model: la relación en sí misma es una entidad con datos extra
    pelicula = models.ForeignKey(
        Pelicula,
        on_delete=models.CASCADE,
        related_name="resenas",
        help_text="Película reseñada"
    )
    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="resenas",
        help_text="Usuario que reseña la película"
    )
    puntuacion = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        help_text="Puntuación de la reseña (0-10)"
    )
    comentario = models.TextField(blank=True, help_text="Comentario de la reseña (opcional)")
    fecha_resena = models.DateTimeField(auto_now_add=True, help_text="Fecha de la reseña")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["pelicula", "usuario"], name="unique_resena")
        ]
        ordering = ["-fecha_resena"]

    def __str__(self):
        return f"{self.usuario.username} - {self.pelicula.titulo}"


class Perfil(models.Model):
    # 1:1 con User (perfil de usuario)
    usuario = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="perfil"
    )
    avatar = models.CharField(max_length=255, blank=True, help_text="URL de la imagen de perfil (opcional)")
    fecha_nacimiento = models.DateField(null=True, blank=True, help_text="Fecha de nacimiento (opcional)")

    def __str__(self):
        return self.usuario.username

