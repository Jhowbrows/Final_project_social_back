from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile

class PublicProfileSerializer(serializers.ModelSerializer):
    profile_picture = serializers.ImageField(source='profile.profile_picture', read_only=True)
    followers_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()
    
    
    followers = serializers.SerializerMethodField()
    following = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 'username', 'first_name', 'last_name', 
            'profile_picture', 'followers_count', 'following_count',
            'followers', 'following' 
        ]

    def get_followers_count(self, obj):
        return obj.followers.count()

    def get_following_count(self, obj):
        return obj.profile.following.count()

    
    def get_followers(self, obj):
        
        follower_users = [profile.user for profile in obj.followers.all()]
        return [{'id': user.id, 'username': user.username} for user in follower_users]

    def get_following(self, obj):
        
        following_users = obj.profile.following.all()
        return [{'id': user.id, 'username': user.username} for user in following_users]

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['profile_picture']

class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()
    profile_picture = serializers.ImageField(source='profile.profile_picture', read_only=True)
    followers = serializers.SerializerMethodField() 
    following = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'profile', 'profile_picture','followers', 'following']
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
    

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)