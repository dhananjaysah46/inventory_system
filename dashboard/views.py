from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from django.db.models import Sum, F, ExpressionWrapper, DecimalField
from django.db.models.functions import TruncDate
from datetime import timedelta

from transactions.models import Sale, Purchase
from inventory.models import Product


class DashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        today = timezone.now().date()
        seven_days_ago = today - timedelta(days=6)

        # ── Today's Sales ──
        today_sales = Sale.objects.filter(created_at__date=today)

        today_revenue = today_sales.aggregate(
            total=Sum(F('quantity') * F('unit_price'))
        )['total'] or 0

        today_profit = today_sales.aggregate(
            profit=Sum(
                ExpressionWrapper(
                    (F('unit_price') - F('product__cost_price')) * F('quantity'),
                    output_field=DecimalField()
                )
            )
        )['profit'] or 0

        # ── Low Stock ──
        low_stock = Product.objects.filter(
            current_stock__lte=F('low_stock_threshold'),
            is_active=True
        ).values('id', 'name', 'current_stock', 'low_stock_threshold')

        # ── Top 5 Products ──
        top_products = Sale.objects.values(
            'product__name'
        ).annotate(
            total_sold=Sum('quantity')
        ).order_by('-total_sold')[:5]

        # ── Last 7 Days Sales Trend ──
        daily_sales = Sale.objects.filter(
            created_at__date__gte=seven_days_ago
        ).annotate(
            date=TruncDate('created_at')
        ).values('date').annotate(
            revenue=Sum(F('quantity') * F('unit_price'))
        ).order_by('date')

        # Data नभएको दिन 0 राख्ने
        sales_map = {
            str(s['date']): float(s['revenue'])
            for s in daily_sales
        }

        last_7_days = []
        for i in range(6, -1, -1):
            date = today - timedelta(days=i)
            last_7_days.append({
                'date': str(date),
                'revenue': sales_map.get(str(date), 0)
            })

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
            'last_7_days': last_7_days,  # ← नयाँ
        })