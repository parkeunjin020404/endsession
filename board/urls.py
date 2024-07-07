from django.urls import path
from .views import *

app_name = 'board'

urlpatterns = [
    path('', board_list, name='board_list_get'),
    path('',board_list, name='board_list_post'),
    path('<int:pk>/', board_detail, name='board_detail_get'),
    path('<int:pk>/', board_detail, name='board_detail_put'),
    path('<int:pk>/', board_detail, name='board_detail_delete'),
    path('<int:board_id>/comment/',board_comments, name='board_comments_get'),
    path('<int:board_id>/comment/', board_comments, name='board_comments_post'),
]