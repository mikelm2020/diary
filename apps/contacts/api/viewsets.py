from django.shortcuts import get_object_or_404
from django_filters import rest_framework
from drf_spectacular.utils import extend_schema
from rest_framework import filters, status, viewsets
from rest_framework.response import Response

from apps.contacts.api.serializers import (
    ContactListSerializer,
    ContactSerializer,
    ContactUpdateSerializer,
)
from apps.users.api.permissions import CreateUserPermission
from utils.filters import UserFilterSet
from utils.pagination import ExtendedPagination


class ContactViewSet(viewsets.GenericViewSet):
    serializer_class = ContactSerializer

    list_serializer_class = ContactListSerializer
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
        Get the queryset for the ContactViewSet.

        If the queryset is not already defined, it filters the model objects based on the 'is_active' field
        and returns a queryset containing only the 'id', 'username', and 'email' fields.

        Returns:
        queryset: A filtered queryset containing 'id', 'username', and 'email' fields of active users.
        """
        if self.queryset is None:
            self.queryset = self.serializer_class.Meta.model.objects.filter(
                is_active=True
            ).values("id", "username")
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

    @extend_schema(request=ContactSerializer, responses={201: None})
    def create(self, request):
        """
        Create a new contact.

        Args:
        self: The ContactViewSet instance.
        request: The request object containing the contact data.

        Returns:
        Response: A response indicating the status of the contact creation operation.

        Raises:
        N/A
        """
        resource_serializer = self.serializer_class(data=request.data)
        if resource_serializer.is_valid():
            resource_serializer.save()
            return Response(
                {"message": "El contacto se creo correctamente!"},
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {
                "message": "Hay errores en el registro!",
                "errors": resource_serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    @extend_schema(
        description="Obtiene una colección de contactos",
        summary="Contacts",
        request=ContactListSerializer,
        responses=ContactListSerializer,
    )
    def list(self, request, *args, **kwargs):
        """
        Get a collection of contacts

        Args:
        self: The ContactViewSet instance.
        request: The request object.

        Returns:
        Response: A response containing a collection of contacts.

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

    @extend_schema(description="Obtiene el detalle de un contacto", summary="Contacts")
    def retrieve(self, request, pk=None):
        """
        Get details of a contact.

        Args:
        self: The ContactViewSet instance.
        request: The request object.
        pk (int): The primary key of the contact to retrieve.

        Returns:
        Response: A response containing the details of the contact.

        Raises:
        N/A
        """
        resource = self.get_object(pk)
        resource_serializer = self.serializer_class(resource)

        # if meta := request.META.get("HTTP_REFERER"):
        #     print("La petición proviene de:", meta)
        # else:
        #     print("No se encontró el origen de la petición")

        return Response(resource_serializer.data)

    @extend_schema(description="Actualiza un contacto", summary="Users")
    def update(self, request, pk=None):
        """
        Update an contact.

        Args:
        self: The ContactViewSet instance.
        request: The request object containing the updated contact data.
        pk (int): The primary key of the contact to be updated.

        Returns:
        Response: A response indicating the status of the contact update operation.

        Raises:
        N/A
        """
        resource = self.get_object(pk)
        resource_serializer = ContactUpdateSerializer(resource, data=request.data)
        if resource_serializer.is_valid():
            resource_serializer.save()
            return Response(
                {"message": "Usuario actualizado correctamente!"},
                status=status.HTTP_200_OK,
            )
        return Response(
            {
                "message": "Hay errores en la actualización!",
                "error": resource_serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    @extend_schema(description="Elimina un contacto en modo lógico", summary="Contacts")
    def destroy(self, request, pk=None):
        """
        Delete a contact in logical mode.

        Args:
        self: The ContactViewSet instance.
        request: The request object.
        pk (int): The primary key of the contact to be deleted.

        Returns:
        Response: A response indicating the status of the contact deletion operation.

        Raises:
        N/A
        """
        resource_destroy = self.serializer_class.Meta.model.objects.filter(
            id=pk
        ).update(is_active=False)
        if resource_destroy == 1:
            return Response(
                {"message": "Usuario eliminado correctamente!"},
                status=status.HTTP_200_OK,
            )
        return Response(
            {"message": "El contacto no existe!"}, status=status.HTTP_404_NOT_FOUND
        )
