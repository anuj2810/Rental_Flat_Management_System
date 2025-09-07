from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('user_type', 'phone_number', 'profile_image')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {'fields': ('user_type', 'phone_number', 'profile_image')}),
    )
    list_display = ('username', 'email', 'first_name', 'last_name', 'user_type')
    list_filter = ('user_type',)

admin.site.site_header = "Flat Rental System Admin"
admin.site.site_title = "Flat Rental System Admin Portal"
admin.site.index_title = "Welcome to Flat Rental System Admin Portal"
