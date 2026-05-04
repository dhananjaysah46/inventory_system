from rest_framework import serializers
from .models import Purchase, Sale
from inventory.models import Product


class PurchaseSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    total_cost = serializers.DecimalField(
        max_digits=10, decimal_places=2, read_only=True
    )
    # recorded_by automatically current user हुन्छ - user ले manually दिनु पर्दैन
    recorded_by = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Purchase
        fields = [
            'id', 'product', 'product_name', 'supplier_name',
            'quantity', 'unit_cost', 'total_cost',
            'recorded_by', 'created_at'
        ]

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Quantity must be greater than 0.")
        return value


class SaleSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    total_revenue = serializers.DecimalField(
        max_digits=10, decimal_places=2, read_only=True
    )
    total_profit = serializers.DecimalField(
        max_digits=10, decimal_places=2, read_only=True
    )
    recorded_by = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Sale
        fields = [
            'id', 'product', 'product_name', 'customer_name',
            'quantity', 'unit_price', 'total_revenue', 'total_profit',
            'recorded_by', 'created_at'
        ]

    def validate(self, data):
        """
        Stock available छ कि छैन check गर्ने
        यो critical validation हो - बेच्नु अघि stock हेर्नु पर्छ
        """
        product = data.get('product')
        quantity = data.get('quantity', 0)

        if product and quantity > product.current_stock:
            raise serializers.ValidationError(
                f"Insufficient stock. Available: {product.current_stock}"
            )
        return data