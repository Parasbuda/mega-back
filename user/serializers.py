from dataclasses import fields
from statistics import mode
from rest_framework import serializers

from core.models import Branch

from .models import User
from util.get_current_user import current_user
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed


class BranchDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = "__all__"


class UserViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username"]


class UserSerializer(serializers.ModelSerializer):
    user_branch = BranchDetailSerializer()

    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "middle_name",
            "last_name",
            "gender",
            "group",
            "user_branch",
            "employee_id",
            "email",
            "username",
            "is_staff",
            "is_superuser",
            "is_active",
            "created_date_ad",
            "created_date_bs",
            "created_by",
            "name",
        ]


class UserCreateSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "middle_name",
            "last_name",
            "gender",
            "group",
            "user_branch",
            "employee_id",
            "email",
            "username",
            "password",
            "confirm_password",
            "is_staff",
            "is_superuser",
            "is_active",
            "created_date_ad",
            "created_date_bs",
            "created_by",
            "name",
            "last_login",
        ]
        read_only_fields = [
            "created_date_ad",
            "created_date_bs",
            "created_by",
            "name",
            "last_login",
        ]

    def create(self, validated_data):
        user = current_user(self.context)
        validated_data.pop("confirm_password")
        first_name = validated_data["first_name"]
        middle_name = validated_data["middle_name"]
        last_name = validated_data["last_name"]
        if middle_name == "":
            full_name = f"{first_name} {last_name}"
        else:
            full_name = f"{first_name} {middle_name} {last_name}"
        user = User.objects.create_user(
            **validated_data, name=full_name, created_by=user
        )
        return user


class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "first_name",
            "middle_name",
            "last_name",
            "gender",
            "user_branch",
            "employee_id",
            "email",
            "username",
            "is_active",
            "created_date_ad",
            "created_date_bs",
            "created_by",
            "name",
            "last_login",
            "group",
        ]
        read_only_fields = [
            "created_date_ad",
            "created_date_bs",
            "created_by",
            "name",
            "last_login",
        ]


# class PermissionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = UserPermission
#         fields = ["id", "code_name"]


# class GroupSerializer(serializers.ModelSerializer):
#     permissions = PermissionSerializer(many=True, read_only=True)

#     class Meta:
#         model = UserGroup
#         fields = ["id", "name"]


class LoginSerializer(serializers.ModelSerializer):
    tokens = serializers.SerializerMethodField()
    username = serializers.CharField(max_length=50, min_length=3)
    password = serializers.CharField(max_length=68, min_length=4, write_only=True)

    # to obtain the value of tokens
    def get_tokens(self, obj):
        user = User.objects.get(username=obj["username"])
        refresh = RefreshToken.for_user(user)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }

    class Meta:
        model = User
        fields = ["id", "username", "tokens", "is_superuser", "password", "group"]
        read_only_fields = ["password", "tokens", "group"]

    def validate(self, attrs):
        username = attrs.get("username", "")
        password = attrs.get("password", "")
        tokens = attrs.get("tokens", "")

        user = authenticate(username=username, password=password)

        if not user:
            raise AuthenticationFailed("invalid credential,try again")
        if not user.is_active:
            raise AuthenticationFailed("User is in active")

        if int(user.group) == 1:
            group_name = {"id": 1, "name": "ADMIN"}
        elif int(user.group) == 2:
            group_name = {"id": 2, "name": "STAFF"}
        else:
            group_name = {"id": 3, "name": "MAINTAINER"}
        return {
            "username": user.username,
            "id": user.id,
            "is_superuser": user.is_superuser,
            "tokens": tokens,
            "group": group_name,
        }


class LogoutSerializer(serializers.Serializer):
    """
    serializer for user logout
    """

    refresh = serializers.CharField()

    def validate(self, attrs):
        self.token = attrs["refresh"]
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except:
            raise serializers.ValidationError({"bad token"})


class ChangePasswordSerializer(serializers.ModelSerializer):
    """
    serializer class for change password for user
    """

    password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)
    old_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ("old_password", "password", "confirm_password")
        extra_kwargs = {
            "old_password": {"required": True},
            "password": {"required": True},
            "confirm_password": {"required": True},
        }

    def validate_password(self, password):
        """
        Method for validate user password
        """
        if len(password) < 6:
            serializers.ValidationError("Password must be at least 6 characters")
        if len(password) > 32:
            serializers.ValidationError("password must be max 32 characters")
        if str(password).isalpha():
            serializers.ValidationError(
                "password must contain at least alphabets and numbers"
            )
        return password

    def validate(self, attrs):
        user = self.context["request"].user
        try:
            if not user.check_password(attrs["old_password"]):
                raise serializers.ValidationError(
                    {"old_password": "Old password is not correct"}
                )
        except KeyError:
            raise serializers.ValidationError(
                {"key_error": "please provide old_password"}
            )

        try:
            if attrs["password"] != attrs["confirm_password"]:
                raise serializers.ValidationError(
                    {"password": "Password fields didn't match."}
                )
        except KeyError:
            raise serializers.ValidationError(
                {"key_error": "please provide password and confirm_password"}
            )
        return attrs

    def update(self, instance, validated_data):
        """
        function for update password for user
        """
        instance.set_password(validated_data["password"])
        instance.save()

        return instance
