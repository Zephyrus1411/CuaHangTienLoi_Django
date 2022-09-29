from django.urls import path, include
from .import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(prefix='category', viewset=views.CategoryViewSet, basename='category')
router.register(prefix='product', viewset=views.ProductViewSet, basename='product')
router.register(prefix='order', viewset=views.OrderViewSet, basename='order')
router.register(prefix='order-details', viewset=views.OrderDetailViewSet, basename='orderdetail')
router.register(prefix='user', viewset=views.UserViewSet, basename='user')
router.register(prefix='comments', viewset=views.CommentViewSet, basename='comment')

urlpatterns = [
    path('', include(router.urls)),
]