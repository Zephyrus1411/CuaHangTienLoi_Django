from dataclasses import fields
from pyexpat import model
from rest_framework import serializers
from .models import Category, User, Product, Order, OrderDetail, Comment


class UserSerializer(serializers.ModelSerializer):
    avatar_path = serializers.SerializerMethodField(source='avatar')

    def get_avatar_path(self, obj):
        request = self.context.get('request')
        if obj.avatar and not obj.avatar.name.startswith('/static'):
            path = '/static/%s' % obj.avatar.name
            return request.build_absolute_uri(path)
            # return 1

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name',
                  'username', 'password', 'email', 'avatar_path']
        extra_kwargs = {
            'password': {
                'write_only': True
            }, 'avatar_path': {
                'read_only': True
            }
        }

    def create(self, validated_data):
        data = validated_data.copy()
        user = User(**data)
        user.set_password(user.password)
        user.save()

        return user

class UserAuthSerializer(UserSerializer):
    avatar_path = serializers.SerializerMethodField(source='avatar')

    def get_avatar_path(self, obj):
        request = self.context.get('request')
        if obj.avatar and not obj.avatar.name.startswith('/static'):
            path = '/static/%s' % obj.avatar.name
            return request.build_absolute_uri(path)
            # return 1

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'avatar_path']
        extra_kwargs = {
            'avatar_path': {
                'read_only': True
            }
        }

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField(source='image')

    def get_image(self, obj):
        request = self.context['request']
        # if obj.image and obj.image.name.startswith("/static"):
        #     pass
        # else:
        path = '/static/%s' % obj.image.name

        return request.build_absolute_uri(path)

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'manufacturer', 'image', 'category']


class CreateCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['content', 'user', 'product']


class CommentSerializer(serializers.ModelSerializer):
    user = UserAuthSerializer()
    # user = UserSerializer()
    class Meta:
        model = Comment
        exclude = ['active']


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ['id','amount', 'user', 'address', 'phone']


class OrderDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderDetail
        fields = ['id', 'order', 'product', 'unit_price', 'numb']

