from django.urls import path

from shop.auth_user.auth_login import login_view, logoutPage, register_view
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.index_views, name="index"),  # Главная страница приложения 'shop'
    path(
        "products/<str:category_name>/",
        views.product_in_category,
        name="product_in_category",
    ),
    path("login/", login_view, name="login"),
    path("register/", register_view, name="register"),
    path("logoutPage/", logoutPage, name="logoutPage"),
    path("add_to_bascet/", views.add_to_bascet, name="add_to_bascet"),
    path("bascet/", views.bascket, name="bascet"),
    path("checkout/", views.checkout_view, name="checkout"),
    path("order/", views.order, name="order"),
    path("delete/cart/<int:product_id>/", views.delete_product, name="delete"),
    path("delete/cart/", views.delete_cart, name="delete_cart"),
]
