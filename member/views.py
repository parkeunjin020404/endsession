from django.shortcuts import render
from .models import CustomUser
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import authenticate
from .serializers import CustomUserSerializer
from rest_framework_simplejwt.tokens import RefreshToken
# Create your views here.
# member/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import LoginSerializer
from django.http import HttpResponse
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import UserInfoSerializer
from .serializers import UserPostSerializer
from board.models import Board
class RegisterView(APIView):
    def get(self, request, *args, **kwargs):
        # 기본값 설정
        default_data = {
            "username": "유저명",
            "password1": "비밀번호",
            "password2": "비밀번호 확인",
            "university": "재학중인 대학교"
        }
        serializer = RegisterSerializer(data=default_data)
        serializer.is_valid()
        return Response(serializer.initial_data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class LoginView(APIView):
    def get(self, request, *args, **kwargs):
        # 기본값 설정
        default_data = {
            "username": "유저명",
            "password1": "비밀번호",
        }
        serializer = RegisterSerializer(data=default_data)
        serializer.is_valid()
        return Response(serializer.initial_data, status=status.HTTP_200_OK)
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            user_data = CustomUserSerializer(user).data
            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'user': user_data
            }, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

def logout_view(request):
    response = JsonResponse({
        "detail": "Neither cookies or blacklist are enabled, so the token has not been deleted server side. Please make sure the token is deleted client side."
    })
    response.delete_cookie('jwt')  # 쿠키에서 JWT 토큰 삭제
    return response     


class UserInfoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserInfoSerializer(request.user)
        return Response(serializer.data) 
    
class UserPostView(APIView):
    permission_classes  = [IsAuthenticated]
    def get(self, request):
        posts = Board.objects.filter(user=request.user)
        serializer = UserPostSerializer(posts, many=True)
        return Response(serializer.data)