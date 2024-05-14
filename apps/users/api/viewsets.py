from django.shortcuts import get_object_or_404
from django_filters import rest_framework
from drf_spectacular.utils import extend_schema
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.users.api.serializers import (
    PasswordSerializer,
    UserListSerializer,
    UserSerializer,
    UserUpdateSerializer,
)
from utils.filters import UserFilterSet
from utils.pagination import ExtendedPagination

from .permissions import CreateUserPermission


class UserViewSet(viewsets.GenericViewSet):
    serializer_class = UserSerializer

    list_serializer_class = UserListSerializer
    filter_backends = [
        rest_framework.DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_class = UserFilterSet
    search_fields = ("email", "username")
    ordering_fields = ("email", "username")
    pagination_class = ExtendedPagination
    permission_classes = [CreateUserPermission]

    def get_queryset(self):
        """
        Get the queryset for the UserViewSet.

        If the queryset is not already defined, it filters the model objects based on the 'is_active' field
        and returns a queryset containing only the 'id', 'username', and 'email' fields.

        Returns:
        queryset: A filtered queryset containing 'id', 'username', and 'email' fields of active users.
        """
        if self.queryset is None:
            self.queryset = self.serializer_class.Meta.model.objects.filter(
                is_active=True
            ).values("id", "username", "email")
            return self.queryset

    def get_object(self, pk):
        """
        Get an object by its primary key.

        Args:
        pk (int): The primary key of the object to retrieve.

        Returns:
        object: The object corresponding to the given primary key.

        Raises:
        Http404: If no object is found with the given primary key, Http404 exception is raised.
        """
        return get_object_or_404(self.serializer_class.Meta.model, pk=pk)

    @extend_schema(request=PasswordSerializer, responses={200: None})
    @action(methods=["post"], detail=True)
    def set_password(self, request, pk=None):
        """
        Change the password of a user.

        Args:
        self: The UserViewSet instance.
        request: The request object containing the new password data.
        pk (int): The primary key of the user for which the password is to be changed.

        Returns:
        Response: A response indicating the status of the password change operation.

        Raises:
            N/A
        """
        user = self.get_object(pk)
        password_serializer = PasswordSerializer(data=request.data)
        if password_serializer.is_valid():
            user.set_password(password_serializer.validated_data["password"])
            user.save()
            return Response(
                {"message": "La contraseña se actualizó correctamente!"},
                status=status.HTTP_200_OK,
            )
        return Response(
            {"message": "Ocurrieron errores!", "error": password_serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )

    @extend_schema(request=UserSerializer, responses={201: None})
    def create(self, request):
        """
        Create a new user.

        Args:
        self: The UserViewSet instance.
        request: The request object containing the user data.

        Returns:
        Response: A response indicating the status of the user creation operation.

        Raises:
        N/A
        """
        user_serializer = self.serializer_class(data=request.data)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response(
                {"message": "El usuario se creo correctamente!"},
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {
                "message": "Hay errores en el registro!",
                "errors": user_serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    @extend_schema(
        description="Obtiene una colección de usuarios",
        summary="Users",
        request=UserListSerializer,
        responses=UserListSerializer,
    )
    def list(self, request, *args, **kwargs):
        """
        Get a collection of users

        Args:
        self: The UserViewSet instance.
        request: The request object.

        Returns:
        Response: A response containing a collection of users.

        Raises:
        N/A
        """
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.list_serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.list_serializer_class(queryset, many=True)
        return Response(serializer.data)

    @extend_schema(description="Obtiene el detalle de un usuario", summary="Users")
    def retrieve(self, request, pk=None):
        """
        Get details of a user.

        Args:
        self: The UserViewSet instance.
        request: The request object.
        pk (int): The primary key of the user to retrieve.

        Returns:
        Response: A response containing the details of the user.

        Raises:
        N/A
        """
        user = self.get_object(pk)
        user_serializer = self.serializer_class(user)

        # if meta := request.META.get("HTTP_REFERER"):
        #     print("La petición proviene de:", meta)
        # else:
        #     print("No se encontró el origen de la petición")

        return Response(user_serializer.data)

    @extend_schema(description="Actualiza un usuario", summary="Users")
    def update(self, request, pk=None):
        """
        Update an user.

        Args:
        self: The UserViewSet instance.
        request: The request object containing the updated user data.
        pk (int): The primary key of the user to be updated.

        Returns:
        Response: A response indicating the status of the user update operation.

        Raises:
        N/A
        """
        user = self.get_object(pk)
        user_serializer = UserUpdateSerializer(user, data=request.data)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response(
                {"message": "Usuario actualizado correctamente!"},
                status=status.HTTP_200_OK,
            )
        return Response(
            {
                "message": "Hay errores en la actualización!",
                "error": user_serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    @extend_schema(description="Elimina un usuario en modo lógico", summary="Users")
    def destroy(self, request, pk=None):
        """
        Delete a user in logical mode.

        Args:
        self: The UserViewSet instance.
        request: The request object.
        pk (int): The primary key of the user to be deleted.

        Returns:
        Response: A response indicating the status of the user deletion operation.

        Raises:
        N/A
        """
        user_destroy = self.serializer_class.Meta.model.objects.filter(id=pk).update(
            is_active=False
        )
        if user_destroy == 1:
            return Response(
                {"message": "Usuario eliminado correctamente!"},
                status=status.HTTP_200_OK,
            )
        return Response(
            {"message": "El usuario no existe!"}, status=status.HTTP_404_NOT_FOUND
        )
