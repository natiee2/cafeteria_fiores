from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from pedidos.models import Categoria, Producto

class Command(BaseCommand):
    help = 'Carga datos iniciales para Cafetería Fiores'

    def handle(self, *args, **kwargs):
        # Usuarios
        if not User.objects.filter(username='encargado').exists():
            User.objects.create_superuser('encargado', 'encargado@fiores.cl', 'fiores123', first_name='Carlos Encargado')
        if not User.objects.filter(username='cliente1').exists():
            User.objects.create_user('cliente1', 'ana@inacapmail.cl', 'fiores123', first_name='Ana Pérez')
        if not User.objects.filter(username='cliente2').exists():
            User.objects.create_user('cliente2', 'luis@inacapmail.cl', 'fiores123', first_name='Luis Soto')

        # 4 Categorías
        cats = {
            'Cafetería': Categoria.objects.get_or_create(nombre='Cafetería', defaults={'descripcion': 'Café de grano e infusiones', 'activa': True})[0],
            'Pastelería': Categoria.objects.get_or_create(nombre='Pastelería', defaults={'descripcion': 'Dulces, tortas y medialunas', 'activa': True})[0],
            'Sándwiches': Categoria.objects.get_or_create(nombre='Sándwiches', defaults={'descripcion': 'Fajitas, ciabattas y miga', 'activa': True})[0],
            'Bebidas Frías': Categoria.objects.get_or_create(nombre='Bebidas Frías', defaults={'descripcion': 'Jugos naturales y bebidas', 'activa': True})[0],
        }

        # 20 Productos
        productos_data = [
            ('CAF-001', 'Café Americano', 'Cafetería', 1500, 25, True),
            ('CAF-002', 'Cappuccino', 'Cafetería', 2200, 20, True),
            ('CAF-003', 'Latte Vainilla', 'Cafetería', 2500, 15, True),
            ('CAF-004', 'Espresso Doble', 'Cafetería', 1800, 0, True),
            ('CAF-005', 'Té Chai Latte', 'Cafetería', 2300, 10, False),
            ('CAF-006', 'Medialuna Dulce', 'Pastelería', 1200, 30, True),
            ('CAF-007', 'Muffin de Arándanos', 'Pastelería', 1800, 12, True),
            ('CAF-008', 'Trozo Torta Selva Negra', 'Pastelería', 2900, 8, True),
            ('CAF-009', 'Brownie de Chocolate', 'Pastelería', 2000, 0, True),
            ('CAF-010', 'Roll de Canela', 'Pastelería', 2100, 14, True),
            ('CAF-011', 'Ciabatta Ave Palta', 'Sándwiches', 3500, 18, True),
            ('CAF-012', 'Barros Luco', 'Sándwiches', 3800, 10, True),
            ('CAF-013', 'Fajita Pollo Teriyaki', 'Sándwiches', 3600, 15, True),
            ('CAF-014', 'Sándwich Vegetariano', 'Sándwiches', 3200, 5, False),
            ('CAF-015', 'Empanada Pino Horno', 'Sándwiches', 2400, 22, True),
            ('CAF-016', 'Jugo Natural Naranja', 'Bebidas Frías', 2000, 20, True),
            ('CAF-017', 'Limonada Menta Jengibre', 'Bebidas Frías', 2200, 16, True),
            ('CAF-018', 'Agua Mineral Sin Gas', 'Bebidas Frías', 1100, 40, True),
            ('CAF-019', 'Bebida Lata 350cc', 'Bebidas Frías', 1300, 35, True),
            ('CAF-020', 'Café Helado Mocaccino', 'Bebidas Frías', 2800, 0, True),
        ]

        for cod, nom, cat_nom, pre, stk, disp in productos_data:
            Producto.objects.get_or_create(
                codigo=cod,
                defaults={
                    'categoria': cats[cat_nom],
                    'nombre': nom,
                    'precio': pre,
                    'stock': stk,
                    'disponible': disp
                }
            )
        self.stdout.write(self.style.SUCCESS('Datos de prueba cargados exitosamente.'))