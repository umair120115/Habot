from django.contrib import admin
from .models import Employee, AppUser
admin.site.register(AppUser)
admin.site.register(Employee)
# Register your models here.
