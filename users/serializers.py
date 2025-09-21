from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile

class PublicProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['profile_picture']

class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    
    followers = serializers.SerializerMethodField() 

    following = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'profile', 'followers', 'following']
        read_only_fields = ['id', 'followers', 'following']

    def get_following(self, obj):
       
        return PublicProfileSerializer(obj.profile.following.all(), many=True).data

    
    def get_followers(self, obj):
        
        follower_users = [profile.user for profile in obj.followers.all()]
        return PublicProfileSerializer(follower_users, many=True).data

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', None)
        if profile_data:
            profile_serializer = ProfileSerializer(instance.profile, data=profile_data, partial=True)
            if profile_serializer.is_valid(raise_exception=True):
                profile_serializer.save()

        return super().update(instance, validated_data)

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'first_name', 'last_name', 'email')
        extra_kwargs = {'password': {'write_only': True}}
    def create(self, validated_data):
        return User.objects.create_user(
            username=validated_data['username'], password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            email=validated_data.get('email', '')
        )