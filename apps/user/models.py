from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager

class MyAccountManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("You have not provided a valid e-mailaddress")
        if not password:
            raise ValueError("You have not provide a valid password")
        email = self.normalize_email(email)
        user = self.model(email = email, **extra_fields)
        user.set_password(password)
        extra_fields.setdefault('is_verified', True)
        user.save(using = self.db)
        return user
    
    def create_user(self, email = None, password = None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)
    
    def create_superuser(self, email =None, password = None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(email, password, **extra_fields)

class User_Profile(AbstractBaseUser):
    id = models.AutoField(primary_key=True)
    firstname = models.CharField(max_length=250,null=True)
    lastname = models.CharField(max_length=250,null=True)
    email = models.CharField(max_length=250, unique=True)
    password = models.CharField(max_length=250, blank = True)
    role = models.CharField(max_length=250)
    country_code=models.CharField(max_length=5,null=True)
    phone_number = models.BigIntegerField(unique = True,null=True)
    is_active = models.BooleanField(default = True)
    is_superuser = models.BooleanField(default = False)
    is_staff = models.BooleanField(default = True)
    otp = models.CharField(max_length=250,null=True)
    is_verified = models.BooleanField(default = False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    last_login = models.DateTimeField(auto_now = True)

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = MyAccountManager()

    class Meta:
        managed = True
        db_table = "user_profile"
        get_latest_by = 'created_on'
    def __str__(self):
        return self.email