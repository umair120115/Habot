from rest_framework import serializers
from .models import Employee, AppUser

class AppUserSignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, style={'input_type':'password'})

    class Meta:
        model= AppUser
        fields=['id','name','email','username','password']
        extra_kwargs={
            'id':{'read_only':True}
        }
    def create(self, validated_data):
        user = AppUser.objects.create_user(
            # OPTION 1: Use .get() with PARENTHESES
            username = validated_data.get('username'), 
            email = validated_data.get('email'),
            name = validated_data.get('name'),
            password = validated_data.get('password')
        )
        return user

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields=['id','name','email','department','role','date_joined']