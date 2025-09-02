
from django.urls import path, include

from rest_framework_nested import routers

from flowers import views as f_view
from order import views as o_view


router = routers.DefaultRouter()

router.register('flowers', f_view.Flowers_ViewSet, basename='flowers')
router.register('categories', f_view.Category_ViewSet, basename='categories')
router.register('carts', o_view.Cart_ViewSet, basename='carts')

cart_router = routers.NestedDefaultRouter(router, 'carts', lookup='cart')
cart_router.register('items', o_view.Cart_Items_ViewSet, basename='cart_items')


urlpatterns = [
    path('', include(router.urls)),
    path('', include(cart_router.urls)),
]
