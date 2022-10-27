from django.contrib import admin
from django.urls import path
from datetime import datetime
from .models import Category,User,Product,Order,OrderDetail,Comment
from datetime import date
from django.template.response import TemplateResponse
from django.db.models import Count, Avg, Sum
from django.contrib.auth.models import Group


class GroceryStoreAppAdminSite(admin.AdminSite):
    site_header = 'Hệ thống cửa hàng tiện lợi'

    def get_urls(self):
        return [
            path('page_admin/', self.page_admin_view)
        ] + super().get_urls()

    def page_admin_view(self, request):
        a = []
        total = []
        totalorder = []
        cars = request.GET.get('cars')
        dau = date.today().year
        if cars == 'nam':
            dau = Order.objects.filter().first().created_date.year
            a.append(dau)
            cuoi = Order.objects.filter().last().created_date.year
            a.append(cuoi)
        else:
            a = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        count = Order.objects.filter(active=True).count()
        pr_count = OrderDetail.objects.filter().aggregate(Sum('numb'))
        turnover = Order.objects.filter().aggregate(Sum('amount'))
        if cars == 'nam':
            for i in range(a[0], a[1] + 1):
                tien = Order.objects.filter(created_date__year=i).aggregate(Sum('amount'))
                total.append(tien)
                order = Order.objects.filter(created_date__year=i).count()
                totalorder.append(order)
        else:
            payment = Order.objects.filter(created_date__year=date.today().year)
            orderpr = Order.objects.filter(created_date__year=date.today().year)
            for i in a:
                tien = payment.filter(created_date__month=i).aggregate(Sum('amount'))
                total.append(tien)
                order = orderpr.filter(created_date__month=i).count()
                totalorder.append(order)
        orderpr = Order.objects.filter(created_date__month=date.today().month)
        return TemplateResponse(request, 'admin/Admin_Site_App.html', {
            'a': a,
            'pr_count': pr_count,
            'order_count': count,
            'turnover': turnover,
            'cars': cars,
            'total': total,
            'totalorder': totalorder,
            # 'dau':dau

        })


admin_site = GroceryStoreAppAdminSite('myadmin')

admin_site.register(User)
admin_site.register(Category)
admin_site.register(Product)
admin_site.register(Order)
admin_site.register(OrderDetail)
admin_site.register(Comment)
# Register your models here.
