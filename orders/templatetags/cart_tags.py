from django import template

register = template.Library()

@register.simple_tag(name='multiply')
def multiply(price, quantity):
    return round(price * quantity, 2)

@register.simple_tag(name='subtotal')
def subtotal(cart):
    return round(sum(item.product.price * item.quantity for item in cart.added_items.all()), 2)



@register.simple_tag(name='total')
def total(cart):
    subtotal = sum(item.product.price * item.quantity for item in cart.added_items.all())
    tax = 35
    return round(subtotal + tax)
