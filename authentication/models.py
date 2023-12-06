from django.db import models
from django.contrib.auth.models import UserManager, PermissionsMixin, AbstractUser
from django.contrib.auth.hashers import make_password,check_password
# Create your models here.


class CustomUserManager(UserManager):
    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class MyUser(AbstractUser, PermissionsMixin):
    username = None

    email = models.EmailField(unique=True)
    phone = models.IntegerField(null=True,blank=True)

    REQUIRED_FIELDS = []
    USERNAME_FIELD = "email"

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    



class OTP(models.Model):

    user = models.OneToOneField(MyUser, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    expiration_time = models.DateTimeField(blank=True,null=True)
    is_verified  = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
