from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from .models import Profile
from .serializers import UserProfileSerializer
from rest_framework.generics import UpdateAPIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from .models import ListePatient
from django.contrib.auth.hashers import make_password
from .authenticate import EmailAuthBackend


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]   

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")  
            token = RefreshToken(refresh_token)
            token.blacklist()  

            return Response({"message": "Successfully logged out"}, status=status.HTTP_205_RESET_CONTENT)

        except Exception as e:
            return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)










class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        # Authenticate using email instead of username
        auth_backend = EmailAuthBackend()
        user = auth_backend.authenticate(request, email=email, password=password)

        if user is None:
            return Response({"error": "Invalid email or password"}, status=status.HTTP_401_UNAUTHORIZED)

        # Check if user is a Patient
        if not ListePatient.objects.filter(email=email).exists():
            return Response({"error": "You are not authorized as a patient"}, status=status.HTTP_403_FORBIDDEN)

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh)
        }, status=status.HTTP_200_OK)



















User = get_user_model()
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class SignUpView(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        first_name = request.data.get("first_name")
        last_name = request.data.get("last_name")
        role = request.data.get("role")  

     
        if role not in ["etudiant", "enseignant", "ATS"]:
            return Response({"error": "Invalid role selection"}, status=status.HTTP_400_BAD_REQUEST)

        
        if not email or not password or not first_name or not last_name:
            return Response({"error": "All fields are required"}, status=status.HTTP_400_BAD_REQUEST)

       
        if not ListePatient.objects.filter(email=email).exists():  
            return Response({"error": "You are not in ListePatient, registration failed."}, status=status.HTTP_403_FORBIDDEN)

   
        if User.objects.filter(email=email).exists():
            return Response({"error": "User already exists"}, status=status.HTTP_400_BAD_REQUEST)

    
        user = User.objects.create_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            role=role  
        )

        refresh = RefreshToken.for_user(user)

        return Response({
            "message": "Registration successful",
            "role": user.role,  
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)
    
































class UpdateUserProfileView(UpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.profile


