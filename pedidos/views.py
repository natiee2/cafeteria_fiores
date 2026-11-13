from datetime import datetime, timedelta, time
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.db.models import Q, ProtectedError
from django.http import HttpResponseForbidden
from django.utils import timezone

from .models import Categoria, Producto, Pedido, DetallePedido
from .forms import CategoriaForm, ProductoForm


def encargado_requerido(view_func):
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_staff:
            return HttpResponseForbidden("Acceso denegado: esta sección es exclusiva para encargados.")
        return view_func(request, *args, **kwargs)
    return _wrapped_view


def cliente_requerido(view_func):
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_staff:
            return HttpResponseForbidden("Acceso denegado: esta sección es exclusiva para clientes.")
        return view_func(request, *args, **kwargs)
    return _wrapped_view


@login_required
def redireccion_rol(request):
    if request.user.is_staff:
        return redirect('encargado_pedidos')
    return redirect('catalogo')


@cliente_requerido
def catalogo(request):
    productos = Producto.objects.filter(disponible=True, categoria__activa=True)
    categorias = Categoria.objects.filter(activa=True)

    busqueda = request.GET.get('q', '').strip()
    categoria_id = request.GET.get('categoria', '')

    if busqueda:
        productos = productos.filter(nombre__icontains=busqueda)
    if categoria_id:
        productos = productos.filter(categoria_id=categoria_id)

    return render(request, 'pedidos/catalogo.html', {
        'productos': productos,
        'categorias': categorias,
        'busqueda': busqueda,
        'categoria_id': categoria_id,
    })


@encargado_requerido
def categoria_lista(request):
    categorias = Categoria.objects.all()
    return render(request, 'pedidos/categoria_lista.html', {'categorias': categorias})


