from django.contrib.auth.models import AbstractUser, BaseUserManager, Group, Permission
from django.db import models
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from django.utils.translation import gettext_lazy as _

from django.contrib.auth.tokens import PasswordResetTokenGenerator
class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("username", email)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)

class User(AbstractUser):
    """
    Default custom user model for Sparkon Project.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """
    groups = models.ManyToManyField(
        Group,
        verbose_name=_("groups"),
        blank=True,
        related_name="custom_user_set"  # Change 'custom_user_set' to your preferred name
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_("user permissions"),
        blank=True,
        related_name="custom_user_set_permissions"  # Change 'custom_user_set_permissions' to your preferred name
    )
    email = models.EmailField(_("email address"), unique=True)
    group_name = models.CharField(max_length=70)

    username = models.CharField(max_length=30, null=True, blank=True)
    last_password_change = models.DateTimeField(null=True, blank=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = UserManager()

    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"pk": self.id})

    def get_token(self):
        """
        Generate token for user
        """
        return PasswordResetTokenGenerator().make_token(self)

    def get_uidb64(self):
        """
        Generate uidb64 against user's email address
        """

        return urlsafe_base64_encode(self.email.encode())

    def verify_token(self, token):
        return PasswordResetTokenGenerator().check_token(user=self, token=token)

    def __str__(self):
        return self.email