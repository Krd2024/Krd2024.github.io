print(" -- signals.py is loaded -- ")

from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache

# from .models import Post, User, Question, Product
