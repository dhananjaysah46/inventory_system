# accounts/permissions.py
from rest_framework.permissions import BasePermission


class IsAdminUser(BasePermission):
    """सिर्फ Admin ले access पाउने"""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin


class IsManagerOrAdmin(BasePermission):
    """Manager र Admin दुवैले access पाउने"""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_manager


class IsAuthenticatedReadOnly(BasePermission):
    """
    GET - सबैले गर्न पाउने
    POST/PUT/DELETE - Manager+ मात्र
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        return request.user.is_manager