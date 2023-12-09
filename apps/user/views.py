from django.shortcuts import render
from rest_framework.views import APIView
from CampusCrave.generics.helpers import *
import json as j
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth import authenticate,login
from django.views.decorators.csrf import csrf_exempt
from .models import *
from .serializers import *
import random
from django.contrib.auth.hashers import make_password,check_password
from CampusCrave.generics.permissions import *
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from CampusCrave.settings import *
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import ( smart_str, force_str,force_bytes, smart_bytes,
                                  DjangoUnicodeDecodeError )
from django.contrib.auth.tokens import default_token_generator

@csrf_exempt
def loginapi(request):
    requestData = j.loads(request.body.decode('utf-8'))
    role = requestData['role']
    email = requestData['email']
    password = requestData['password']
    user = authenticate(email=email, password=password)
    
    if user is not None:
        if not User_Profile.objects.filter(email=email,is_verified=True):
            return APIResponse("Please verify otp",400,False)
        login(request, user)
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        data = {"access_token": access_token, "refresh_token": str(refresh)}
        return APIResponse(data, 200,True)
    else:
        return APIResponse('Invalid credentials', 200,True)

class Register(APIView):

    def dispatch(self,request,*args,**kwargs):
        return super(Register,self).dispatch(request, *args, **kwargs)
    
    def post(self,request):
        datas = j.loads(request.body.decode('utf-8'))
        first_name = datas['first_name']
        if not first_name:
            return APIResponse('first name is Required', 400, False)
        last_name = datas['last_name']
        email = datas['email']
        if not email:
            return APIResponse('email is Required', 400, False)
        role = "Customer"
        phone_number = datas['phone_number']
        password = datas['password']
        if not password:
            return APIResponse('password is Required', 400, False)
        phone_number = datas['phone_number']
        if not phone_number:
            return APIResponse('phone_number is Required', 400, False)
        if User_Profile.objects.filter(email=email):
            return APIResponse('email already exists', 400, False)
        digits = '0123456789'
        length = 4
        otp = ''.join(random.choice(digits) for _ in range(length))
        user_obj = User_Profile(firstname=first_name,lastname=last_name,role=role,email=email,password=make_password(password),phone_number=phone_number,otp=1234)
        user_obj.save()
        # Generate the activation URL
        # user = User_Profile.objects.get(email=email)
        # activation_url = f"http://{BASE_URL}/activate/{urlsafe_base64_encode(force_bytes(user.id))}/{default_token_generator.make_token(user)}/"

        # # Create the text and HTML versions of the email content
        # text_content = f"Hello {user.firstname}, Click the following link to activate your account: {activation_url}"
        # html_content = render_to_string("activation_email.html", {'name': user.firstname, 'activation_url': activation_url})

        # # Create the email message
        # subject = 'Activate Your Account'
        # from_email = "mailfrombackend@gmail.com"
        # recipient_list = [email]

        # msg = EmailMultiAlternatives(subject, text_content, from_email, recipient_list)
        # msg.attach_alternative(html_content, "text/html")  # Attach the HTML content

        # # Send the email
        # msg.send()
        return APIResponse("Registration successful, We have sent an email for verification",200, True)

class Resend_otp(APIView):
    def post(self,request):
        email = request.data['email']
        if not User_Profile.objects.filter(email=email):
            return APIResponse("Please provide valid email id",400,False)
        digits = '0123456789'
        length = 4
        otp = ''.join(random.choice(digits) for _ in range(length))
        User_Profile.objects.filter(email=email).update(otp=otp)
        return APIResponse("OTP send to your registered mobile number",200,True)
class Update_password(APIView):
    @csrf_exempt
    def post(self,request):
        data = j.loads(request.body.decode('utf-8'))
        email = data['email']
        userCurrentPassword = data['old_password']
        userNewPassword = data['new_password']
        if userCurrentPassword and userNewPassword and email:
            user = User_Profile.objects.get(email=email)
            if user:
                if user.check_password(userCurrentPassword):
                    if userNewPassword != userCurrentPassword:
                        user.password=make_password(userNewPassword)
                        user.save()
                        user = User_Profile.objects.get(email=email)
                        user.password = make_password(userNewPassword)
                        user.save()
                    else:
                        return APIResponse("Old password and newpassword should not be same",400, False)
                else:
                    return APIResponse("Old password doesn't match",400, False)
            else:
                return APIResponse('User not exist',400, False)
        else:
            return APIResponse('Please enter valid credentials',400, False)
        return APIResponse('Your password changed successfully',200,True)           
  
