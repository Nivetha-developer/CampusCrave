from .models import *
from rest_framework import serializers

class CategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"

class ItemsSerializers(serializers.ModelSerializer):
    category_name = serializers.SerializerMethodField('get_category_name')

    def get_category_name(self,request):
        return Category.objects.get(id=request.category_id).name

    class Meta:
        model = Items
        fields = "__all__"

class CartSerializers(serializers.ModelSerializer):
    class Meta:
        model = Mycart
        fields = "__all__"

class OrderhisSerializers(serializers.ModelSerializer):
    item_name = serializers.SerializerMethodField('get_name')

    def get_name(self,request):
        return Items.objects.get(id=request.item_id).name

    class Meta:
        model = OrderHistory
        fields = "__all__"

class OrderSerializers(serializers.ModelSerializer):
    items = serializers.SerializerMethodField('get_orderhistory')
    item_count = serializers.SerializerMethodField('get_itemcount')
    order_by = serializers.SerializerMethodField('get_orderby')

    def get_orderhistory(self,request):
        order_his = OrderHistory.objects.filter(order_id=request.id) 
        serialized_data = OrderhisSerializers(order_his,many=True).data
        return serialized_data
    
    def get_itemcount(self,request):
        order_his = OrderHistory.objects.filter(order_id=request.id) 
        serialized_data = OrderhisSerializers(order_his,many=True).data
        return len(serialized_data)
    
    def get_orderby(self,request):
        return User_Profile.objects.get(id=request.created_by_id).firstname

    class Meta:
        model = Order
        fields = "__all__"

class FavouriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = Favourite
        fields = "__all__"









