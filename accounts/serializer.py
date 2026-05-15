"""Serializers for the User model.

Provides serialization and deserialization of User objects for API endpoints.
Handles user data validation and secure password creation.
"""

from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    """Serializes User model instances to/from JSON.
    
    Handles conversion of User model objects to JSON and vice versa.
    Password field is write-only to ensure it's never exposed in responses.
    """
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email', 'role']
        read_only_fields = ['role']

    def create(self, validated_data):
        """Create a new user with secure password hashing.
        
        Args:
            validated_data: Dictionary containing validated user data.
        
        Returns:
            User: The newly created user object with hashed password.
        """
        user = User.objects.create_user(**validated_data)
        return user
