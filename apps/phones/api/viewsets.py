from django.shortcuts import get_object_or_404
from django_filters import rest_framework
from drf_spectacular.utils import extend_schema
from rest_framework import filters, status, viewsets
from rest_framework.response import Response

from apps.phones.api.serializers import (
    PhoneListSerializer,
    PhoneRegisterSerializer,
    PhonesSerializer,
    PhoneUpdateSerializer,
)
from apps.users.api.permissions import CreateUserPermission
from utils.filters import PhoneFilterSet
from utils.pagination import ExtendedPagination


class PhoneViewSet(viewsets.GenericViewSet):
    serializer_class = PhonesSerializer
    register_serializer_class = PhoneRegisterSerializer
    list_serializer_class = PhoneListSerializer
    filter_backends = [
        rest_framework.DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_class = PhoneFilterSet
    search_fields = ("phone", "phone_type")
    ordering_fields = ("phone", "phone_type")
    pagination_class = ExtendedPagination
    permission_classes = [CreateUserPermission]

    def get_queryset(self):
        """
        Get the queryset for the ContactViewSet.

        If the queryset is not already defined, it filters the model objects based on the 'is_active' field
        and returns a queryset containing only the 'id', 'phone', and 'phone_typr' fields.

        Returns:
        queryset: A filtered queryset containing 'id', 'phone', and 'phone_type' fields of active phones.
        """
        if self.queryset is None:
            self.queryset = self.serializer_class.Meta.model.objects.filter(
                is_active=True
            ).values("id", "phone", "phone_type")
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

    @extend_schema(request=register_serializer_class, responses={201: None})
    def create(self, request):
        """
        Create a new phone.

        Args:
        self: The PhoneViewSet instance.
        request: The request object containing the phone data.

        Returns:
        Response: A response indicating the status of the phone creation operation.

        Raises:
        N/A
        """
        resource_serializer = self.register_serializer_class(data=request.data)
        if resource_serializer.is_valid():
            resource_serializer.save()
            return Response(
                {"message": "El telefono se creo correctamente!"},
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
        description="Obtiene una colección de telefonos",
        summary="Phones",
        request=PhoneListSerializer,
        responses=PhoneListSerializer,
    )
    def list(self, request, *args, **kwargs):
        """
        Get a collection of phones

        Args:
        self: The PhoneViewSet instance.
        request: The request object.

        Returns:
        Response: A response containing a collection of phones.

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

    @extend_schema(description="Obtiene el detalle de un telefono", summary="Phones")
    def retrieve(self, request, pk=None):
        """
        Get details of a phone.

        Args:
        self: The PhoneViewSet instance.
        request: The request object.
        pk (int): The primary key of the phone to retrieve.

        Returns:
        Response: A response containing the details of the phone.

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

    @extend_schema(description="Actualiza un telefono", summary="Phones")
    def update(self, request, pk=None):
        """
        Update an phone.

        Args:
        self: The PhonetViewSet instance.
        request: The request object containing the updated phone data.
        pk (int): The primary key of the phone to be updated.

        Returns:
        Response: A response indicating the status of the phone update operation.

        Raises:
        N/A
        """
        resource = self.get_object(pk)
        resource_serializer = PhoneUpdateSerializer(resource, data=request.data)
        if resource_serializer.is_valid():
            resource_serializer.save()
            return Response(
                {"message": "Telefono actualizado correctamente!"},
                status=status.HTTP_200_OK,
            )
        return Response(
            {
                "message": "Hay errores en la actualización!",
                "error": resource_serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    @extend_schema(description="Elimina un telefono en modo lógico", summary="Phones")
    def destroy(self, request, pk=None):
        """
        Delete a phone in logical mode.

        Args:
        self: The ContactViewSet instance.
        request: The request object.
        pk (int): The primary key of the phone to be deleted.

        Returns:
        Response: A response indicating the status of the phone deletion operation.

        Raises:
        N/A
        """
        resource_destroy = self.serializer_class.Meta.model.objects.filter(
            id=pk
        ).update(is_active=False)
        if resource_destroy == 1:
            return Response(
                {"message": "Telefono eliminado correctamente!"},
                status=status.HTTP_200_OK,
            )
        return Response(
            {"message": "El telefono no existe!"}, status=status.HTTP_404_NOT_FOUND
        )
