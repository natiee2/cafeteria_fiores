def carrito_contador(request):
    carrito = request.session.get('carrito', {})
    total_unidades = sum(item['cantidad'] for item in carrito.values())
    return {'carrito_unidades': total_unidades}