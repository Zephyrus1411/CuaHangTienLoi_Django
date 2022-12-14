from rest_framework.decorators import action
from rest_framework.response import Response
from .perms import CommentOwnerPerms
from rest_framework.views import APIView
from django.conf import settings
from rest_framework import viewsets, generics, status, permissions
from drf_yasg.utils import swagger_auto_schema
from .models import Category, User, Product, Order, OrderDetail,Comment
from .serializers import  CategorySerializer ,UserSerializer, ProductSerializer, OrderSerializer, OrderDetailSerializer, CommentSerializer, CreateCommentSerializer
# Create your views here.


class UserViewSet(viewsets.ViewSet, generics.CreateAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == 'current_user':
            return [permissions.IsAuthenticated()]

        return [permissions.AllowAny()]

    @action(methods=['get'], url_path="current-user", detail=False)
    def current_user(self, request):
        return Response(self.serializer_class(request.user, context={'request': request}).data,
                        status=status.HTTP_200_OK)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.filter(active=True)
    serializer_class = CategorySerializer

    def get_queryset(self):
        q = self.queryset

        kw = self.request.query_params.get('kw')
        if kw:
            q = q.filter(name__icontains=kw)

        return q

class OauthInfo(APIView):
    def get(self, request):
        return Response(settings.OAUTH2_INFO, status=status.HTTP_200_OK)

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(active=True)
    serializer_class = ProductSerializer

    def get_queryset(self):
        queryset = self.queryset

        kw = self.request.query_params.get("kw")
        if kw:
            queryset = queryset.filter(name__icontains=kw)

        category_id = self.request.query_params.get("category_id")
        if category_id:
            queryset = queryset.filter(category_id=category_id)

        return queryset

    @swagger_auto_schema(
        operation_description='Get the comments of a lesson',
        responses={
            status.HTTP_200_OK: CommentSerializer()
        }
    )
    @action(methods=['get'], url_path='comments', detail=True)
    def get_comments(self, request, pk):
        product = self.get_object()
        comments = product.comments.select_related('user')

        return Response(CommentSerializer(comments, many=True, context={'request': request}).data,
                        status=status.HTTP_200_OK)


class CommentViewSet(viewsets.ViewSet, generics.CreateAPIView,
                     generics.UpdateAPIView, generics.DestroyAPIView):
    queryset = Comment.objects.filter(active=True)
    serializer_class = CreateCommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action in ['update', 'destroy']:
            return [CommentOwnerPerms()]

        return [permissions.IsAuthenticated()]


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.filter(active=True)
    serializer_class = OrderSerializer

    @action(methods=['get'], detail=True, url_path='order-detail')
    def get_orderdetail(self, request, pk):
        order = self.get_object()
        order_detail = OrderDetail.objects.filter(bookingID=order.id, active=True)

        return Response(data=OrderDetailSerializer(order_detail, many=True,
                                                     context={'request': request}).data,
                        status=status.HTTP_200_OK)


class OrderDetailViewSet(viewsets.ModelViewSet):
    queryset = OrderDetail.objects.filter(active=True)
    serializer_class = OrderDetailSerializer


