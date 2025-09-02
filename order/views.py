from django.shortcuts import render

from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, DestroyModelMixin

from .models import Cart, Cart_Items
from .serializers import Cart_Serializer, Cart_Items_Serializer, Add_Cart_Items_Serializer, Update_Cart_Item_Serializer



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

        

