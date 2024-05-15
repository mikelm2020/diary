from django.contrib.auth.models import BaseUserManager
from django.db import models


class UserManager(BaseUserManager, models.Manager):
    """Manager for new user model

    Args:
        BaseUserManager (obj): class Base of the user Manager of Django
        models (obj): class of the model of Manager of the user of Django
    """

    def _create_user(
        self,
        username,
        email,
        password,
        is_staff,
        is_superuser,
        is_active,
        **extra_fields,
    ):
        """Private method for create an user based in new model user

        Args:
            username (str): knick name
            email (str): email
            password (str): password
            is_staff (bool): the user has permisssions for the admin panel?
            is_superuser (bool): the user is an admin?
            is_active (bool): logical delete
            **extra_fields (dict): other fields

        Returns:
            obj: returns an user instance
        """
        # Create an user instance
        user = self.model(
            username=username,
            email=email,
            is_staff=is_staff,
            is_superuser=is_superuser,
            is_active=is_active,
            **extra_fields,
        )

        user.set_password(password)  # Encrypt the password
        user.save(using=self.db)  # Save password encrypted
        return user

    def create_user(self, username, email, password=None, **extra_fields):
        """Method for create un normal user

        Args:
            username (_type_): _description_
            email (_type_): _description_
            password (_type_, optional): _description_. Defaults to None.
            **extra_fields (dict): other fields


        Returns:
            obj: The private method for create an user
        """
        return self._create_user(
            username, email, password, False, False, True, **extra_fields
        )

    def create_superuser(self, username, email, password=None, **extra_fields):
        """Method for create a super user

        Args:
            username (str): username
            email (str): email
            password (str, optional): password. Defaults to None.
            **extra_fields (dict): other fields


        Returns:
            obj: the private method for create an super user
        """
        return self._create_user(
            username, email, password, True, True, True, **extra_fields
        )
