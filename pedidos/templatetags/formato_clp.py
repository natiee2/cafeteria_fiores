from django import template

register = template.Library()

@register.filter
def clp(valor):
    try:
        entero = int(valor)
        return f"${entero:,}".replace(",", ".")
    except (ValueError, TypeError):
        return "$0"