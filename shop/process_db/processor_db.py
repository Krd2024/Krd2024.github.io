from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import render

from shop.models import Cart, CartItem, Category, Order, OrderItem, Product

from django.shortcuts import render, get_object_or_404


# def index_process(request):
#     test = Product.objects.all()
#     res = render(request, "index.html", {"test": test})
#     return res
def get_category(request):
    category_obj = Category.objects.all()
    print(category_obj)
    contex = render(request, "index.html", {"category": category_obj})
    return contex


def get_products_in_category(category_name):
    category = get_object_or_404(Category, name=category_name)
    # product.quantity_bascket = product.stock_quantity

    return Product.objects.filter(category=category)


def get_bascet(request):

    cart_obj = Cart.objects.prefetch_related("items").get(user=request.user)
    # print("--------------------------------")
    # for cart_item in cart_obj.items.all():

    #     product = cart_item.product
    #     quantity = cart_item.quantity
    #     price = cart_item.price

    #     print(product, quantity, price)
    # print("--------------------------------")

    return cart_obj


def create_cart_item(product_id, quantity, user):
    """Создать корзину + добавить товар"""

    try:
        cart, created = Cart.objects.get_or_create(user=user)

        product = Product.objects.get(id=product_id)
        try:
            # product.quantity_bascket = product.stock_quantity
            product.stock_quantity -= quantity
            product.save()
            # print(product.stock_quantity)

            cart_item = CartItem.objects.get(cart=cart, product=product)
            cart_item.quantity += quantity
            cart_item.price = product.price

            cart_item.save()

        except ObjectDoesNotExist:
            cart_item = CartItem.objects.create(
                cart=cart, product=product, quantity=quantity, price=product.price
            )
        except Exception as e:
            print(e)

    except Exception as e:
        status = 0
        return status


def create_order_from_cart(user):
    try:
        cart_obj = Cart.objects.prefetch_related("items").get(user=user)

        total_amount = sum(cart_item.total_price for cart_item in cart_obj.items.all())
        if total_amount == 0:
            return

        order = Order.objects.create(user=user, total_price=total_amount)

        for cart_item in cart_obj.items.all():
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                price=cart_item.price,
            )

        # Очищаем корзину после создания заказа
        cart_obj.items.all().delete()

        return order
    except Exception as e:
        print(e)
        return None


def get_orders(user):
    orders = Order.objects.filter(user=user)  # Получаем заказ с ID 1
    # items = orders.get_order_items()  # Получаем все элементы этого заказа
    # for item in items:
    #     print(
    #         f"Product: {item.product.name}, Quantity: {item.quantity}, Total Price: {item.total_price}"
    #     )
    return orders


def delete_product_in_bascket(user, product_id, all=False):
    print(user, product_id)
    cart = get_object_or_404(Cart, user=user)
    try:
        product_del = get_object_or_404(
            CartItem, cart=cart, product=(Product.objects.get(id=product_id))
        )
        print(product_del.quantity, "<<< -----на удаление ")

        product = Product.objects.get(id=product_id)
        product.stock_quantity += product_del.quantity

        product.save()
        product_del.delete()
        return True
    except Exception as e:
        print(e)


def delete_product_in_bascket_all(user):
    """Удалить содержимое корзины"""
    try:
        cart_obj = Cart.objects.prefetch_related("items").get(user=user)
        all_product = cart_obj.items.all()
        for product in all_product:
            add_quantity = Product.objects.get(pk=product.product.id)
            add_quantity.stock_quantity += product.quantity
            add_quantity.save()
        cart_obj.delete()
    except Exception as e:
        print(e)
    # print(product.quantity)
    # print(product.product.id)
    # print(product.product.name)
    # print(product.quantity)
