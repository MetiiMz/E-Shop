from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserCreationForm, UserChangeForm
from .models import User, OtpCode


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('full_name', 'email', 'phone_number', 'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ['full_name', 'email', 'phone_number', 'password']}),
        ('permissions', {'fields': ['is_active', 'is_admin', 'is_superuser', 'last_login', 'groups', 'user_permissions']})
    )
    add_fieldsets = (
        (None, {'fields': ['full_name', 'email', 'phone_number', 'password1', 'password2']}),
    )
    search_fields = ('full_name', 'email')
    ordering = ('full_name',)
    filter_horizontal = ('groups', 'user_permissions')


@admin.register(OtpCode)
class OtpCodeAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'code', 'created')


admin.site.register(User, UserAdmin)
