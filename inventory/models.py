from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name
    
class Product(models.Model):
    """
    Core model - सबै calculations यहीँबाट हुन्छ
    """
    category = models.ForeignKey(
        Category, 
        on_delete=models.PROTECT,  # DELETE नगर्न दिने category लाई
        related_name='products'
    )
    name = models.CharField(max_length=200)
    sku = models.CharField(max_length=50, unique=True)  # Stock Keeping Unit
    
    # Pricing
    cost_price = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    selling_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    
    # Stock tracking
    current_stock = models.IntegerField(default=0)
    low_stock_threshold = models.IntegerField(default=10)  # Alert यहाँबाट
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
    
    # Computed properties - model मै राख्नु राम्रो
    @property
    def profit_margin(self):
        """प्रति unit कति कमाउँछौं"""
        return self.selling_price - self.cost_price
    
    @property
    def is_low_stock(self):
        """Low stock alert logic"""
        return self.current_stock <= self.low_stock_threshold
    
    def __str__(self):
        return f"{self.name} (SKU: {self.sku})"
