from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    avatar = models.ImageField(null=True, upload_to='users/%Y/%m')


class ModelBase(models.Model):
    active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(ModelBase):
    name = models.CharField(max_length=50, null=False)

    def __str__(self):
        return self.name


class Product(ModelBase):
    name = models.CharField(max_length=50, null=False)
    description = models.CharField(max_length=250, null=True)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    manufacturer = models.CharField(max_length=100, null=True)
    image = models.ImageField(upload_to='image/%Y/%m', default=None)
    category = models.ForeignKey(Category, null=False, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Order(ModelBase):
    amount = models.DecimalField(decimal_places=0, max_digits=10)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=250, null=True)
    phone = models.CharField(max_length=50, null=True)


class OrderDetail(models.Model):
    active = models.BooleanField(default=True)
    order = models.ForeignKey(Order, null=False, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, null=False, on_delete=models.CASCADE)
    unit_price = models.DecimalField(decimal_places=0, max_digits=10)
    numb = models.IntegerField()


class Comment(ModelBase):
    content = models.TextField()
    product = models.ForeignKey(Product, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.content

