from django.urls import path
from .views import *

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', SignUpView.as_view(), name='signup'),
    path('login/' ,LoginView.as_view() , name ="login"),
    path('logout/' ,LogoutView.as_view() , name='logout'),
    path('profile/' ,UpdateUserProfileView.as_view() , name="edit_profile"),
]
