from django_filters import rest_framework
from drf_spectacular.utils import extend_schema
from rest_framework import filters, status, viewsets
from rest_framework.response import Response

from apps.contacts.api.serializers import (
    ContactListSerializer,
    ContactSerializer,
    ContactsRegisterSerializer,
    ContactUpdateSerializer,
)
from apps.contacts.models import Contacts
from apps.users.api.permissions import CreateUserPermission
from utils.filters import ContactFilterSet
from utils.pagination import ExtendedPagination


class ContactViewSet(viewsets.ModelViewSet):
    serializer_class = ContactSerializer
    register_serializer_class = ContactsRegisterSerializer
    list_serializer_class = ContactListSerializer
    filter_backends = [
        rest_framework.DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_class = ContactFilterSet
    search_fields = ("name", "last_name", "phones", "user")
    ordering_fields = ("name", "last_name", "phones", "user")
    pagination_class = ExtendedPagination
    permission_classes = [CreateUserPermission]
    queryset = Contacts.objects.filter(is_active=True)
    # def get_queryset(self):
    #     """
    #     Get the queryset for the ContactViewSet.

    #     If the queryset is not already defined, it filters the model objects based on the 'is_active' field
    #     and returns a queryset containing only the 'id', 'name', 'last_name', 'phones' and 'user' fields.

    #     Returns:
    #     queryset: A filtered queryset containing 'id', 'name', 'last_name', 'phones' and 'user' fields of active users.
    #     """
    #     if self.queryset is None:
    #         self.queryset = self.serializer_class.Meta.model.objects.filter(
    #             is_active=True
    #         ).values("id", "name", "last_name", "phones", "user")
    #         return self.queryset

    # def get_object(self, id):
    #     """
    #     Get an object by its primary key.

    #     Args:
    #     id (int): The primary key of the object to retrieve.

    #     Returns:
    #     object: The object corresponding to the given primary key.

    #     Raises:
    #     Http404: If no object is found with the given primary key, Http404 exception is raised.
    #     """
    #     return get_object_or_404(self.serializer_class.Meta.model, id=id)

    @extend_schema(request=register_serializer_class, responses={201: None})
    def create(self, request, *args, **kwargs):
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

        serializer = self.register_serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        contact = serializer.save(user=request.user)

        # Asocia los teléfonos al contacto creado
        phones_data = request.data.get("phones", [])
        for phone_data in phones_data:
            phone_number = phone_data["phone"]["number"]
            phone_type = phone_data["phone_type"]
            contact.phones.create(phone=phone_number, phone_type=phone_type)

        headers = self.get_success_headers(serializer.data)
        return Response(
            {"message": "El contacto se creó correctamente."},
            status=status.HTTP_201_CREATED,
            headers=headers,
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

        # Serializamos los datos y luego ajustamos el formato de los números de teléfono
        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data
        for item in data:
            phones_data = item.pop("phones", [])
            item["phone"] = [phone["phone"] for phone in phones_data]

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.list_serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.list_serializer_class(queryset, many=True)
        return Response(serializer.data)

    @extend_schema(description="Obtiene el detalle de un contacto", summary="Contacts")
    def retrieve(self, request, id=None):
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
        resource = self.get_object(id)
        resource_serializer = self.serializer_class(resource)

        # if meta := request.META.get("HTTP_REFERER"):
        #     print("La petición proviene de:", meta)
        # else:
        #     print("No se encontró el origen de la petición")

        return Response(resource_serializer.data)

    @extend_schema(description="Actualiza un contacto", summary="Users")
    def update(self, request, id=None):
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
        resource = self.get_object(id)
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
    def destroy(self, request, id=None):
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
            id=id
        ).update(is_active=False)
        if resource_destroy == 1:
            return Response(
                {"message": "Usuario eliminado correctamente!"},
                status=status.HTTP_200_OK,
            )
        return Response(
            {"message": "El contacto no existe!"}, status=status.HTTP_404_NOT_FOUND
        )
