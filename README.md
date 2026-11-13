# Cafetería Fiores - Sistema de Gestión y Pedidos

Aplicación web desarrollada en Django 6 y Bootstrap 5 para la gestión de catálogo, inventario y pedidos con retiro en tienda.

## Funcionalidades Principales

* **Control de Acceso por Roles:** Autenticación diferenciada entre **Encargado** (gestión administrativa) y **Cliente** (compras y seguimiento).
* **Gestión de Inventario (CRUD):** Administración completa de categorías y productos con validaciones de código, precio y stock, protegiendo la integridad referencial de pedidos históricos.
* **Carrito de Compras:** Gestión basada en sesiones con validación de disponibilidad en tiempo real y límite de 10 unidades totales por pedido.
* **Procesamiento Transaccional:** Confirmación atómica de pedidos con descuento automático de inventario y validación de horario de retiro.
* **Flujo de Estados:** Seguimiento secuencial del pedido (`Pendiente` → `En preparación` → `Listo` → `Entregado`) y opción de cancelación con reposición automática de stock.

---

## Instrucciones de Instalación y Ejecución

1. **Clonar el repositorio:**
   ```bash
   git clone [https://github.com/natiee2/cafeteria_fiores.git](https://github.com/natiee2/cafeteria_fiores.git)
   cd cafeteria_fiores