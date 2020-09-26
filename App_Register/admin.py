from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model

from .models import UserEmailConfirmed

from .forms import UserCreationForm, UserChangeForm
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin 
# Register your models here.

User = get_user_model()

admin.site.unregister(Group)

class UserAdmin(BaseUserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm

    list_display = ('email', 'first_name', 'last_name', 'is_active', 'is_admin', 'is_staff')
    list_filter = ('is_admin',)

    fieldsets = (
        (None,{'fields': ('email', 'first_name', 'last_name', 'password')}),
        ('Permission', {'fields': ('is_admin', 'is_staff', )})
    )

    add_fieldsets = (
        (None, {'fields': ('email', 'first_name', 'last_name', 'is_active', 'password1', 'password2')}),
        ('Permission', {'fields': ('is_admin', 'is_staff', )})
    )

    ordering = ('email',)
    search_fields = ('email',)
    filter_horizontal = ()


admin.site.register(User, UserAdmin)

class EmaiConfirmedAdmin(admin.ModelAdmin):
    list_display = ( 'user', 'first_name', 'last_name', 'activation_key', 'email_confirmed')

    def first_name(self, obj):
        return obj.user.first_name

    def last_name(self, obj):
        return obj.user.last_name

admin.site.register(UserEmailConfirmed, EmaiConfirmedAdmin)