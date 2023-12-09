from django.urls import path
from .views import *

urlpatterns = [
    #COMMON
    path('login',loginapi,name='login'),
    path('update_password',Update_password.as_view(),name="password_update"),
    path('forgot_password' , resetpassword),
    path('reset/<uidb64>/<token>',resettemplates),
    path('save_password',save_reset_password ),
    path('profile',Profile.as_view()),

    
    path('register',Register.as_view(),name='register'),
    # path('dashboard_api',Dashboard_api.as_view(),name='dashboard'),
    path('verified',verified),
    path('otp_verify',Verify_otp.as_view()),
    path('resend_otp',Resend_otp.as_view()),
    path('block',BlockAndUnblock.as_view()),

]
