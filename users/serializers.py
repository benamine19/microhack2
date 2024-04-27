from rest_framework import serializers
from .models import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email','role')


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        token['id'] = user.id
        token['email'] = user.email
        token['role'] = user.role 
        # token['profile_pic'] = user.profile_pic.url
        return token



class RegisterSerializerChef(serializers.ModelSerializer):
    email = serializers.EmailField( required=True,validators=[UniqueValidator(queryset=User.objects.all())] )
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email','profile_pic')
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs
    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            role='chef',
        )
        user.set_password(validated_data['password'])
        user.save()
        chef=Chef.objects.create(user=user)
        return user
    
class TacheSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tache
        fields = "__all__"

class EmployeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employe
        fields = "__all__"
        
class TacheResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskResponse
        fields = "__all__"
