from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, full_name, phone_number, password):
        """
        Creates and saves a User with the given email, fullname of phone number and password.
        """

        if not email:
            raise ValueError('The user must have a email')

        if not full_name:
            raise ValueError('The user must have a full name')

        if not phone_number:
            raise ValueError('The user must have an phone number')

        user = self.model(
            email=self.normalize_email(email),
            full_name=full_name,
            phone_number=phone_number
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, full_name, phone_number, password):
        """
        Creates and saves a Super User with the given email, fullname of phone number and password.
        """

        user = self.create_user(email, full_name, phone_number, password)
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
