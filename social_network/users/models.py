from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth import get_user_model


class CustomUserManager(BaseUserManager):
    """
    Custom manager for User model.

    This manager provides methods to create regular users and superusers
    with email and password as primary credentials.
    """
    def create_user(self, email, password=None, **extra_fields):
        """
        Create and return a regular user with an email and password.

        :param email: User's email address.
        :param password: User's password.
        :param extra_fields: Additional fields for the user.
        :return: The created user instance.
        """
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Create and return a superuser with an email and password.

        :param email: Superuser's email address.
        :param password: Superuser's password.
        :param extra_fields: Additional fields for the superuser.
        :return: The created superuser instance.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser):
    """
    Custom User model.

    This model extends AbstractBaseUser and uses email as the unique identifier
    for authentication instead of a username.
    """
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = CustomUserManager()

    def __str__(self):
        return self.email

User = get_user_model()


class FriendRequest(models.Model):
    """
    Model representing a friend request between users.

    This model stores information about friend requests sent from one user to another.
    """
    from_user = models.ForeignKey(User, related_name='sent_requests', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='received_requests', on_delete=models.CASCADE)
    is_accepted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('from_user', 'to_user')
        
    def __str__(self):
        return f"From {self.from_user.email} to {self.to_user.email}"
    
    