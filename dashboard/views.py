# dashboard/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from django.db.models import Sum, Count, F, ExpressionWrapper, DecimalField

from transactions.models import Sale, Purchase
from inventory.models import Product


class DashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        today = timezone.now().date()

        # Today's sales - DB मा calculate गर्ने
        today_sales = Sale.objects.filter(created_at__date=today)

        today_revenue = today_sales.aggregate(
            total=Sum(F('quantity') * F('unit_price'))
        )['total'] or 0

        # Profit = Revenue - Cost (DB level calculation)
        today_profit = today_sales.aggregate(
            profit=Sum(
                ExpressionWrapper(
                    (F('unit_price') - F('product__cost_price')) * F('quantity'),
                    output_field=DecimalField()
                )
            )
        )['profit'] or 0

        # Low stock items
        low_stock = Product.objects.filter(
            current_stock__lte=F('low_stock_threshold'),
            is_active=True
        ).values('id', 'name', 'current_stock', 'low_stock_threshold')

        # Top 5 selling products (all time)
        top_products = Sale.objects.values(
            'product__name'
        ).annotate(
            total_sold=Sum('quantity')
        ).order_by('-total_sold')[:5]

        return Response({
            'today': {
                'revenue': today_revenue,
                'profit': today_profit,
                'sales_count': today_sales.count(),
            },
            'inventory': {
                'total_products': Product.objects.filter(is_active=True).count(),
                'low_stock_count': low_stock.count(),
                'low_stock_items': list(low_stock),
            },
            'top_products': list(top_products),
        })