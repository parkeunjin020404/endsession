from dj_rest_auth.registration.serializers import RegisterSerializer
from allauth.account.adapter import get_adapter
from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import CustomUser
from django.contrib.auth import get_user_model
from board.models import Board



class CustomRegisterSerializer(RegisterSerializer):
    nickname = serializers.CharField(max_length=100)
    university = serializers.CharField(max_length=50)

    
    def get_cleaned_data(self):
        super(CustomRegisterSerializer, self).get_cleaned_data()
        return {
            'username': self.validated_data.get('username', ''),
            'password1': self.validated_data.get('password1', ''),
            'password2': self.validated_data.get('password2', ''),
            'nickname': self.validated_data.get('nickname', ''),
            'university': self.validated_data.get('university', ''),
        }
    
    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        user.username = self.cleaned_data.get('username')
        user.nickname = self.cleaned_data.get('nickname')
        user.university = self.cleaned_data.get('university')
        user.save()
        adapter.save_user(request, user, self)
        return user
    


class CustomUserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username']

# member/serializers.py


class RegisterSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'password1', 'password2', 'university']

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        user = CustomUser(
            username=validated_data['username'],
            university=validated_data['university']
        )
        user.set_password(validated_data['password1'])
        user.save()
        return user
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(username=data['username'], password=data['password'])
        if user is None:
            raise serializers.ValidationError("Invalid username/password.")
        return user
    
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'password', 'nickname', 'university']
        read_only_fields = ['id', 'username', 'nickname', 'university']
        extra_kwargs = {'password': {'write_only': False, 'read_only': True}}

User = get_user_model()

class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'nickname', 'university']

class UserPostSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%Y-%m-%d")
    class Meta:
        model = Board
        fields = ['id', 'user','title',  'created_at']

class UserPostSerializer2(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ['id',  'nickname']