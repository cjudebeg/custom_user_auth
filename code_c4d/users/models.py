import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager


class CustomUser(AbstractUser):
    """
    Custom user model that uses email as the primary identifier
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = None  # Remove username field
    email = models.EmailField(_("email address"), unique=True)

    # We'll keep first_name and last_name from AbstractUser
    # But we'll add some basic validation
    first_name = models.CharField(_("first name"), max_length=150, blank=True)
    last_name = models.CharField(_("last name"), max_length=150, blank=True)

    # Add a display name field
    display_name = models.CharField(max_length=100, blank=True)

    # Email verification status
    email_verified = models.BooleanField(default=False)

    # When the user was created and last updated
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def save(self, *args, **kwargs):
        # Set display_name if not set
        if not self.display_name and (self.first_name or self.last_name):
            self.display_name = f"{self.first_name} {self.last_name}".strip()
        elif not self.display_name:
            self.display_name = self.email.split("@")[0]

        super().save(*args, **kwargs)

    def __str__(self):
        if self.display_name:
            return self.display_name
        return self.email

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
        indexes = [
            models.Index(fields=["email"]),
        ]


STATE_CHOICES = [
    ("VIC", "VIC"),
    ("NSW", "NSW"),
    ("ACT", "ACT"),
    ("QLD", "QLD"),
    ("NT", "NT"),
    ("WA", "WA"),
    ("SA", "SA"),
]

CLEARANCE_LEVEL_CHOICES = [
    ("None", "None"),
    ("Pending", "Pending"),
    ("Baseline", "Baseline"),
    ("NV1", "NV1"),
    ("NV2", "NV2"),
    ("PV", "PV"),
]


class Profile(models.Model):
    """
    Extended profile information for users
    Note: Basic identity info (first_name, last_name) is now in CustomUser
    """

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile"
    )

    # Changed second_name to middle_name for clarity and consistency
    middle_name = models.CharField(max_length=30, blank=True)

    # Remove duplicate and keep one date_of_birth field
    date_of_birth = models.DateField(
        blank=True, null=True
    )  # null is OK for date fields

    # Location
    state = models.CharField(max_length=3, choices=STATE_CHOICES, blank=True)
    suburb = models.CharField(max_length=100, blank=True)

    # Security clearance
    clearance_level = models.CharField(
        max_length=20, choices=CLEARANCE_LEVEL_CHOICES, default="None"
    )
    clearance_no = models.CharField(max_length=50, blank=True)
    clearance_expiry = models.DateField(blank=True, null=True)

    # Skills
    skill_sets = models.TextField(blank=True)
    skill_level = models.CharField(max_length=100, blank=True)

    # Onboarding status
    onboarding_completed = models.BooleanField(default=False)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Profile of {self.user}"

    class Meta:
        verbose_name = _("profile")
        verbose_name_plural = _("profiles")
        indexes = [
            models.Index(fields=["clearance_level"]),
            models.Index(fields=["onboarding_completed"]),
        ]
