from django.contrib import admin
from . import models

admin.site.register(models.Products)


@admin.register(models.Order)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('user', 'id', 'total_price',)
    list_filter = ('user', 'id', 'total_price',)


@admin.register(models.OrderItem)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'product', 'quantity',)
    list_filter = ('id', 'order',)
