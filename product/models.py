from django.contrib.auth.models import User
from django.db import models


class Products(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=200)
    price = models.FloatField(default=0)
    description = models.TextField()
    category = models.CharField(max_length=200)
    image = models.ImageField(upload_to='images', default='default.jpg', blank=True)
    quantity = models.IntegerField(default=0, blank=True, null=True)

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return self.title


class Order(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    total_price = models.FloatField(default=0)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user)


class OrderItem(models.Model):
    id = models.BigAutoField(primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Products, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=200)
    price = models.FloatField(default=0)
    quantity = models.IntegerField(default=1)
    image = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return str(self.title) + str(self.quantity)
