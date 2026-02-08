from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Categoria(models.Model):
    # Nombre de la categoría, debe ser único
    nombre = models.CharField(max_length=100, unique=True, help_text="Nombre de la categoría (único)")
    # Descripción opcional de la categoría
    descripcion = models.TextField(blank=True, help_text="Descripción de la categoría (opcional)")

    class Meta:
        verbose_name_plural = "Categorías"
        ordering = ['nombre']

    def __str__(self):
        return self.nombre

class Etiqueta(models.Model):
    # Nombre de la etiqueta
    nombre = models.CharField(max_length=50, help_text="Nombre de la etiqueta")

    def __str__(self):
        return self.nombre

class Perfil(models.Model):
    # Relación 1:1 con el modelo User de Django
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    # URL de la imagen de perfil, opcional
    avatar = models.CharField(max_length=255, blank=True, help_text="URL de la imagen de perfil (opcional)")
    # Fecha de nacimiento, opcional
    fecha_nacimiento = models.DateField(null=True, blank=True, help_text="Fecha de nacimiento (opcional)")

    def __str__(self):
        return self.usuario.username

class Pelicula(models.Model):
    # Título de la película
    titulo = models.CharField(max_length=200, help_text="Título de la película")
    # Descripción de la película
    descripcion = models.TextField(help_text="Descripción de la película")
    # Relación 1:N con Categoria
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.SET_NULL,
        null=True,
        related_name="peliculas",
        help_text="Categoría a la que pertenece la película"
    )
    # Relación N:M con Etiqueta
    etiquetas = models.ManyToManyField(Etiqueta, blank=True, help_text="Etiquetas asociadas a la película")
    # Relación N:M con User a través de Resena
    usuarios = models.ManyToManyField(User, through='Resena', help_text="Usuarios que han reseñado la película")
    # Precio de la película
    precio = models.DecimalField(max_digits=6, decimal_places=2, default=0.00, help_text="Precio de la película")
    # Fecha de estreno
    fecha_estreno = models.DateField(help_text="Fecha de estreno de la película")
    # Duración en minutos
    duracion = models.IntegerField(help_text="Duración de la película en minutos")
    # Indica si la película está activa
    activa = models.BooleanField(default=True, help_text="Indica si la película está activa")
    # Campos de auditoría
    created_at = models.DateTimeField(auto_now_add=True, help_text="Fecha de creación de la película")
    updated_at = models.DateTimeField(auto_now=True, help_text="Fecha de última actualización de la película")

    class Meta:
        verbose_name = "Película"
        verbose_name_plural = "Películas"
        ordering = ['-fecha_estreno']

    def __str__(self):
        return self.titulo

class Resena(models.Model):
    # Tabla intermedia explícita (Through Model)
    # Relación 1:N con Pelicula
    pelicula = models.ForeignKey(Pelicula, on_delete=models.CASCADE, help_text="Película reseñada")
    # Relación 1:N con User
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, help_text="Usuario que reseña la película")
    # Puntuación de la reseña
    puntuacion = models.IntegerField(help_text="Puntuación de la reseña (0-10)")
    # Comentario opcional de la reseña
    comentario = models.TextField(blank=True, help_text="Comentario de la reseña (opcional)")
    # Fecha de la reseña
    fecha_resena = models.DateTimeField(auto_now_add=True, help_text="Fecha de la reseña")

    class Meta:
        # Evita que un usuario reseñe la misma película dos veces
        constraints = [
            models.UniqueConstraint(fields=['pelicula', 'usuario'], name='unique_resena')
        ]

    def __str__(self):
        return f"{self.usuario.username} - {self.pelicula.titulo}"
