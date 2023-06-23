from django.urls import path
from .views import GroupListView, RegisterView, UserDetailView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path("<int:id>", UserDetailView.as_view(), name="user_details"),
    path("login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("login/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("register/", RegisterView.as_view(), name="sign_up"),
    path("groups/", GroupListView.as_view(), name="group_list"),
]
