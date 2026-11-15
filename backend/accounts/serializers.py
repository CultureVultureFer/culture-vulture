from rest_framework import serializers

from .models import User, username_validator


class UserSerializer(serializers.ModelSerializer):
    role = serializers.CharField(source="role.name", read_only=True)
    # Organization name; null for everyone who is not an organizer.
    # allow_null is required, otherwise the key is left out when there is no organization.
    organization = serializers.CharField(source="organization.name", read_only=True, allow_null=True)

    class Meta:
        model = User
        fields = ["id", "username", "email", "role", "organization"]


class OrganizationRegisterSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=150, validators=[username_validator])
