from django.db import models
from apps.user.models import *
# Create your models here.
class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=250)
    description = models.TextField()
    image = models.CharField(max_length=250)
    is_deleted = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User_Profile,on_delete=models.CASCADE,related_name='category_created')
    updated_by = models.ForeignKey(User_Profile,on_delete=models.CASCADE,related_name='category_updated')

    class Meta:
        managed = True
        db_table = 'category'

class Items(models.Model):
    id = models.AutoField(primary_key=True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    description = models.TextField()
    image = models.CharField(max_length=250)
    item_type = models.CharField(max_length=250)
    price = models.DecimalField(max_digits=5,decimal_places=2)
    is_deleted = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User_Profile,on_delete=models.CASCADE,related_name='item_created')
    updated_by = models.ForeignKey(User_Profile,on_delete=models.CASCADE,related_name='item_updated')

    class Meta:
        managed = True
        db_table = 'items'

class Favourite(models.Model):
    item = models.ForeignKey(Items,on_delete=models.CASCADE,related_name='fav_item')
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User_Profile,on_delete=models.CASCADE,related_name='fav_created')

    class Meta:
        managed = True
        db_table = 'fav'

class Mycart(models.Model):
    item = models.ForeignKey(Items,on_delete=models.CASCADE,related_name='items')
    quantity = models.CharField(max_length=250)
    price = models.DecimalField(max_digits=5,decimal_places=2)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User_Profile,on_delete=models.CASCADE,related_name='created')

    class Meta:
        managed = True
        db_table = 'mycart'

class Order(models.Model):
    is_paid = models.BooleanField(default=False)
    total_amount = models.DecimalField(max_digits=5,decimal_places=2)
    is_cancelled = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User_Profile,on_delete=models.CASCADE,related_name='order_by')
    status = models.CharField(max_length=200,null=True)

    class Meta:
        managed = True
        db_table = 'order'
  
class OrderHistory(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE,related_name='order')
    item = models.ForeignKey(Items,on_delete=models.CASCADE,related_name='item')
    price = models.DecimalField(max_digits=5,decimal_places=2)
    quantity = models.CharField(max_length=250)

    class Meta:
        managed = True
        db_table = 'orderhistory'

class PaymentHistory(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    payment_order_id = models.CharField(max_length=250)
    pay_id =  models.CharField(max_length=250,null=True)
    is_paid = models.BooleanField(default=False)
    amount = models.DecimalField(max_digits=8,decimal_places=2)
    currency = models.CharField(max_length=200)
    status = models.CharField(max_length=200)

    class Meta:
        db_table = "paymenthistory"
        managed = True

