from rest_framework import status, viewsets
from rest_framework import serializers
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db import transaction
from .serializers import UserRegistrationSerializer, UserLoginSerializer, UserProfileSerializer


class UserViewSet(viewsets.GenericViewSet):
    """
    ViewSet for user authentication and profile management.
    Provides registration, login, logout, and profile operations.
    """
    queryset = User.objects.all()
    
    def get_permissions(self):
        """Set permissions based on action."""
        if self.action in ['register', 'login', 'refresh_token']:
            return [AllowAny()]
        return [IsAuthenticated()]
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action."""
        if self.action == 'register':
            return UserRegistrationSerializer
        elif self.action == 'login':
            return UserLoginSerializer
        return UserProfileSerializer
    
    @action(detail=False, methods=['post'])
    @transaction.atomic
    def register(self, request):
        """Register a new user."""
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            
            # Check if username already exists
            if User.objects.filter(username=serializer.validated_data['username']).exists():
                return Response(
                    {
                        'success': False,
                        'message': 'Username already exists'
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            
            return Response(
                {
                    'success': True,
                    'message': 'User registered successfully',
                    'data': {
                        'user': UserProfileSerializer(user).data,
                        'access': str(refresh.access_token),
                        'refresh': str(refresh)
                    }
                },
                status=status.HTTP_201_CREATED
            )
        except serializers.ValidationError as e:
            return Response(
                {
                    'success': False,
                    'message': 'Validation error',
                    'errors': e.detail
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {
                    'success': False,
                    'message': 'Registration failed',
                    'errors': str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['post'])
    def login(self, request):
        """Authenticate user and return token."""
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            
            user = authenticate(username=username, password=password)
            
            if user:
                if user.is_active:
                    refresh = RefreshToken.for_user(user)
                    return Response(
                        {
                            'success': True,
                            'message': 'Login successful',
                            'data': {
                                'user': UserProfileSerializer(user).data,
                                'access': str(refresh.access_token),
                                'refresh': str(refresh)
                            }
                        },
                        status=status.HTTP_200_OK
                    )
                else:
                    return Response(
                        {
                            'success': False,
                            'message': 'Account is disabled'
                        },
                        status=status.HTTP_401_UNAUTHORIZED
                    )
            else:
                return Response(
                    {
                        'success': False,
                        'message': 'Invalid credentials'
                    },
                    status=status.HTTP_401_UNAUTHORIZED
                )
        except Exception as e:
            return Response(
                {
                    'success': False,
                    'message': 'Login failed',
                    'errors': str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['post'])
    def logout(self, request):
        """Logout user by blacklisting refresh token."""
        try:
            refresh_token = request.data.get('refresh')
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
            
            return Response(
                {
                    'success': True,
                    'message': 'Logout successful'
                },
                status=status.HTTP_200_OK
            )
        except Exception:
            return Response(
                {
                    'success': True,
                    'message': 'Logout successful'
                },
                status=status.HTTP_200_OK
            )
    
    @action(detail=False, methods=['get'])
    def profile(self, request):
        """Get user profile."""
        serializer = UserProfileSerializer(request.user)
        return Response(
            {
                'success': True,
                'message': 'Profile retrieved successfully',
                'data': serializer.data
            },
            status=status.HTTP_200_OK
        )
    
    @action(detail=False, methods=['put', 'patch'])
    def update_profile(self, request):
        """Update user profile."""
        try:
            serializer = UserProfileSerializer(
                request.user, 
                data=request.data, 
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            
            return Response(
                {
                    'success': True,
                    'message': 'Profile updated successfully',
                    'data': serializer.data
                },
                status=status.HTTP_200_OK
            )
        except serializers.ValidationError as e:
            return Response(
                {
                    'success': False,
                    'message': 'Validation error',
                    'errors': e.detail
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {
                    'success': False,
                    'message': 'Profile update failed',
                    'errors': str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['post'])
    def refresh_token(self, request):
        """Refresh access token using refresh token."""
        try:
            refresh_token = request.data.get('refresh')
            if not refresh_token:
                return Response(
                    {
                        'success': False,
                        'message': 'Refresh token is required'
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            token = RefreshToken(refresh_token)
            return Response(
                {
                    'success': True,
                    'message': 'Token refreshed successfully',
                    'data': {
                        'access': str(token.access_token)
                    }
                },
                status=status.HTTP_200_OK
            )
        except TokenError:
            return Response(
                {
                    'success': False,
                    'message': 'Invalid or expired refresh token'
                },
                status=status.HTTP_401_UNAUTHORIZED
            )
        except Exception as e:
            return Response(
                {
                    'success': False,
                    'message': 'Token refresh failed',
                    'errors': str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
