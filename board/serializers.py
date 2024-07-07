from rest_framework import serializers
from .models import Board
from .models import Comment
from member.serializers import CustomUserDetailSerializer, UserPostSerializer2

class CommentSerializer(serializers.ModelSerializer):
    user = CustomUserDetailSerializer() 
    created_at = serializers.DateTimeField(format="%Y-%m-%d")
    class Meta:
        model = Comment
        fields = ['id','user','comment','created_at']


class CommentSerializer2(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id','user','comment']
        

class BoardDetailSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    created_at = serializers.DateTimeField(format="%Y-%m-%d")
    #user = CustomUserDetailSerializer()
    nickname = serializers.SerializerMethodField()
    class Meta:
        model = Board
        fields = ['id', 'user', 'nickname','title', 'body','created_at','comments']
    def get_nickname(self, obj):
        return obj.user.nickname
        

class BoardCreateSerializer(serializers.ModelSerializer): #만들때
    class Meta:
        model = Board
        fields = ['id','title','body']

class BoardSimpleSerializer(serializers.ModelSerializer):
    user = CustomUserDetailSerializer()
    #nickname = serializers.SerializerMethodField()
    class Meta:
        model = Board
        fields = ['id', 'user', 'title','body','created_at','comments']
    def get_nickname(self, obj):
        return obj.user.nickname

class BoardDetailSerializer2(serializers.ModelSerializer):
    user = CustomUserDetailSerializer()
    nickname = serializers.SerializerMethodField()

    class Meta:
        model = Board
        fields = ['id', 'user','nickname','title','body','created_at','comments']

    def get_nickname(self, obj):
        return obj.user.nickname
    
class AllBoardlist(serializers.ModelSerializer):
    user = CustomUserDetailSerializer()
    #nickname = serializers.SerializerMethodField()
    class Meta:
        model = Board
        fields = ['id', 'user', 'title','body','created_at','comments']
    def get_nickname(self, obj):
        return obj.user.nickname