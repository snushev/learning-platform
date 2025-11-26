from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import User


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, min_length=6)

    class Meta:
        model = User
        fields = ["username", "email", "password", "first_name", "last_name", "role"]

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
            first_name=validated_data.get("first_name", ''),
            last_name=validated_data.get("last_name", ''),
            profile_picture=validated_data.get("profile_picture"),
            bio=validated_data.get("bio"),
            role=validated_data.get("role", "Student"),
        )
        return user


class LoginSerializer(serializers.Serializer):
    login = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        login = data.get("login")
        password = data.get("password")
        
        try:
            if '@' in login:
                user = User.objects.get(email=login)
            else:
                user = User.objects.get(username=login)
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid credentials")
        
        if not user.check_password(password):
            raise serializers.ValidationError("Invalid credentials")

        data["user"] = user
        return data


class UserProfileSerializer(serializers.ModelSerializer):
    profile_picture = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "profile_picture",
            "bio",
            "role",
            "date_joined",
            "last_login",
        ]
        read_only_fields = ["id", "date_joined", "last_login", "username"]

    def update(self, instance, validated_data):
        profile_picture = validated_data.pop('profile_picture', None)
        
        if profile_picture:
            if instance.profile_picture:
                instance.profile_picture.delete(save=False)
            instance.profile_picture = profile_picture
        
        return super().update(instance, validated_data)