from django.urls import path
from .views import *

urlpatterns = [
    path('register',Register.as_view(),name='register'),
    path('login',loginapi),
    path('dashboard_api',Dashboard_api.as_view(),name='dashboard'),
    path('update_password',Update_password.as_view(),name="password_update"),
    path('reset_password' , resetpassword),
    path('reset/<uidb64>/<token>',resettemplates),
    path('verified',verified),
    path('save_password',save_reset_password ),
    path('profile',Profile.as_view()),
    path('otp_verify',Verify_otp.as_view())

]
