from django import template
from core.models import CartOrder

register = template.Library()

@register.filter
def cart_item_count(user):
    if user.is_authenticated:
        qs = CartOrder.objects.filter(user=user)
        if qs.exists():
            return qs[0].game_accounts.count()
    return 0 