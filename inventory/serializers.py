from rest_framework import serializers
from .models import Category, Product


class CategorySerializer(serializers.ModelSerializer):
    product_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'product_count', 'created_at']


class ProductSerializer(serializers.ModelSerializer):
    # Nested - category को name देखाउने, id मात्र होइन
    category_name = serializers.CharField(
        source='category.name', 
        read_only=True
    )
    
    # Model properties लाई API मा expose गर्ने
    profit_margin = serializers.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        read_only=True
    )
    is_low_stock = serializers.BooleanField(read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'category', 'category_name', 'name', 'sku',
            'cost_price', 'selling_price', 'profit_margin',
            'current_stock', 'low_stock_threshold', 'is_low_stock',
            'is_active', 'created_at'
        ]

    def validate(self, data):
        """
        selling_price cost_price भन्दा कम हुन नहुने
        यो business rule हो - serializer मा राख्नु सही ठाउँ हो
        """
        cost = data.get('cost_price', 0)
        sell = data.get('selling_price', 0)
        
        if sell < cost:
            raise serializers.ValidationError(
                "Selling price cannot be less than cost price."
            )
        return data