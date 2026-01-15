from django.db import models
import uuid
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)
# Create your models here.
class AppUserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError("Username is required!")
        if not password:
            raise ValueError("Password is required!")

        extra_fields.setdefault("is_active", True)
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_staff", True)

        return self.create_user(username, password, **extra_fields)


class AppUser(AbstractBaseUser):
    

    id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable =False)
    username = models.CharField( max_length=100, blank=True, null=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    name = models.CharField(max_length=100, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name", "password", "username"]

    objects = AppUserManager()

    def __str__(self):
        return self.name or self.phone or self.email

    def has_module_perms(self, app_label):
        return True

    def has_perm(self, perm, obj=None):
        return True

class Employee(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    department = models.CharField(max_length=255, choices=(
    ('HR','HR'),
    ('Engineering','Engineering'),
    ('Sales','Sales')
    ), blank=True, null=True)
    
    role = models.CharField(max_length=255,choices=(
        ('Manager','Manager'),
        ('Developer','Developer'),
        ('Analyst','Analyst'))
        ,blank=True, null=True)
    date_joined = models.DateField(auto_now_add=True)


    def __str__(self):
        return f"{self.name} with email {self.email}"

    class Meta:
        db_table='employee_table'
        verbose_name='Employee'
        verbose_name_plural='Employees'
        ordering = ['name']