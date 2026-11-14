from rest_framework import serializers

from .models import User, username_validator


class UserSerializer(serializers.ModelSerializer):
    role = serializers.CharField(source="role.name", read_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "email", "role"]


class OrganizationRegisterSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=150, validators=[username_validator])
