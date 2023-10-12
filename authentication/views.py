from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login, logout
from .models import *
from .serializers import *


class UserRegistrationAPIView(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = CustomUserSerializer


class UserAuthenticationAPIView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            serializer = CustomUserSerializer(user)
            return Response({'status': 'success', 'result': serializer.data})
        else:
            return Response({'status': 'fail', 'error': 'Invalid credentials', 'result': None})


class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({"status": "success", "message": "User logged out successfully."})


class UserDetail(generics.GenericAPIView):
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()

    def get_user(self, user_id):
        try:
            return CustomUser.objects.get(id=user_id)
        except:
            return None

    def get(self, request, user_id):
        """
        Получение записи CustomUser
        """
        user = self.get_user(user_id)
        if user is None:
            return Response({"status": "fail", "error": f"User with id: {user_id} not found"},
                            status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(user)
        return Response({"status": "success", "data": {"user": serializer.data}})
