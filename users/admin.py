from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

# Register your models here.
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'role', 'is_active', 'is_staff')
    list_filter  = ('role', 'is_staff', 'is_superuser', 'is_active')
    fieldsets = (
        (None,               {'fields': ('username', 'password')}),
        ('Personal Info',    {'fields': ('first_name', 'last_name', 'email')}),
        ('Role & Permissions', {
            'fields': (
                'role',
                'is_active',
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions',
            )
        }),
        ('Important dates',  {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'role', 'password1', 'password2', 'is_active', 'is_staff'),
        }),
    )
    search_fields = ('username', 'email', 'role')
    ordering = ('username',)

admin.site.register(CustomUser, CustomUserAdmin)