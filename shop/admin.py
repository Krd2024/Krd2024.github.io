from .models import Product, User, Category
from django.contrib.auth.admin import UserAdmin
from django.contrib import admin


class Model_user_admin(UserAdmin):

    list_display = ("username", "email", "phone_number", "on_the_list")
    search_fields = ("username",)
    list_editable = ("on_the_list", "phone_number")


class Model_category_admin(admin.ModelAdmin):
    list_display = ("name", "description")
    list_editable = (
        "description",
    )  # Поле, которое можно редактировать непосредственно
    list_display_links = ("name",)


class Model_product_admin(admin.ModelAdmin):
    list_display = (
        "name",
        "description",
        "price",
        "created_at",
        "category",
        "discount",
        "is_active",
        "stock_quantity",
        "attributes",
    )
    search_fields = (
        "name",
        "description",
        "category",
    )  # Укажите поля, по которым можно искать
    list_editable = (
        "description",
        "price",
        "category",
        "discount",
        "is_active",
        "stock_quantity",
        "attributes",
    )
    list_display_links = ("name",)  # Поле для ссылки на редактирование


admin.site.register(User, Model_user_admin)
admin.site.register(Product, Model_product_admin)
admin.site.register(Category, Model_category_admin)
