from .models import *
from apps.user.models import *
from .serializers import *
import json as j
from rest_framework.views import APIView
from CampusCrave.generics.helpers import *
import razorpay
client = razorpay.Client(auth=("rzp_test_FlBgzH672A0qLj", "MEzOs5ltbeyG37eYpGuy63AQ"))

class CategoryView(APIView):
    def get(self,request):
        category_objs = Category.objects.all()
        if  request.GET.get('category_id'):
            category_objs = Category.objects.filter(id= request.GET.get('category_id'))
        serialized_data = CategorySerializers(category_objs,many=True).data
        return APIResponse(serialized_data,200,True)

    def post(self,request):
        data = j.loads(request.body.decode('utf-8'))
        name = data['name']
        description = data['description']
        image = data['image']
        if Category.objects.filter(name=name,is_deleted=False):
            return APIResponse("Category name already exists",400,False)
        Category.objects.create(name=name,description=description,image=image,created_by_id=4,updated_by_id=4)
        return APIResponse("Category created successfully",200,True)
    
    def put(self,request):
        data = j.loads(request.body.decode('utf-8'))
        category_id = data['category_id']
        name = data['name']
        if Category.objects.filter(name=name,is_deleted=False).exclude(id=category_id):
            return APIResponse("Category name already exists",400,False)
        Category.objects.filter(id=category_id).update(name=name,updated_by_id=4)
        return APIResponse("Category updated successfully",200,True)

    def delete(self,request):
        category_id = request.GET.get('category_id')
        if not Category.objects.filter(id=category_id):
            return APIResponse("Provided category is not exists",400,False)
        Category.objects.filter(id=category_id).delete()
        return APIResponse("Category deleted successfully",200,True)

class ItemsView(APIView):
    def get(self,request):
        item_objs = Items.objects.all()
        if request.GET.get('category_id'):
            item_objs = Items.objects.filter(category_id= request.GET.get('category_id'))
        if  request.GET.get('item_id'):
            item_objs = Items.objects.filter(id= request.GET.get('item_id'))
        serialized_data = ItemsSerializers(item_objs,many=True).data
        return APIResponse(serialized_data,200,True)

    def post(self,request):
        data = j.loads(request.body.decode('utf-8'))
        category_id = data['category_id']
        item_type = data['item_type']
        name = data['name']
        price = data['price']
        description = data['description']
        image = data['image']
        if Items.objects.filter(name=name,item_type=item_type,is_deleted=False):
            return APIResponse("Item already exists",400,False)
        Items.objects.create(category_id=category_id,name=name,price=price,item_type=item_type,image=image,description=description,created_by_id=4,updated_by_id=4)
        return APIResponse("Item added successfully",200,True)
    
    def put(self,request):
        data = j.loads(request.body.decode('utf-8'))
        item_id = data['item_id']
        category_id = data['category_id']
        item_type = data['item_type']
        name = data['name']
        price = data['price']
        description = data['description']
        image = data['image']
        if Items.objects.filter(name=name,item_type=item_type,is_deleted=False).exclude(id=item_id):
            return APIResponse("Category name already exists",400,False)
        Items.objects.filter(id=item_id).update(category_id=category_id,description=description,image=image,price=price,name=name,item_type=item_type,updated_by_id=request.user.id)
        return APIResponse("Item updated successfully",200,True)

    def delete(self,request):
        item_id = request.GET.get('item_id')
        if not Items.objects.filter(id=item_id):
            return APIResponse("Provided item is not exists",400,False)
        Items.objects.filter(id=item_id).delete()
        return APIResponse("Item deleted successfully",200,True)

