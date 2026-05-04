from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer
from accounts.permissions import IsManagerOrAdmin, IsAuthenticatedReadOnly

from inventory import models


class CategoryViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedReadOnly]
    serializer_class = CategorySerializer

    def get_queryset(self):
        # product_count annotate - DB मा count गर्ने, Python मा होइन
        return Category.objects.annotate(
            product_count=Count('products')
        ).order_by('name')


class ProductViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedReadOnly]
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['category', 'is_active']
    search_fields = ['name', 'sku']
    ordering_fields = ['name', 'current_stock', 'selling_price']

    def get_queryset(self):
        return Product.objects.select_related('category').filter(is_active=True)

    @action(detail=False, methods=['get'], url_path='low-stock')
    def low_stock(self, request):
        """
        /api/products/low-stock/ → threshold भन्दा कम stock भएका products
        Custom action - ModelViewSet को बाहिर logic
        """
        low = self.get_queryset().filter(
            current_stock__lte=models.F('low_stock_threshold')
        )
        serializer = self.get_serializer(low, many=True)
        return Response({
            'count': low.count(),
            'items': serializer.data
        })