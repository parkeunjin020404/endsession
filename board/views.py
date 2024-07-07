
from .models import Board, Comment
from .serializers import BoardDetailSerializer, BoardDetailSerializer2
from .serializers import CommentSerializer
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .permissions import IsOwnerOrReadOnly
from .serializers import BoardCreateSerializer
from .serializers import BoardSimpleSerializer
from .serializers import AllBoardlist
from .serializers import CommentSerializer2
'''
전체 블로그를 조회
'''
@api_view(['GET','POST']) 
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticatedOrReadOnly])
def board_list(request):
    if request.method =='GET':
        boards = Board.objects.all()
        serializer = BoardDetailSerializer2(boards, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer = BoardCreateSerializer(data=request.data)
        if serializer.is_valid():
            board = serializer.save(user = request.user)
            result = BoardDetailSerializer2(board)
            return Response(result.data, status = status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)   
'''
한 블로그 조회
'''
@api_view(['GET','PUT','DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsOwnerOrReadOnly])
def board_detail(request, pk):
    try: 
        board = Board.objects.get(pk=pk)
        if request.method == 'GET':
            serializer = BoardDetailSerializer(board)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif request.method =='PUT':
            serializer = BoardCreateSerializer(board, data=request.data)
            if serializer.is_valid():
                board = serializer.save(user = request.user)
                result = BoardDetailSerializer2(board)
                return Response(result.data,status=status.HTTP_200_OK)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        elif request.method =='DELETE':
            board.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
    except Board.DoesNotExist: 
        return Response(status=status.HTTP_404_NOT_FOUND)
    
@api_view(['GET', 'POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsOwnerOrReadOnly])
def board_comments(request, board_id):
    try:
        board = Board.objects.get(pk=board_id)
        comment = Comment.objects.get(pk=board_id)
    except Board.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        board = Board.objects.get(pk=board_id)
        comments = board.comments.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer = CommentSerializer2(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, board=board)
            board_serializer = BoardDetailSerializer(board)
            return Response(board_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method =='DELETE':
            comment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
    