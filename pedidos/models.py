from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator

class Categoria(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    descripcion = models.TextField(blank=True)
    activa = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.PROTECT,
        related_name='productos'
    )
    codigo = models.CharField(
        max_length=10,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^CAF-\d{3}$',
                message='El código debe tener el formato CAF-000 (ej: CAF-001).'
            )
        ]
    )
    nombre = models.CharField(max_length=100)
    precio = models.IntegerField(
        validators=[MinValueValidator(100), MaxValueValidator(20000)]
    )
    stock = models.IntegerField(validators=[MinValueValidator(0)])
    disponible = models.BooleanField(default=True)
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['nombre']

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"


class Pedido(models.Model):
    ESTADOS = [
        ('Pendiente', 'Pendiente'),
        ('En preparación', 'En preparación'),
        ('Listo', 'Listo'),
        ('Entregado', 'Entregado'),
        ('Cancelado', 'Cancelado'),
    ]

    cliente = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='pedidos'
    )
    fecha = models.DateTimeField(auto_now_add=True)
    hora_retiro = models.TimeField()
    estado = models.CharField(max_length=15, choices=ESTADOS, default='Pendiente')
    total = models.IntegerField(default=0)
    observacion = models.TextField(blank=True)

    class Meta:
        ordering = ['-fecha']

    def __str__(self):
        return f"Pedido #{self.id} - {self.cliente.username} ({self.estado})"


class DetallePedido(models.Model):
    pedido = models.ForeignKey(
        Pedido,
        on_delete=models.CASCADE,
        related_name='detalles'
    )
    producto = models.ForeignKey(
        Producto,
        on_delete=models.PROTECT
    )
    cantidad = models.IntegerField(validators=[MinValueValidator(1)])
    precio_unitario = models.IntegerField()
    subtotal = models.IntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['pedido', 'producto'],
                name='unique_pedido_producto'
            )
        ]

    def __str__(self):
        return f"{self.cantidad}x {self.producto.nombre} (Pedido #{self.pedido.id})"