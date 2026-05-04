from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Purchase, Sale

@receiver(post_save, sender=Purchase)
def update_stock_on_purchase(sender, instance, created, **kwargs):
    """
    Purchase save हुँदा automatically stock बढाउने
    Manual update गर्नु पर्दैन - यही हो automation
    """
    if created:  # नयाँ purchase मात्र, update होइन
        product = instance.product
        product.current_stock += instance.quantity
        product.save(update_fields=['current_stock'])  # Efficient: सबै fields update नगर्ने


@receiver(post_save, sender=Sale)
def update_stock_on_sale(sender, instance, created, **kwargs):
    """
    Sale हुँदा stock घटाउने + low stock check
    """
    if created:
        product = instance.product
        product.current_stock -= instance.quantity
        product.save(update_fields=['current_stock'])