class Cartview(APIView):
    def get(self,request):
        cart_object = Mycart.objects.filter(created_by_id=request.user.id)
        serialized_data = CartSerializers(cart_object,many=True).data
        return APIResponse(serialized_data,200,True)

    def post(self,request):
        data = j.loads(request.body.decode('utf-8'))
        item = data['item']
        quantity = data['quantity']
        price = (Items.objects.filter(id=item).price * int(quantity))
        Mycart.objects.create(item_id=item,quantity=quantity,price=price,created_by_id=request.user.id)
        return APIResponse("Item added to cart successfully",200,True)

    def put(self,request):
        data = j.loads(request.body.decode('utf-8'))
        cart_id = data['cart_id']
        item = data['item']
        quantity = data['quantity']
        price = (Items.objects.filter(id=item).price * int(quantity))
        Mycart.objects.filter(id=cart_id,item_id=item,created_by_id=request.user.id).update(quantity=quantity,price=price)
        if int(quantity) == 0:
            Mycart.objects.filter(item_id=item,created_by_id=request.user.id).delete()
        return APIResponse("Cart updated successfully",200,True)

    def delete(self,request):
        if request.GET.get('cart_id'):
            Mycart.objects.filter(id=request.GET.get('cart_id')).delete()
        return APIResponse("Item removed from cart",200,True)

class OrderView(APIView):
    def get(self,request):
        order_obj = Order.objects.all()
        if request.GET.get('user_id'):
            order_obj = Order.objects.filter(created_by_id=request.GET.get('user_id'))
        if request.GET.get('order_id'):
            order_obj = Order.objects.filter(id=request.GET.get('order_id'))
        serialized_data = OrderSerializers(order_obj,many=True).data
        return APIResponse(serialized_data,200,True)

    def post(self,request):
        user_id = request.data['user_id']
        order_obj = Order.objects.create(created_by_id=user_id)
        cart_obj = Mycart.objects.filter(created_by_id=user_id)
        for cart_item in cart_obj:
            OrderHistory.objects.create(item=cart_item.item,quantity=cart_item.quantity,order_id=order_obj.id,price =order_obj.price)
        cart_obj.delete()
        return APIResponse("Order created successfully",200,True)

    #need to work 
    def put(self,request):
        items_to_update_instances = []
        item_ids = []
        for item_data in request.data['data']:
            item_id = item_data['id']
            item_ids.append(item_data['id'])
            try:
                item = OrderHistory.objects.get(id=item_id)
                for field, value in item_data.items():
                    setattr(item, field, value)
                items_to_update_instances.append(item)
            except OrderHistory.DoesNotExist:
                pass
        if items_to_update_instances:
            OrderHistory.objects.bulk_update(items_to_update_instances, ['quantity', 'order_id', 'item_id'])
            OrderHistory.objects.filter(order_id=item.order_id).exclude(id__in=item_ids).delete()
        return APIResponse("Order updated successfully",200,True)

class FavouriteView(APIView):
    def get(self,request):
        if request.GET.get('user_id'):
            fav_obj = Favourite.objects.filter(created_by_id=request.GET.get('user_id')).values_list('item',flat=True)
            item_obj = Items.objects.filter(id__in =fav_obj)
        serialized_data = ItemsSerializers(item_obj,many=True).data
        return APIResponse(serialized_data,200,True)
    
    def post(self,request):
        data = j.loads(request.body.decode('utf-8'))
        item = data['item']

        if Favourite.objects.filter(item_id=item,created_by_id=request.user.id):
            Favourite.objects.filter(item_id=item,created_by_id=request.user.id).delete()
            return APIResponse("Item removed to your favourite successfully",200,True)
        else:
            Favourite.objects.create(item_id=item,created_by_id=request.user.id)
            return APIResponse("Item added to your favourite successfully",200,True)

class PaymentView(APIView):
    def get(self,request):
        try:
            print(PaymentHistory.objects.filter(order_id=request.GET.get("order_id")),"_______")
            latest_payment = PaymentHistory.objects.filter(order_id=request.GET.get("order_id")).latest('payment_order_id')
        except PaymentHistory.DoesNotExist:
            pass
            # raise Http404("PaymentHistory not found for the specified order_id.")
        print(latest_payment.payment_order_id,"***********")
        return APIResponse(client.order.fetch("order_Mz2tNbA0TaGct2"),200,True)

    def post(self,request):
        order_id = request.data['order_id']
        order_obj = Order.objects.filter(id=order_id)
        response = client.order.create({
            "amount": int(order_obj.last().total_amount),
            "currency": "INR"
            })
        if response['id']:
            PaymentHistory.objects.create(order_id=order_id,payment_order_id=response['id'],amount=response['amount'],currency=response["currency"],status=response["status"])
            order_obj.update(status=response['status'])
        return APIResponse(response,200,True)
        
