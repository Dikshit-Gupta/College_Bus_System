from django.contrib import admin

# Register your models here.
from .models import User , Driver , Student

class UserAdmin(admin.ModelAdmin):
    list_display = ("email","role","is_active","created_at")
    search_fields = ("email" , "first_name" , "last_name")

class StudentAdmin(admin.ModelAdmin):
    list_display = ("enrollment_no", "department", "year_of_study", "transport_mode")
    search_fields = ("enrollment_no", "user__first_name", "user__last_name")

class DriverAdmin(admin.ModelAdmin):
    list_display = ("license_number", "license_expiry", "user")
    search_fields = ("license_number", "user__first_name", "user__last_name")