from django.core.exceptions import ValidationError, FieldDoesNotExist
from django.utils.translation import ngettext, gettext as _, gettext_lazy as _
from django.utils.deconstruct import deconstructible
import re


class NewPasswordNotSameAsOldValidator:
    def validate(self, password, user=None):
        if user and user.check_password(password):
            raise ValidationError(
                _("The new password cannot be the same as your current password."),
                code="password_no_change",
            )

    def get_help_text(self):
        return _("Your new password must be different from your current password.")


class MaximumLengthValidator:

    def __init__(self, max_length=128):
        self.max_length = max_length

    def validate(self, password, user=None):
        if len(password) > self.max_length:
            raise ValidationError(
                _(
                    "This password is greater than the maximum of %(max_length)d characters."
                ),
                code="password_too_long",
                params={"max_length": self.max_length},
            )

    def get_help_text(self):
        return _(
            "Your password can be a maximum of %(max_length)d characters."
            % {"max_length": self.max_length}
        )



# class BreachPasswordValidator:
#     """
#     Checks if the given password has been breached using the Have I Been Pwned API.
#     """

#     def validate(self, password, user=None):
#         sha1_password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
#         prefix = sha1_password[:5]
#         url = f'https://api.pwnedpasswords.com/range/{prefix}'
#         response = requests.get(url)

#         if response.status_code != 200:
#             raise ValidationError("Error checking password security. Please try again.")

#         suffix = sha1_password[5:]
#         if any(line.split(':')[0] == suffix for line in response.text.splitlines()):
#             raise ValidationError("This password has been compromised in a data breach. Please choose a different one.")

#     def get_help_text(self):
#         return "Your password must not have been compromised in a data breach."


class UnicodePasswordValidator:
    def validate(self, password, user=None):
        if not re.match(
            r"^[\s\w\W]+$", password
        ):  # Allows all Unicode and whitespace characters
            raise ValidationError(
                "Your password must allow any Unicode character, including emojis."
            )

    def get_help_text(self):
        return "Your password can contain any character, including Unicode and emojis."


class MinimumLengthValidator:
    """
    Validate that the password is of a minimum length.
    """

    def __init__(self, min_length=12):
        self.min_length = min_length

    def validate(self, password, user=None):
        if len(password) < self.min_length:
            raise ValidationError(
                ngettext(
                    "This password is too short. It must contain at least "
                    "%(min_length)d characters.",
                    "This password is too short. It must contain at least "
                    "%(min_length)d characters.",
                    self.min_length,
                ),
                code="password_too_short",
                params={"min_length": self.min_length},
            )

    def get_help_text(self):
        return ngettext(
            "Your password must contain at least %(min_length)d characters.",
            "Your password must contain at least %(min_length)d characters.",
            self.min_length,
        ) % {"min_length": self.min_length}
