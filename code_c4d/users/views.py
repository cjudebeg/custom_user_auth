from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import CreateView, UpdateView, DetailView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from .models import Profile
from .forms import (
    CustomUserCreationForm,
    CustomUserChangeForm,
    ProfileForm,
    UserProfileForm,
)

User = get_user_model()


class SignUpView(CreateView):
    """
    View for basic user registration with email and password.
    """

    form_class = CustomUserCreationForm
    template_name = "registration/signup.html"
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Your account has been created! Please login.")
        return response


class CombinedSignUpView(CreateView):
    """
    View for user registration that collects profile info at the same time.
    """

    form_class = UserProfileForm
    template_name = "registration/signup_with_profile.html"
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        # Create the user first
        user = User.objects.create_user(
            email=form.cleaned_data["email"],
            password=form.cleaned_data["password1"],
            first_name=form.cleaned_data.get("first_name", ""),
            last_name=form.cleaned_data.get("last_name", ""),
        )

        # Profile should be created via signal, so we just need to update it
        profile = user.profile
        profile.second_name = form.cleaned_data.get("middle_name", "")
        profile.state = form.cleaned_data.get("state", "")
        profile.save()

        messages.success(self.request, "Your account has been created! Please login.")
        return redirect(self.success_url)


class UserUpdateView(LoginRequiredMixin, UpdateView):
    """
    View for users to update their account information.
    """

    model = User
    form_class = CustomUserChangeForm
    template_name = "profiles/user_update.html"
    success_url = reverse_lazy("profile_detail")

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, "Your account has been updated!")
        return super().form_valid(form)


class UserDeleteView(LoginRequiredMixin, DeleteView):
    """
    View for users to delete their account.
    """

    model = User
    template_name = "profiles/user_confirm_delete.html"
    success_url = reverse_lazy("signup")

    def get_object(self):
        return self.request.user

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Your account has been deleted!")
        return super().delete(request, *args, **kwargs)


class ProfileDetailView(LoginRequiredMixin, DetailView):
    """
    View for displaying the user's profile.
    """

    model = Profile
    template_name = "profiles/profile_detail.html"
    context_object_name = "profile"

    def get_object(self):
        return self.request.user.profile


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """
    View for updating profile information.
    """

    model = Profile
    form_class = ProfileForm
    template_name = "profiles/profile_update.html"
    success_url = reverse_lazy("profile_detail")

    def get_object(self):
        return self.request.user.profile

    def form_valid(self, form):
        messages.success(self.request, "Your profile has been updated!")
        return super().form_valid(form)


@login_required
def profile_create_view(request):
    """
    View for creating a profile if one doesn't exist.
    This should rarely be needed since profiles are created via signals.
    """
    # Check if user already has a profile
    try:
        profile = request.user.profile
        return redirect("profile_detail")
    except Profile.DoesNotExist:
        if request.method == "POST":
            form = ProfileForm(request.POST)
            if form.is_valid():
                profile = form.save(commit=False)
                profile.user = request.user
                profile.save()
                messages.success(request, "Your profile has been created!")
                return redirect("profile_detail")
        else:
            form = ProfileForm()

        return render(request, "profiles/profile_update.html", {"form": form})


@login_required
def dashboard_view(request):
    """
    User dashboard view.
    """
    return render(request, "profiles/dashboard.html", {"profile": request.user.profile})


@login_required
def onboarding_view(request):
    """
    Onboarding view for users to complete their profile.
    """
    profile = request.user.profile

    # If onboarding is already completed, redirect to dashboard
    if profile.onboarding_completed:
        messages.info(request, "You've already completed onboarding.")
        return redirect("dashboard")

    if request.method == "POST":
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.onboarding_completed = True
            profile.save()
            messages.success(request, "Onboarding completed successfully!")
            return redirect("dashboard")
    else:
        form = ProfileForm(instance=profile)

    return render(request, "profiles/onboarding.html", {"form": form})
