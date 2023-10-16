from django.contrib import admin

from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    model = User
    list_display = ('id', 'email', 'is_active', 'is_staff', 'is_superuser', 'last_login')
