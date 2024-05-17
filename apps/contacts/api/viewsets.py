from django.shortcuts import get_object_or_404
from django_filters import rest_framework
from drf_spectacular.utils import OpenApiExample, extend_schema
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

    @extend_schema(
        request=ContactsRegisterSerializer,
        responses={201: None},
        examples=[
            OpenApiExample(
                "Example Value Schemma",
                description="Request Body",
                value={
                    "name": "Geronimo",
                    "last_name": "Valtierra",
                    "company": "Industrias Futura SA de CV",
                    "phones": [
                        {"phone": "+5215578906715", "phone_type": "MO"},
                        {"phone": "+5215566907612", "phone_type": "WO"},
                    ],
                    "emails": [
                        {"email": "geronimo.val@futura.com", "email_type": "MA"}
                    ],
                    "address": [{"address": "Calle 123", "address_type": "MA"}],
                    "website": "url",
                    "important_dates": [
                        {
                            "important_date": "2021-01-01",
                            "important_date_type": "MA",
                        }
                    ],
                    "related_persons": [
                        {"name": "Alicia", "related_person_type": "AS"}
                    ],
                    "sip": "sip",
                    "notes": "",
                    "tags": [{"tag": "CU"}],
                },
            ),
        ],
    )
    def perform_create(self, serializer):
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
        serializer = ContactsRegisterSerializer(data=self.request.data)
        if serializer.is_valid():
            serializer.save(user=self.request.user)

        else:
            return Response(
                {"message": "Ocurrieron errores!", "error": serializer.errors},
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
        queryset = Contacts.objects.filter(user=request.user, is_active=True)
        serializer = self.list_serializer_class(queryset, many=True)
        data = serializer.data

        for item in data:
            phones_data = item.pop("phones", [])
            item["phone"] = [phone["phone"] for phone in phones_data]
            emails_data = item.pop("emails", [])
            item["email"] = [email["email"] for email in emails_data]
            addresses_data = item.pop("address", [])
            item["address"] = [address["address"] for address in addresses_data]
            important_dates_data = item.pop("important_dates", [])
            item["important_date"] = [
                important_date["important_date"]
                for important_date in important_dates_data
            ]
            related_persons_data = item.pop("related_persons", [])
            item["related_person"] = [
                related_person["related_person"]
                for related_person in related_persons_data
            ]
            tags_data = item.pop("tags", [])
            item["tag"] = [tag["tag"] for tag in tags_data]

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.list_serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.list_serializer_class(queryset, many=True)
        return Response(serializer.data)

    @extend_schema(
        description="Obtiene el detalle de un contacto",
        summary="Contacts",
        responses=ContactListSerializer,
    )
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
        queryset = Contacts.objects.filter(user=request.user, is_active=True)
        contact = get_object_or_404(queryset, pk=pk)
        resource_serializer = self.get_serializer(contact)

        return Response(resource_serializer.data)

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
        queryset = Contacts.objects.filter(user=request.user, is_active=True)
        contact = get_object_or_404(queryset, pk=pk)
        # Desactivar el contacto (marcarlo como inactivo)
        contact.is_active = False
        contact.save()

        return Response(
            {"message": "Contacto eliminado correctamente!"}, status=status.HTTP_200_OK
        )

    @extend_schema(
        description="Actualiza un contacto",
        summary="Contacts",
        request=ContactUpdateSerializer,
        responses=ContactUpdateSerializer,
    )
    def partial_update(self, request, pk=None):
        """
        Partially update a contact.

        Args:
        self: The ContactUpdateViewSet instance.
        request: The request object containing the partially updated contact data.
        pk (int): The primary key of the contact to be partially updated.

        Returns:
        Response: A response indicating the status of the partial update operation.

        Raises:
        N/A
        """
        queryset = Contacts.objects.filter(user=request.user, is_active=True)
        contact = get_object_or_404(queryset, pk=pk)
        serializer = self.get_serializer(contact, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        # Associates the phones to created contact
        phones_data = request.data.get("phones", [])
        for phone_data in phones_data:
            phone_number = phone_data["phone"]["number"]
            phone_type = phone_data["phone_type"]
            contact.phones.create(phone=phone_number, phone_type=phone_type)

        # Associates the emails to created contact
        emails_data = request.data.get("emails", [])
        for email_data in emails_data:
            email = email_data["email"]
            email_type = email_data["email_type"]
            contact.emails.create(email=email, email_type=email_type)

        # Associates the address to created contact
        addresses_data = request.data.get("address", [])
        for address_data in addresses_data:
            address = address_data["address"]
            address_type = address_data["address_type"]
            contact.address.create(address=address, address_type=address_type)

        # Associates the important_dates to created contact
        important_dates_data = request.data.get("important_dates", [])
        for important_date_data in important_dates_data:
            important_date = important_date_data["important_date"]
            important_date_type = important_date_data["important_date_type"]
            contact.important_dates.create(
                important_date=important_date, important_date_type=important_date_type
            )

        # Associates the related_persons to created contact
        related_persons_data = request.data.get("related_persons", [])
        for related_person_data in related_persons_data:
            name = related_person_data["name"]
            related_person_type = related_person_data["related_person_type"]
            contact.related_persons.create(
                name=name, related_person_type=related_person_type
            )

        serializer.save()
        # Associates the tags to created contact
        tags_data = request.data.get("tags", [])
        for tag_data in tags_data:
            tag = phone_data["tag"]
            contact.tags.create(tag=tag)

        headers = self.get_success_headers(serializer.data)

        return Response(
            {"message": "El contacto se actualizó correctamente."},
            status=status.HTTP_200_OK,
            headers=headers,
        )
