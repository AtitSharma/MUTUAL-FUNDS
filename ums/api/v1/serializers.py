from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer,TokenRefreshSerializer,RefreshToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenBackendError, TokenError
from ums.models import User, UserInvestment
from django.utils import timezone


    

class UserLoginSuccessResponse(TokenObtainPairSerializer):

    refresh = serializers.SerializerMethodField()  
    access = serializers.SerializerMethodField()   

    def __init__(self, *args, **kwargs):
        """
        Initialize the serializer and retrieve the token 
        if a user object is passed in the arguments.
        """
        super().__init__(*args, **kwargs)
        if args:
            self.token = self.get_token(args[0])  

    def get_refresh(self, obj):
        """
        Get the refresh token string for the user
        """
        token = self.token
        return str(token)  

    def get_access(self, obj):
        """
        Get the access token string for the user
        """
        token = self.token
        return str(token.access_token) 

    @classmethod
    def get_token(cls, user):
        """
        Get the token for a specific user using the parent method
        """
        token = super().get_token(user)  
        return token


class CustomTokenRefreshSerializer(TokenRefreshSerializer):

    token_class = RefreshToken  

    @classmethod
    def get_token(cls, user):
        """
        Get the refresh token for a specific user
        """
        token = cls.token_class.for_user(user) 
        return token

    def validate(self, attrs):
        """
        Validate the refresh token and return the new access token
        """
        refresh_token = attrs["refresh"] 
        try:
            refresh = RefreshToken(refresh_token) 
        except (TokenError, TokenBackendError):
           
            raise InvalidToken

        user_id = refresh.payload.get("user_id")  

        if user_id:
            
            user = User.objects.filter(id=user_id).first()
            if not user:
                raise serializers.ValidationError("User Not Found") 
        refresh = self.get_token(user=user) 
        data = {"access": str(refresh.access_token)} 
        return data

    

class UserRegisterSerializer(serializers.ModelSerializer):
    
    password1 = serializers.CharField(write_only=True, min_length=5)  # Password input field
    password2 = serializers.CharField(write_only=True, min_length=5)  # Confirm password field

    class Meta:
        model = User  
        fields = ["id", "username", "password1", "password2"]  

    def validate_username(self, value):
        """
        Ensure the username is unique
        """
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError(f"User with such username {value} already exists.")
        return value

    def validate(self, attrs):
        """
        Validate that both password fields match and set the final password
        """
        password1 = attrs.pop("password1") 
        password2 = attrs.pop("password2")  
        if password1 != password2:
            raise serializers.ValidationError("Both password didn't match.")  
        attrs["password"] = password2 
        return super().validate(attrs) 

    def create(self, validated_data):
        """
        Create a new user and set their password correctly
        """
        user = super().create(validated_data)  
        user.set_password(validated_data.get("password"))  
        user.save()  
        return user


class UserLoginSerializer(serializers.Serializer):
    
    username = serializers.CharField() 
    password = serializers.CharField() 

    def validate(self, attrs: dict):
        """
        Validate user credentials during login
        """
        username = attrs.get("username")
        password = attrs.get("password")

        user = User.objects.filter(username=username).first() 
        if not(user and user.check_password(password)):
            raise serializers.ValidationError("User with such credentials doesn't exist")  

        user.last_login = timezone.now() 
        user.save()  

        
        response = UserLoginSuccessResponse(user)  
        return response.data


class InvestmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserInvestment  
        fields = ["id", "user", "mutual_fund", "units"] 

        extra_kwargs = {
            "user": {"read_only": True}  
        }

    def create(self, validated_data):
        """
        Create a new investment for the logged-in user
        """
        validated_data["user"] = self.context.get("request").user 
        return super().create(validated_data)  


class ReportGenerationListSerializer(serializers.Serializer):

    mutual_fund_name = serializers.CharField()  
    total_units = serializers.FloatField()  
    total_value = serializers.FloatField() 
