from re import U
from rest_framework import viewsets
from rest_framework import generics
from .models import User
from .serializers import (
    UserSerializer,
    UserCreateSerializer,
    LoginSerializer,
    UpdateUserSerializer,
    ChangePasswordSerializer,
    LogoutSerializer,
    UserViewSerializer,
)
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView
from user.user_permission import UserPermission

# Create your views here.


class UserListView(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.filter(is_active=True).exclude(
        username="admin", email="admin@gmail.com"
    )
    filter_backends = [OrderingFilter, SearchFilter]
    search_fields = ["username"]
    ordering_fields = ["id", "username"]
    serializer_class = UserViewSerializer
    permission_classes = [UserPermission]


class UserViewset(viewsets.ModelViewSet):
    queryset = User.objects.exclude(username="admin", email="admin@gmail.com")
    http_method_names = ["get", "post", "retrive"]
    filter_backends = [
        SearchFilter,
        OrderingFilter,
        DjangoFilterBackend,
    ]
    search_fields = ["username", "employee_id"]
    filterset_fields = ["username", "employee_id"]
    ordering_fields = ["id", "username", "employee_id"]
    permission_classes = [UserPermission]

    def get_serializer_class(self):
        if self.action == "list":
            return UserSerializer
        if self.action == "create":
            return UserCreateSerializer
        return UserSerializer


class UpdateUserViewset(viewsets.ModelViewSet):
    queryset = User.objects.exclude(username="admin", email="admin@gmail.com")
    http_method_names = ["put", "patch"]
    serializer_class = UpdateUserSerializer
    permission_classes = [UserPermission]

    def partial_update(self, request, pk=None):
        print(request.data, "data")
        user_object = User.objects.get(id=pk)
        serializer = self.serializer_class(
            user_object, data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginViewset(APIView):
    def get_queryset(self):
        return User.objects.all()

    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid(raise_exception=True):
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLogout(APIView):
    """
    view for user logout
    """

    permission_classes = [AllowAny]
    serializer_class = LogoutSerializer

    def get_queryset(self):
        return User.objects.all()

    def post(self, request):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"Logout successful"}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(generics.UpdateAPIView):
    """
    view for change password for user
    """

    permission_classes = [AllowAny]
    queryset = User.objects.all()
    serializer_class = ChangePasswordSerializer
