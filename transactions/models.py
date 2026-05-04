from django.db import models
from django.contrib.auth import get_user_model
from inventory.models import Product

User = get_user_model()

# Create your models here.

class Purchase(models.Model):
    """
    Supplier बाट किन्दा - stock बढ्छ
    """
    product = models.ForeignKey(
        Product, 
        on_delete=models.PROTECT,
        related_name='purchases'
    )
    supplier_name = models.CharField(max_length=200)
    quantity = models.PositiveIntegerField()
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2)
    recorded_by = models.ForeignKey(User, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    
    @property
    def total_cost(self):
        return self.quantity * self.unit_cost
    
    def __str__(self):
        return f"Purchase: {self.product.name} x{self.quantity}"


class Sale(models.Model):
    """
    Customer लाई बेच्दा - stock घट्छ
    """
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name='sales'
    )
    customer_name = models.CharField(max_length=200, blank=True)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    recorded_by = models.ForeignKey(User, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    
    @property
    def total_revenue(self):
        return self.quantity * self.unit_price
    
    @property
    def total_profit(self):
        """Sale बाट कति profit भयो"""
        cost = self.quantity * self.product.cost_price
        return self.total_revenue - cost
    
    def __str__(self):
        return f"Sale: {self.product.name} x{self.quantity}"