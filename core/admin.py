from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from .models import UserAccountManager
from .forms import UserCreationForm
class UserAdmin(BaseUserAdmin):

    list_display = ('id','email', 'first_name', 'last_name', 'mobile', 'is_staff', 'is_active', 'is_superuser')
    search_fields = ('id','email', 'first_name', 'last_name', 'mobile')

    list_filter = ('is_staff', 'is_active', 'is_superuser')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'mobile', 'address')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),  # Adjusted to include only existing fields
    )

    # Define the fields to be used in the add user form.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'mobile', 'address', 'password1', 'password2'),
        }),
    )

    # Specify the model's ordering
    ordering = ('email',)  # Use a field that exists in your model

    # Customize the form used for adding users.
    add_form = UserCreationForm

admin.site.register(UserAccountManager, UserAdmin)

# Optionally, unregister the default Group model if you don't need it.
admin.site.unregister(Group)
