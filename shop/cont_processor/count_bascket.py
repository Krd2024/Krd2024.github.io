from django.shortcuts import render
from shop.models import Cart


def count_products_in_bascket(request):

    try:
        cart = Cart.objects.get(user=request.user)
        count = cart.items.count()

        print(count)
        return {"count": count}
    except Exception as e:
        print(e)
        return {"count": 0}
