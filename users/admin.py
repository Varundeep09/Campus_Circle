from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Profile

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        (None, {'fields': ('role', 'is_alumni_verified')}),
    )
    list_display = ('username', 'email', 'role', 'is_alumni_verified', 'is_staff', 'is_active')
    list_filter = ('role', 'is_alumni_verified', 'is_staff', 'is_active')
    search_fields = ('username', 'email')

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'college', 'graduation_year')
    search_fields = ('user__username', 'college')