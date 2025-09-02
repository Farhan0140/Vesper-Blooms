from django.shortcuts import render

from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, DestroyModelMixin
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Cart, Cart_Items, Order, OrderItem
from .serializers import Cart_Serializer, Cart_Items_Serializer, Add_Cart_Items_Serializer, Update_Cart_Item_Serializer, Order_Serializer, Create_Order_Serializer, Empty_Serializer, Update_Order_Serializer
from.services import Order_Service


class Cart_ViewSet( CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, GenericViewSet ):
    serializer_class = Cart_Serializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Cart.objects.none()
        
        return Cart.objects.filter(user=self.request.user)
    

class Cart_Items_ViewSet( ModelViewSet ):
    http_method_names = ['get', 'post', 'patch', 'delete']
    serializer_class = Cart_Items_Serializer

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return Add_Cart_Items_Serializer
        
        if self.request.method == 'PATCH':
            return Update_Cart_Item_Serializer
        
        return Cart_Items_Serializer

    def get_queryset(self):
        return Cart_Items.objects.select_related('flower').filter(cart_id=self.kwargs.get('cart_pk'))
    
    def get_serializer_context(self):
        if getattr(self, 'swagger_fake_view', False):
            return super().get_serializer_context()
        
        return {'cart_id': self.kwargs.get('cart_pk')}

        
# ______ Orders ________


class Order_ViewSet( ModelViewSet ):
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']

    def get_serializer_class(self, *args, **kwargs):
        if self.action == 'cancel':
            return Empty_Serializer 
        if self.action == 'create':
            return Create_Order_Serializer
        if self.action == 'update_status':
            return Update_Order_Serializer

        return Order_Serializer
    

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Order.objects.none()
         
        if self.request.user.is_staff:
            return Order.objects.prefetch_related('items__flower').all()
        
        return Order.objects.prefetch_related('items__flower').filter(user=self.request.user)
    

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        order = self.get_object()
        user = self.request.user

        Order_Service.cancel_order(order=order, user=user)
        return Response({'status': 'Order Canceled'})


    @action(detail=True, methods=['patch'])
    def update_status(self, request, pk=None):
        order = self.get_object()
        serializer = Update_Order_Serializer(order, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'status': f'Order Status Updated to {request.data['status']}'})


    def get_permissions(self):
        if self.action in ['update_status', 'destroy']:
            return [IsAdminUser()]
        return [IsAuthenticated()]

    
    def get_serializer_context(self):
        return {
            'user_id': self.request.user.id,
            'user': self.request.user,
        }
