from typing import Iterable
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import RegisterSerializer, LoginSerializer , UserSerializer , ChangePassSerializer
from .models import User
from django.contrib.auth import authenticate
from .permissions import IsActive
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = get_tokens_for_user(user)
            return Response({'msg':'registration successful','data':serializer.data,'token':token},status=201)
        return Response({'error':serializer.errors},status=400)

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            user = authenticate(username=email,password=password)
            if user:
                token = get_tokens_for_user(user)
                return Response({'msg':'login success','data':{'email':user.email,'name':user.name,'role':user.role,'token':token}},status=200)
            return Response({'error':'Email or Password is not valid'}, status=404)
        return Response({'error':serializer.errors}, status=400)
           
class UserView(APIView):
    def get(self,request):
        paramId = request.query_params.get("id")
        paramRole = request.query_params.get("role")
        paramName = request.query_params.get("name")
        if not paramId and not paramName and not paramRole:
            users = User.objects.all()
            serializer = UserSerializer(instance=users, many=True)
            return Response({'data':serializer.data},status=200)
        # if paramId:
        #     users1 = User.objects.get(id=paramId)
        #     serializer1 = UserSerializer(instance=users1)
        #     return Response({'data':serializer1.data},status=200)
        # if paramRole:
        #     users2 = User.objects.get(role=paramRole)
        #     print(isinstance(users2, Iterable))
        #     # serializer2 = UserSerializer(instance=users2)
        #     # return Response({'data':serializer2.data},status=200)
        return Response({'msg':'not working yet for params'})

class ChangePassView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = ChangePassSerializer(data=request.data, context={'user':request.user} )
        if serializer.is_valid():
            return Response({'msg':'password changed successfuly'},status=201)
        return Response({'error':serializer.errors},status=400)
        
            