from rest_framework import viewsets, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter

from .models import Purchase, Sale
from .serializers import PurchaseSerializer, SaleSerializer
from accounts.permissions import IsManagerOrAdmin


class PurchaseViewSet(viewsets.ModelViewSet):
    permission_classes = [IsManagerOrAdmin]  # Staff ले purchase record गर्न नपाउने
    serializer_class = PurchaseSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['product']
    ordering_fields = ['created_at', 'quantity']

    def get_queryset(self):
        return Purchase.objects.select_related(
            'product', 'recorded_by'
        ).order_by('-created_at')


class SaleViewSet(viewsets.ModelViewSet):
    permission_classes = [IsManagerOrAdmin]
    serializer_class = SaleSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['product']
    ordering_fields = ['created_at', 'quantity']

    def get_queryset(self):
        return Sale.objects.select_related(
            'product', 'recorded_by'
        ).order_by('-created_at')