from .models import Profile
from django.contrib import admin


class adminPage(admin.ModelAdmin):
    fields = (
        'first_name', 'last_name', 'email', 'mobile', 'is_active', 'username', 'image', 'CompanyID', 'Activate_Account')


admin.site.register(Profile, adminPage)
