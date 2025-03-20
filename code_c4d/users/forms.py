from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model
from .models import Profile, STATE_CHOICES, CLEARANCE_LEVEL_CHOICES

CustomUser = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    """
    Form for user registration. Extends Django's UserCreationForm to use
    our custom User model with email as the unique identifier.
    """

    email = forms.EmailField(
        max_length=254,
        required=True,
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "Email"}
        ),
    )

    class Meta:
        model = CustomUser
        fields = ("email",)  # Fixed tuple syntax

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make the password fields prettier
        self.fields["password1"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Password"}
        )
        self.fields["password2"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Confirm Password"}
        )


class CustomUserChangeForm(UserChangeForm):
    """
    Form for updating users. Extends Django's UserChangeForm to use
    our custom User model.
    """

    email = forms.EmailField(
        max_length=254,
        required=True,
        widget=forms.EmailInput(attrs={"class": "form-control"}),
    )
    first_name = forms.CharField(
        max_length=150,
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    last_name = forms.CharField(
        max_length=150,
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    display_name = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )

    class Meta:
        model = CustomUser
        fields = ("email", "first_name", "last_name", "display_name", "is_active")


class ProfileForm(forms.ModelForm):
    """
    Form for creating or updating user profile information.
    """

    # Remove first_name and last_name since they belong to User model
    middle_name = forms.CharField(
        max_length=30,
        required=False,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Middle Name"}
        ),
    )

    date_of_birth = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={"class": "form-control", "type": "date"}),
    )

    state = forms.ChoiceField(
        choices=[("", "Select State")]
        + list(STATE_CHOICES),  # Correct choices from model
        required=False,
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    suburb = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Suburb"}
        ),
    )

    clearance_level = forms.ChoiceField(
        choices=[("", "Select Clearance Level")]
        + list(CLEARANCE_LEVEL_CHOICES),  # Correct choices
        required=False,
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    clearance_no = forms.CharField(
        max_length=50,
        required=False,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Clearance Number"}
        ),
    )

    clearance_expiry = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={"class": "form-control", "type": "date"}),
    )

    skill_sets = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={"class": "form-control", "placeholder": "Skills", "rows": 3}
        ),
    )

    skill_level = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Skill Level"}
        ),
    )

    class Meta:
        model = Profile
        fields = (
            "middle_name",
            "date_of_birth",
            "state",
            "suburb",
            "clearance_level",
            "clearance_no",
            "clearance_expiry",
            "skill_sets",
            "skill_level",
            "onboarding_completed",
        )


class UserProfileForm(forms.Form):
    """
    Combined form for creating a user with profile information in one step.
    Useful for registration processes that collect profile information upfront.
    """

    # User fields
    email = forms.EmailField(
        max_length=254,
        required=True,
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "Email"}
        ),
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Password"}
        )
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Confirm Password"}
        )
    )

    # User personal info
    first_name = forms.CharField(
        max_length=150,
        required=False,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "First Name"}
        ),
    )
    last_name = forms.CharField(
        max_length=150,
        required=False,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Last Name"}
        ),
    )

    # Profile fields - optional but useful fields to collect during registration
    middle_name = forms.CharField(
        max_length=30,
        required=False,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Middle Name"}
        ),
    )
    state = forms.ChoiceField(
        choices=[("", "Select State")] + list(STATE_CHOICES),  # Fixed choices
        required=False,
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already in use")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match")
        return password2