@csrf_exempt 
def resetpassword(request):
    data = j.loads(request.body.decode('utf-8'))
    email = data['email']
    if User_Profile.objects.filter(email=email).exists()==False:
        return APIResponse("Please enter the valid email",400,False)
    associated_users = User_Profile.objects.filter(email=email)
    if associated_users.exists():
            for user in associated_users:
                email_template_name = "forgot_password.html"
                subject = "Reset your Account password" 

                # Generate the reset password URL
                reset_password_url = BASE_URL + f"/reset/{urlsafe_base64_encode(smart_bytes(user.id))}/{default_token_generator.make_token(user)}"

                # Create the text and HTML versions of the email content
                text_content = f"Hello, To reset your password, click the following link: {reset_password_url}"
                html_content = render_to_string(email_template_name, {'new_password_url': reset_password_url, 'ip': ip})

                # Create the email message
                from_email = EMAIL_HOST_USER  # Replace with your email sender address
                recipient_list = [user.email]

                msg = EmailMultiAlternatives(subject, text_content, from_email, recipient_list)
                msg.attach_alternative(html_content, "text/html")  # Attach the HTML content

                # Send the email
                msg.send()      
            return APIResponse("Please check your registered email inbox to reset your password",200,True)

def resettemplates(request,uidb64,token):
    return render(request,"reset_password.html",{"ip":ip})

def verified(request):
    return render(request,"password_reset_complete.html",{"ip":ip})

@csrf_exempt
def save_reset_password(request):
    import json as j
    if request.method == 'POST':
        password = request.POST.get('new_password')
        cf_password = request.POST.get('confirm_password')
        token = request.POST.get('token')
        uidb64 = request.POST.get('uidb64')
        id=smart_str(urlsafe_base64_decode(uidb64))
        subject="Password created"
        # content = {"reset_link":f"http://localhost:8000/admin/login/?next=/admin/"}
        content = {'ip':ip}
        if(password and cf_password ):

            try:
                user = User_Profile.objects.get(id=id)
                email= User_Profile.objects.get(id=id).email          
            except:
                return APIResponse("Given userid  is not found for reset password",401,False) 
           
            try:
                set=PasswordResetTokenGenerator().check_token(user,token)
            except:
                return APIResponse('Please provide valid token',401,False)
           
            if(set==True):
                if(password==cf_password):
                    user.password=make_password(password)
                    user.save()
                    # html_content = render_to_string('confirm password.html', content)
                    # sendCustomMail(content,email,subject,html_content)
                    # if user.role == "1":
                    #     url =  f"{ip}/login"
                    # else:
                    #     url = f"{ip}/home"
                    response = {"msg":"success","ip":ip}

                    return APIResponse(response,200,True)
                else:
                  return APIResponse("Given password is wrong",401,False)
            else:
                return APIResponse({"msg":"fail","ip":ip},200,False)

        else:
            return APIResponse("New password and confirm password is not matching",401,False)   


class Dashboard_api(APIView):
    permission_classes=[IsUser]
    def get(self,request):
        
        return APIResponse("data",200,True)


class Profile(APIView):
    # permission_classes=[IsUser]
    def get(self,request):
        if request.GET.get('id'):
            data = User_Profile.objects.filter(id=request.GET.get('id'))
        if request.GET.get('user'):
            data = User_Profile.objects.filter(role="Customer")
        serializers = UserSerializer(data,many=True).data
        return APIResponse(serializers,200,True)

    def put(self,request):
        data = j.loads(request.body.decode('utf-8'))
        id = data['id']
        firstname = data['firstname']
        lastname = data['lastname']
        country_code = data['country_code']
        phone_number = data['phone_number']
        User_Profile.objects.filter(id=id).update(firstname=firstname,lastname=lastname,country_code=country_code,phone_number=phone_number)
        return APIResponse("Profile updated successfully",200,True)
    
class BlockAndUnblock(APIView):
    def get(self,request):
        id = request.GET.get('id')
        user_obj = User_Profile.objects.filter(id=id)
        if user_obj.latest().is_active == True:
            user_obj.update(is_active=False)
            return APIResponse("User unblocked successfully",200,True)
        else:
            user_obj.update(is_active=True)
            return APIResponse("User blocked successfully",200,True)

class Verify_otp(APIView):
    # permission_classes=[IsUser]
    def post(self,request):
        email = request.data['email']
        otp = request.data['otp']
        data = User_Profile.objects.filter(email=email,otp=otp)
        if data:
            data.update(is_verified=True)
        else:
            return APIResponse("Please provide valid otp",400,False)
        return APIResponse("Otp verified successfully",200,True)



import razorpay
client = razorpay.Client(auth=("rzp_test_FlBgzH672A0qLj", "MEzOs5ltbeyG37eYpGuy63AQ"))

# DATA = {
#     "amount": 100,
#     "currency": "INR",
#     "receipt": "receipt#1",
#     "notes": {
#         "key1": "value3",
#         "key2": "value2"
#     }
# }
# dd = client.order.create(data=DATA)
# print(dd)


# {'id': 'order_Mz2tNbA0TaGct2', 'entity': 'order', 'amount': 100, 'amount_paid': 0, 'amount_due': 100, 'currency': 'INR', 'receipt': 'receipt#1', 'offer_id': None, 'status': 'created', 'attempts': 0, 'notes': {'key1': 'value3', 'key2': 'value2'}, 'created_at': 1699679239}