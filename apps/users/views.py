# from django.contrib.auth import authenticate
# from drf_spectacular.utils import extend_schema
# from rest_framework import status
# from rest_framework.generics import GenericAPIView
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.response import Response
# from rest_framework_simplejwt.views import TokenObtainPairView

# from apps.users.api.serializers import (
#     CustomTokenObtainPairSerializer,
#     CustomUserSerializer,
#     LogoutSerializer,
# )


# class Login(TokenObtainPairView):
#     serializer_class = CustomTokenObtainPairSerializer

#     def post(self, request, *args, **kwargs):
#         """
#         Handle the POST request for user login.

#         Args:
#         - request: The request object containing user input data.

#         Returns:
#         - Response: A JSON response containing the authentication token, user data, and a success message if the login is successful.
#                     If the login fails, it returns an error message with an appropriate status code.
#         """
#         username = request.data.get("username", "")
#         password = request.data.get("password", "")
#         user = authenticate(username=username, password=password)
#         if user:
#             login_serializer = self.serializer_class(data=request.data)
#             if login_serializer.is_valid():
#                 user_serializer = CustomUserSerializer(user)
#                 return Response(
#                     {
#                         "token": login_serializer.validated_data.get("access"),
#                         "refresh-token": login_serializer.validated_data.get("refresh"),
#                         "user": user_serializer.data,
#                         "message": "Inicio de Sesión Exitoso.",
#                     },
#                     status=status.HTTP_200_OK,
#                 )
#             return Response(
#                 {"error": "Contraseña o nombre de usuario incorrectos."},
#                 status=status.HTTP_400_BAD_REQUEST,
#             )
#         return Response(
#             {"error": "Contraseña o nombre de usuario incorrectos."},
#             status=status.HTTP_400_BAD_REQUEST,
#         )


# @extend_schema(responses={204: LogoutSerializer}, request=LogoutSerializer)
# class Logout(GenericAPIView):
#     serializer_class = LogoutSerializer
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         """
#         Handle the POST request for user logout.

#         Args:
#         - request: The request object containing user input data.

#         Returns:
#         - Response: A JSON response indicating the successful closure of the user session with a corresponding success message and status code 204 (No Content).
#         If the logout process encounters any errors, it returns an error message with an appropriate status code.
#         """
#         serializer = self.serializer_class(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(
#             {"message": "Sesión cerrada exitosamente"},
#             status=status.HTTP_204_NO_CONTENT,
#         )

from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from apps.users.api.serializers import LoginSerializer


@extend_schema(request=LoginSerializer)
class Login(APIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            token = TokenObtainPairView().post(request).data
            return Response(token, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Logout(APIView):
    def post(self, request, *args, **kwargs):
        return Response(status=status.HTTP_204_NO_CONTENT)
