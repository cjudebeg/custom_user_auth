from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, Profile


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'


class CustomUserAdmin(UserAdmin):
    """
    Admin configuration for the CustomUser model.
    """
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    inlines = (ProfileInline, )
    
    list_display = ('email', 'display_name', 'first_name', 'last_name', 'is_active', 'is_staff', 'email_verified')
    list_filter = ('is_active', 'is_staff', 'is_superuser', 'email_verified')
    search_fields = ('email', 'first_name', 'last_name', 'display_name')
    ordering = ('email',)
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'display_name')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'email_verified', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined', 'created_at', 'updated_at')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active'),
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at')


class ProfileAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Profile model.
    """
    list_display = ('user', 'state', 'clearance_level', 'onboarding_completed')
    list_filter = ('state', 'clearance_level', 'onboarding_completed')
    search_fields = ('user__email', 'user__first_name', 'user__last_name', 'suburb')
    raw_id_fields = ('user',)
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        (_('User Information'), {
            'fields': ('user',)
        }),
        (_('Personal Details'), {
            'fields': ('middle_name', 'date_of_birth')
        }),
        (_('Location'), {
            'fields': ('state', 'suburb')
        }),
        (_('Security Clearance'), {
            'fields': ('clearance_level', 'clearance_no', 'clearance_expiry')
        }),
        (_('Skills & Onboarding'), {
            'fields': ('skill_sets', 'skill_level', 'onboarding_completed')
        }),
        (_('Timestamps'), {
            'fields': ('created_at', 'updated_at')
        }),
    )


# Register the models with their admin classes
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Profile, ProfileAdmin)
