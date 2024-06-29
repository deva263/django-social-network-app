from rest_framework import serializers
from .models import User, FriendRequest


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User model.

    This serializer handles the serialization and deserialization of User model instances,
    and includes fields for id, email, first_name, last_name, is_active, is_staff, and date_joined.
    """
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'is_active', 'is_staff', 'date_joined')


class SignupSerializer(serializers.ModelSerializer):
    """
    Serializer for user signup.

    This serializer handles the creation of new users and includes fields for email, first_name, and last_name.
    """
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')


class PasswordResetSerializer(serializers.Serializer):
    """
    Serializer for password reset.

    This serializer handles the password reset functionality and includes fields for email and new_password.
    """
    email = serializers.EmailField()
    new_password = serializers.CharField(write_only=True)


class UserSearchSerializer(serializers.Serializer):
    """
    Serializer for user search.

    This serializer handles the search functionality for users and includes a search_keyword field.
    The search_keyword can be used to search by email or name.
    """

    search_keyword = serializers.CharField(max_length=100, required=True, help_text="Search by email or name")


class FriendRequestSerializer(serializers.ModelSerializer):
    """
    Serializer for FriendRequest model.

    This serializer handles the serialization and deserialization of FriendRequest model instances,
    and includes all fields of the FriendRequest model.
    """
    class Meta:
        model = FriendRequest
        fields = '__all__'

