from django.db import models
from apps.user.models import *
# Create your models here.
class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=250)
    is_deleted = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User_Profile,on_delete=models.CASCADE)
    updated_by = models.ForeignKey(User_Profile,on_delete=models.CASCADE)

    class Meta:
        managed = True
        db_table = 'category'


class Items(models.Model):
    id = models.AutoField(primary_key=True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    type = models.CharField(max_length=250)
    is_deleted = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User_Profile,on_delete=models.CASCADE)
    updated_by = models.ForeignKey(User_Profile,on_delete=models.CASCADE)

    class Meta:
        managed = True
        db_table = 'items'