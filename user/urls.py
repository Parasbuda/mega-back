from rest_framework import routers
from django.urls import path, re_path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from user.views import (
    UserListView,
    UserViewset,
    LoginViewset,
    UpdateUserViewset,
    ChangePasswordView,
    UserLogout,
)

router = routers.DefaultRouter(trailing_slash=False)
router.register("user", UserViewset)
router.register("user-list", UserListView)
router.register("update-user", UpdateUserViewset)

urlpatterns = [
    path("token", LoginViewset.as_view(), name="Token obtain view"),
    path("token/refresh", TokenRefreshView.as_view(), name="Token Refresh view"),
    path("logout", UserLogout.as_view(), name="logout"),
    path(
        "change-password/<int:pk>",
        ChangePasswordView.as_view(),
        name="auth_change_password",
    ),
    re_path(
        r"password-reset/",
        include("django_rest_resetpassword.urls", namespace="password_reset"),
    ),
] + router.urls
