"""
Сигнал для автоматического распеределения пользователя в группу продукта при назначении доступа

"""

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Access
from .utils import base_distribution


@receiver(post_save, sender=Access)
def post_save_product_access(sender, instance, created, **kwargs):
    if created:
        base_distribution(student=instance.student, product=instance.product)
