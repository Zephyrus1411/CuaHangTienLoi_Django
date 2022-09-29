from django.contrib import admin
from .models import Category,User,Product,Order,OrderDetail,Comment


admin.site.register(User)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderDetail)
admin.site.register(Comment)
# Register your models here.
