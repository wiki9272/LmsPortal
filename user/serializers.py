from rest_framework import serializers
from .models import User, Project
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from .utils import Util
import os

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','email','name','password','role','job']
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        extra_kwargs = {"password": {"write_only": True}}

class ChangePassSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255, style = {'input_type':'password'},write_only=True)
    password2 = serializers.CharField(max_length=255, style = {'input_type':'password'},write_only=True)
    class Meta:
        fields = ['password','password2']
    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        user = self.context.get('user')
        if password != password2:
            raise serializers.ValidationError("password and congirm password does not match")
        user.set_password(password)
        user.is_active = False
        user.save()
        return attrs


class PassResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    class Meta:
        fields = ['email']

    def validate(self, attrs):
        email = attrs.get('email')
        if User.objects.filter(email=email).exists():
            User.objects.get(email=email)

        return super().validate(attrs)
    
class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = [ 'description']
    # name = serializers.CharField(max_length=200)
    # description = serializers.CharField()
    # deadline = serializers.DateField()
    # assigned_to = serializers.EmailField()
    # assigned_to = serializers.EmailField()