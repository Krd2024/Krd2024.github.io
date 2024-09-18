from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import EmailValidator
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):

    email_validator = EmailValidator()
    phone_number = models.CharField(max_length=12, blank=True)
    email = models.EmailField(
        _("email address"),
        unique=True,
        blank=False,
        null=False,
        validators=[email_validator],
    )
    on_the_list = models.BooleanField(default=False)


from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="shop/media/products/category")

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to="shop/media/products")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="product_set",
    )
    discount = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True
    )
    is_active = models.BooleanField(default=True)
    stock_quantity = models.PositiveIntegerField(default=0)
    # quantity_bascket = models.PositiveIntegerField(default=0)
    attributes = models.JSONField(blank=True, null=True)

    def get_discounted_price(self):
        if self.discount:
            return self.price - (self.price * (self.discount / 100))
        return self.price

    def is_in_stock(self):
        return self.stock_quantity > 0

    def __str__(self):
        return self.name

    @property
    def category_name(self):
        return self.category.name if self.category else "Разное"


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart for {self.user.username} (ID: {self.id})"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in Cart ID {self.cart.id}"

    @property
    def total_price(self):
        return self.quantity * self.price


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ("Pending", "Pending"),
            ("Completed", "Completed"),
            ("Cancelled", "Cancelled"),
        ],
    )
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Заказ  {self.id} для  {self.user.username}"

    def get_order_items(self):
        return self.order_items.all()


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, related_name="order_items", on_delete=models.CASCADE
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(
        max_digits=10, decimal_places=2
    )  # Цена товара на момент заказа

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in Order {self.order.id}"

    @property
    def total_price(self):
        return self.quantity * self.price


"""
# Получение всех элементов заказа:

order = Order.objects.get(id=1)  # Получаем заказ с ID 1
items = order.get_order_items()  # Получаем все элементы этого заказа
for item in items:
print(f"Product: {item.product.name}, Quantity: {item.quantity}, Total Price: {item.total_price}")

"""
#
#
"""
# Получение общей цены заказа:

order = Order.objects.get(id=1)  # Получаем заказ с ID 1
total_price = order.get_order_items().aggregate(total_price=models.Sum('total_price'))['total_price']
print(f"Total Price: {total_price}")

"""
