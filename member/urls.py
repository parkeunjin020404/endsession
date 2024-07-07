from django.urls import path
from . import views
from .views import RegisterView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import LoginView
from .views import UserInfoView
from .views import logout_view
from .views import UserPostView

app_name = 'member'

urlpatterns = [
    path('signup/',RegisterView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', logout_view, name='logout'),
    path('info/', UserInfoView.as_view(), name='user_info'),
    path('post/', UserPostView.as_view(), name='user_posts'),
]