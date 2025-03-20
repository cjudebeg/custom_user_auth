from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard_view, name="home"),
    # User authentication (complementing django-allauth URLs)
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path(
        "signup/with-profile/",
        views.CombinedSignUpView.as_view(),
        name="signup_with_profile",
    ),
    # User management
    path("account/update/", views.UserUpdateView.as_view(), name="user_update"),
    path("account/delete/", views.UserDeleteView.as_view(), name="user_delete"),
    # Profile management
    path("profile/create/", views.profile_create_view, name="profile_create"),
    path("profile/", views.ProfileDetailView.as_view(), name="profile_detail"),
    path("profile/update/", views.ProfileUpdateView.as_view(), name="profile_update"),
    # Dashboard and onboarding
    path("dashboard/", views.dashboard_view, name="dashboard"),
    path("onboarding/", views.onboarding_view, name="onboarding"),
]
