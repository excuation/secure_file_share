from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.urls import reverse

from .models import CustomUser
from .serializers import UserSignupSerializer
from .utils import generate_email_token




class DynamicRoleSignupView(APIView):
    def post(self, request):
        serializer = UserSignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            # If the user is a client, generate verification link
            if user.is_client_user:
                token = generate_email_token(user)
                verify_url = request.build_absolute_uri(
                    reverse('verify-email') + f"?token={token}"
                )
                return Response({
                    "message": "Client registered. Please verify your email.",
                    "verification_url": verify_url
                }, status=status.HTTP_201_CREATED)

            # If the user is an ops user, no verification needed
            return Response({
                "message": "Ops user registered successfully."
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import CustomUser

class VerifyEmailView(APIView):
    def get(self, request):
        token = request.GET.get('token')
        if not token:
            return Response({"error": "Token is missing."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = URLSafeTimedSerializer(settings.SECRET_KEY)

        try:
            data = serializer.loads(token, max_age=3600)  # valid for 1 hour
            user_id = data.get("user_id")
            user = CustomUser.objects.get(id=user_id)
            user.is_active = True
            user.email_verified = True
            user.save()
            return Response({"message": "Email verified successfully."}, status=status.HTTP_200_OK)
        except SignatureExpired:
            return Response({"error": "Token expired."}, status=status.HTTP_400_BAD_REQUEST)
        except (BadSignature, CustomUser.DoesNotExist):
            return Response({"error": "Invalid token."}, status=status.HTTP_400_BAD_REQUEST)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser

class OpsLoginView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)

        if user is not None and user.is_ops_user:
            if not user.is_active:
                return Response({"error": "Account not activated"}, status=400)
            refresh = RefreshToken.for_user(user)
            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            })
        return Response({"error": "Invalid credentials or not an Ops user"}, status=401)
    


    from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

class ClientLoginView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)

        if user and user.is_client_user:
            if not user.email_verified:
                return Response({"error": "Email not verified."}, status=403)

            refresh = RefreshToken.for_user(user)
            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token)
            }, status=200)

        return Response({"error": "Invalid credentials or not a client user."}, status=401)

