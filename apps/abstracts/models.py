import uuid

from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models.query import QuerySet
from django.http import Http404


class AbstractSoftDeleteManager(models.Manager):
    """
    Returns a QuerySet of objects that are currently active.

    This method overrides the default get_queryset method in the Manager class.
    It filters the QuerySet returned by the superclass's get_queryset method
    to only include objects where the 'is_active' field is set to True.

    Parameters:
    self (AbstractSoftDeleteManager): The instance of the manager class.

    Returns:
    QuerySet: A QuerySet containing only active objects.
    """

    def get_queryset(self) -> QuerySet:
        return super().get_queryset().filter(is_active=True)


class AbstractManager(models.Manager):
    """
    Retrieves an object by its ID.

    This method attempts to retrieve an object by its ID. If the object is found, it is returned.
    If the object does not exist or if the ID is invalid, an Http404 exception is raised.

    Parameters:
    self (AbstractManager): The instance of the manager class.
    id (str): The ID of the object to retrieve.

    Returns:
    object: The retrieved object if found.

    Raises:
    Http404: If the object does not exist or if the ID is invalid.
    """

    def get_object_by_id(self, id):
        try:
            instance = self.get(id=id)
            return instance
        except (ObjectDoesNotExist, ValueError, TypeError):
            return Http404


class AbstractModel(models.Model):
    id = models.UUIDField(
        primary_key=True,
        db_index=True,
        unique=True,
        default=uuid.uuid4,
        editable=False,
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    objects = AbstractManager()
    active_objects = AbstractSoftDeleteManager()

    def soft_delete(self):
        """
        Soft deletes the object by setting its 'is_active' field to False.

        This method updates the 'is_active' field of the object to False and saves the changes to the database,
        effectively marking the object as inactive without physically removing it from the database.

        Parameters:
        self (AbstractModel): The instance of the model to be soft deleted.

        Returns:
        None
        """
        self.is_active = False
        self.save()

    def restore(self):
        """
        Restores the soft-deleted object by setting its 'is_active' field to True and saving the changes.

        This method updates the 'is_active' field of the object to True and saves the changes to the database,
        effectively marking the object as active again after it has been soft-deleted.

        Parameters:
        self (AbstractModel): The instance of the model to be restored.

        Returns:
        None
        """
        self.is_active = True
        self.save()

    class Meta:
        abstract = True

    def __repr__(self):
        """
        Returns a string representation of the object.

        This method returns a string representation of the object, including its class name and ID.

        Parameters:
        self (AbstractModel): The instance of the model.

        Returns:
        str: A string representation of the object, including its class name and ID.
        """
        return f"<{self.__class__.__name__} {self.id}>"
