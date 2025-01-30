from rest_framework import serializers
from .models import User, Project, Task, Client
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from .utils import Util
import os

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email','name','password','role','job']
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
        # user.is_active = False
        user.save()
        return attrs


class PassResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    class Meta:
        fields = ['email']

    def validate(self, attrs):
        email = attrs.get('email')
        print(email)
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.email))
            print('encoded uemail', uid)
            token = PasswordResetTokenGenerator().make_token(user)
            print('password reset token', token)
            link = 'http://localhost:3000/users/reset/'+uid+'/'+token
            print('password reset link',link)
            body = 'Click following link to reset your password '+link
            data ={
                'subject': 'Reset Your password',
                'body':body,
                'to_email': user.email
            }
            # print(os.environ.get('USER_EMAIL'))
            # Util.send_email(data)
            return link
        else:
            raise serializers.ValidationError('You are not a registered user')

class UserPasswordResetSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255, style = {'input_type':'password'},write_only=True)
    password2 = serializers.CharField(max_length=255, style = {'input_type':'password'},write_only=True)
    class Meta:
        fields=['password','password2']
    def validate(self, attrs):
       try:
        password = attrs.get('password')
        password2 = attrs.get('password2')
        uid = self.context.get('uid')
        token = self.context.get('token')
        if password != password2:
            raise serializers.ValidationError("password and confirm password does not match")
        id=smart_str(urlsafe_base64_decode(uid))
        user=User.objects.get(email=id)
        if not PasswordResetTokenGenerator().check_token(user,token):
            raise serializers.ValidationError('Token is not valid or expired')
        user.set_password(password)
        user.save()
        return attrs
       except DjangoUnicodeDecodeError as identifier:
        PasswordResetTokenGenerator().check_token(user,token)
        raise serializers.ValidationError('token is not valid or expired')

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = "__all__"
   
class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = "__all__"

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = "__all__"