@encargado_requerido
def categoria_detalle(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    return render(request, 'pedidos/categoria_detalle.html', {'categoria': categoria})


@encargado_requerido
def categoria_crear(request):
    form = CategoriaForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Categoría creada correctamente.")
        return redirect('categoria_lista')
    return render(request, 'pedidos/categoria_form.html', {'form': form, 'accion': 'Crear'})


@encargado_requerido
def categoria_editar(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    form = CategoriaForm(request.POST or None, instance=categoria)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Categoría actualizada correctamente.")
        return redirect('categoria_lista')
    return render(request, 'pedidos/categoria_form.html', {'form': form, 'accion': 'Editar'})


@encargado_requerido
def categoria_eliminar(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        try:
            categoria.delete()
            messages.success(request, "Categoría eliminada correctamente.")
        except ProtectedError:
            messages.error(request, "No se puede eliminar la categoría porque tiene productos asociados.")
        return redirect('categoria_lista')
    return render(request, 'pedidos/confirmar_eliminar.html', {
        'objeto': categoria,
        'tipo': 'Categoría',
        'url_volver': 'categoria_lista'
    })


@encargado_requerido
def producto_lista(request):
    productos = Producto.objects.select_related('categoria').all()
    categorias = Categoria.objects.all()

    q = request.GET.get('q', '').strip()
    cat = request.GET.get('categoria', '')
    disp = request.GET.get('disponible', '')

    if q:
        productos = productos.filter(Q(nombre__icontains=q) | Q(codigo__icontains=q))
    if cat:
        productos = productos.filter(categoria_id=cat)
    if disp == '1':
        productos = productos.filter(disponible=True)
    elif disp == '0':
        productos = productos.filter(disponible=False)

    return render(request, 'pedidos/producto_lista.html', {
        'productos': productos,
        'categorias': categorias,
        'q': q,
        'cat': cat,
        'disp': disp,
    })


@encargado_requerido
def producto_detalle(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    return render(request, 'pedidos/producto_detalle.html', {'producto': producto})


@encargado_requerido
def producto_crear(request):
    form = ProductoForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Producto creado correctamente.")
        return redirect('producto_lista')
    return render(request, 'pedidos/producto_form.html', {'form': form, 'accion': 'Crear'})


@encargado_requerido
def producto_editar(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    form = ProductoForm(request.POST or None, instance=producto)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Producto actualizado correctamente.")
        return redirect('producto_lista')
    return render(request, 'pedidos/producto_form.html', {'form': form, 'accion': 'Editar'})


@encargado_requerido
def producto_eliminar(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        try:
            producto.delete()
            messages.success(request, "Producto eliminado correctamente.")
        except ProtectedError:
            messages.error(request, "No se puede eliminar el producto porque está asociado a pedidos existentes.")
        return redirect('producto_lista')
    return render(request, 'pedidos/confirmar_eliminar.html', {
        'objeto': producto,
        'tipo': 'Producto',
        'url_volver': 'producto_lista'
    })


@cliente_requerido
def ver_carrito(request):
    carrito = request.session.get('carrito', {})
    items = []
    total = 0

    for prod_id, datos in list(carrito.items()):
        producto = Producto.objects.filter(pk=prod_id, disponible=True, categoria__activa=True).first()
        if not producto:
            del carrito[prod_id]
            request.session.modified = True
            continue
        subtotal = producto.precio * datos['cantidad']
        total += subtotal
        items.append({
            'producto': producto,
            'cantidad': datos['cantidad'],
            'subtotal': subtotal,
        })

    return render(request, 'pedidos/carrito.html', {'items': items, 'total': total})


@cliente_requerido
def agregar_carrito(request, producto_id):
    if request.method != 'POST':
        return redirect('catalogo')

    producto = get_object_or_404(Producto, pk=producto_id, disponible=True, categoria__activa=True)
    carrito = request.session.get('carrito', {})
    prod_key = str(producto.id)

    total_actual = sum(item['cantidad'] for item in carrito.values())
    if total_actual >= 10:
        messages.error(request, "No puedes llevar más de 10 unidades en total por pedido.")
        return redirect('catalogo')

    cantidad_actual = carrito.get(prod_key, {}).get('cantidad', 0)
    if cantidad_actual + 1 > producto.stock:
        messages.error(request, f"Stock insuficiente para {producto.nombre}.")
        return redirect('catalogo')

    carrito[prod_key] = {'cantidad': cantidad_actual + 1}
    request.session['carrito'] = carrito
    messages.success(request, f"Se agregó {producto.nombre} al carrito.")
    return redirect('catalogo')


@cliente_requerido
def actualizar_carrito(request, producto_id):
    if request.method != 'POST':
        return redirect('ver_carrito')

    producto = get_object_or_404(Producto, pk=producto_id)
    carrito = request.session.get('carrito', {})
    prod_key = str(producto.id)

    if prod_key in carrito:
        try:
            nueva_cant = int(request.POST.get('cantidad', 1))
        except ValueError:
            nueva_cant = 1

        if nueva_cant <= 0:
            del carrito[prod_key]
            messages.info(request, f"Se quitó {producto.nombre} del carrito.")
        else:
            otros_items = sum(v['cantidad'] for k, v in carrito.items() if k != prod_key)
            if otros_items + nueva_cant > 10:
                messages.error(request, "El pedido no puede superar las 10 unidades en total.")
            elif nueva_cant > producto.stock:
                messages.error(request, f"Solo quedan {producto.stock} unidades de {producto.nombre}.")
            else:
                carrito[prod_key]['cantidad'] = nueva_cant
                messages.success(request, "Cantidad actualizada.")

        request.session['carrito'] = carrito

    return redirect('ver_carrito')


@cliente_requerido
def quitar_carrito(request, producto_id):
    if request.method == 'POST':
        carrito = request.session.get('carrito', {})
        prod_key = str(producto_id)
        if prod_key in carrito:
            del carrito[prod_key]
            request.session['carrito'] = carrito
            messages.info(request, "Producto eliminado del carrito.")
    return redirect('ver_carrito')


@cliente_requerido
def vaciar_carrito(request):
    if request.method == 'POST':
        request.session['carrito'] = {}
        messages.info(request, "El carrito se ha vaciado.")
    return redirect('ver_carrito')


@cliente_requerido
def confirmar_pedido(request):
    if request.method != 'POST':
        return redirect('ver_carrito')

    carrito = request.session.get('carrito', {})
    if not carrito:
        messages.error(request, "Tu carrito está vacío.")
        return redirect('catalogo')

    hora_str = request.POST.get('hora_retiro', '')
    observacion = request.POST.get('observacion', '').strip()

    try:
        hora_retiro = datetime.strptime(hora_str, '%H:%M').time()
    except ValueError:
        messages.error(request, "Debes ingresar una hora de retiro válida.")
        return redirect('ver_carrito')

    if not (time(8, 0) <= hora_retiro <= time(18, 0)):
        messages.error(request, "La hora de retiro debe estar entre las 08:00 y las 18:00.")
        return redirect('ver_carrito')

    ahora_local = timezone.localtime()
    minimo_retiro = (ahora_local + timedelta(minutes=20)).time()
    if hora_retiro < minimo_retiro:
        messages.error(
            request,
            f"La hora de retiro debe ser al menos 20 minutos después de la hora actual ({minimo_retiro.strftime('%H:%M')})."
        )
        return redirect('ver_carrito')

    try:
        with transaction.atomic():
            productos_bloqueados = Producto.objects.select_for_update().filter(pk__in=carrito.keys())
            mapa_productos = {str(p.id): p for p in productos_bloqueados}

            total_pedido = 0
            for prod_id, datos in carrito.items():
                prod = mapa_productos.get(prod_id)
                if not prod or not prod.disponible or prod.stock < datos['cantidad']:
                    nombre_error = prod.nombre if prod else f"ID {prod_id}"
                    raise ValueError(f"Stock insuficiente para el producto: {nombre_error}.")
                total_pedido += prod.precio * datos['cantidad']

            pedido = Pedido.objects.create(
                cliente=request.user,
                hora_retiro=hora_retiro,
                estado='Pendiente',
                total=total_pedido,
                observacion=observacion
            )

            for prod_id, datos in carrito.items():
                prod = mapa_productos[prod_id]
                cant = datos['cantidad']
                DetallePedido.objects.create(
                    pedido=pedido,
                    producto=prod,
                    cantidad=cant,
                    precio_unitario=prod.precio,
                    subtotal=prod.precio * cant
                )
                prod.stock -= cant
                prod.save()

            request.session['carrito'] = {}
            messages.success(request, f"¡Pedido #{pedido.id} confirmado con éxito!")
            return redirect('mis_pedidos')

    except ValueError as e:
        messages.error(request, str(e))
        return redirect('ver_carrito')


@cliente_requerido
def mis_pedidos(request):
    pedidos = Pedido.objects.filter(cliente=request.user).prefetch_related('detalles__producto')
    return render(request, 'pedidos/mis_pedidos.html', {'pedidos': pedidos})


@cliente_requerido
def cancelar_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, pk=pedido_id, cliente=request.user)

    if request.method == 'POST':
        if pedido.estado != 'Pendiente':
            messages.error(request, "Solo se pueden cancelar pedidos en estado Pendiente.")
        else:
            with transaction.atomic():
                for detalle in pedido.detalles.select_related('producto'):
                    prod = detalle.producto
                    prod.stock += detalle.cantidad
                    prod.save()
                pedido.estado = 'Cancelado'
                pedido.save()
            messages.success(request, f"Pedido #{pedido.id} cancelado y stock repuesto.")

    return redirect('mis_pedidos')


@encargado_requerido
def encargado_pedidos(request):
    hoy = timezone.localdate()
    pedidos = Pedido.objects.filter(fecha__date=hoy).prefetch_related('detalles__producto', 'cliente')
    estado_filtro = request.GET.get('estado', '')

    if estado_filtro:
        pedidos = pedidos.filter(estado=estado_filtro)

    return render(request, 'pedidos/encargado_pedidos.html', {
        'pedidos': pedidos,
        'estado_filtro': estado_filtro,
    })


@encargado_requerido
def avanzar_estado_pedido(request, pedido_id):
    if request.method != 'POST':
        return redirect('encargado_pedidos')

    pedido = get_object_or_404(Pedido, pk=pedido_id)
    transiciones = {
        'Pendiente': 'En preparación',
        'En preparación': 'Listo',
        'Listo': 'Entregado',
    }

    siguiente = transiciones.get(pedido.estado)
    if siguiente:
        pedido.estado = siguiente
        pedido.save()
        messages.success(request, f"Pedido #{pedido.id} actualizado a '{siguiente}'.")
    else:
        messages.error(request, f"El pedido #{pedido.id} no puede avanzar desde '{pedido.estado}'.")

    return redirect('encargado_pedidos')