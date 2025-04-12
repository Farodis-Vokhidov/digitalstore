from django import template
from digitalstore.models import Category, Product, FavoriteProduct

register = template.Library()


@register.simple_tag()
def get_correct(price):
    try:
        price = float(price)
    except ValueError:
        return price
    return f'{price:,.0f}'.replace('_', ' ')


@register.simple_tag()
def get_same_products(model):
    return Product.objects.filter(model=model)


@register.simple_tag(takes_context=True)
def query_params(context, **kwargs):
    query = context['request'].GET.copy()
    for key, value in kwargs.items():
        query[key] = value

    return query.urlencode()


@register.simple_tag()
def get_favorites(user):
    favorites = FavoriteProduct.objects.filter(user=user)
    products = [i.product for i in favorites]
    return products
