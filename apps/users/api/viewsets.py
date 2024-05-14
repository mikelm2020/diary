from django.shortcuts import get_object_or_404
from django_filters import rest_framework
from drf_spectacular.utils import extend_schema
from rest_framework import filters, status, viewsets
from rest_framework.response import Response

from apps.users.api.serializers import (
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
        if self.queryset is None:
            self.queryset = self.serializer_class.Meta.model.objects.filter(
                is_active=True
            ).values("id", "username", "email")
            return self.queryset

    def get_object(self, pk):
        return get_object_or_404(self.serializer_class.Meta.model, pk=pk)

    @extend_schema(
        description="Obtiene una colección de usuarios",
        summary="Users",
        request=UserListSerializer,
        responses=UserListSerializer,
    )
    def list(self, request, *args, **kwargs):
        """
        Get a collection of users
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
        Get an user
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
        Update an user
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
        Delete an user in logical mode
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
