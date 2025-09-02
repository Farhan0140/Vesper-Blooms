
from django.urls import path, include

from rest_framework_nested import routers

from flowers import views as view


router = routers.DefaultRouter()

router.register('flowers', view.Flowers_ViewSet, basename='flowers')
router.register('categories', view.Category_ViewSet, basename='categories')


urlpatterns = [
    path('', include(router.urls)),
]
