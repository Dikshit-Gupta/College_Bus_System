from rest_framework import serializers
from .models import User

class RegisterSerializer(serializers.ModelSerializer):
     class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name", "role", "phone", "password"]
        extra_kwargs = {
            "password": {"write_only": True}  # password won’t be returned in response
        }

     def create(self, validated_data):
        password = validated_data.pop("password")   # remove password from dict
        user = User(**validated_data)               # create user object
        user.set_password(password)                 # hash password securely
        user.save()
        return user