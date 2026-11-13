from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='pedidos/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', views.redireccion_rol, name='redireccion_rol'),

    path('catalogo/', views.catalogo, name='catalogo'),

    path('gestion/categorias/', views.categoria_lista, name='categoria_lista'),
    path('gestion/categorias/<int:pk>/', views.categoria_detalle, name='categoria_detalle'),
    path('gestion/categorias/nueva/', views.categoria_crear, name='categoria_crear'),
    path('gestion/categorias/<int:pk>/editar/', views.categoria_editar, name='categoria_editar'),
    path('gestion/categorias/<int:pk>/eliminar/', views.categoria_eliminar, name='categoria_eliminar'),

    path('gestion/productos/', views.producto_lista, name='producto_lista'),
    path('gestion/productos/<int:pk>/', views.producto_detalle, name='producto_detalle'),
    path('gestion/productos/nuevo/', views.producto_crear, name='producto_crear'),
    path('gestion/productos/<int:pk>/editar/', views.producto_editar, name='producto_editar'),
    path('gestion/productos/<int:pk>/eliminar/', views.producto_eliminar, name='producto_eliminar'),

    path('carrito/', views.ver_carrito, name='ver_carrito'),
    path('carrito/agregar/<int:producto_id>/', views.agregar_carrito, name='agregar_carrito'),
    path('carrito/actualizar/<int:producto_id>/', views.actualizar_carrito, name='actualizar_carrito'),
    path('carrito/quitar/<int:producto_id>/', views.quitar_carrito, name='quitar_carrito'),
    path('carrito/vaciar/', views.vaciar_carrito, name='vaciar_carrito'),
    path('carrito/confirmar/', views.confirmar_pedido, name='confirmar_pedido'),

    path('mis-pedidos/', views.mis_pedidos, name='mis_pedidos'),
    path('mis-pedidos/<int:pedido_id>/cancelar/', views.cancelar_pedido, name='cancelar_pedido'),
    path('gestion/pedidos/', views.encargado_pedidos, name='encargado_pedidos'),
    path('gestion/pedidos/<int:pedido_id>/avanzar/', views.avanzar_estado_pedido, name='avanzar_estado_pedido'),
]