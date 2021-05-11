from .models import MyBackend
from django.contrib.auth.password_validation import validate_password
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from rest_framework import exceptions, serializers
from rest_framework.validators import UniqueValidator

from .models import MyUser


class RegisterSerializer(serializers.ModelSerializer):
    
    email = serializers.EmailField(
        required=True, validators=[UniqueValidator(queryset=MyUser.objects.all())]
    )

    password = serializers.CharField(write_only=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = MyUser
        fields = ["username", "email", "password", "password2"]

    def validate(self, data):
        if data["password"] != data["password2"]:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )

        return data

    def create(self, validated_data):
        user = MyUser.objects.create(
            username=validated_data["username"],
            email=validated_data["email"],
        )
        user.set_password(validated_data["password"])
        user.save()
        return user