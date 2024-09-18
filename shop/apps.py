from django.apps import AppConfig


class ShopConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "shop"

    print(11111111111111111111111)

    def ready(self):

        import shop.signals

        print(2222222222222222222)
