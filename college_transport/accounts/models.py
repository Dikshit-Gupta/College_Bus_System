from django.db import models
from django.contrib.auth.models import AbstractUser , PermissionsMixin , BaseUserManager

# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self , email , password=None , **extra_fields):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(email=email , **extra_fields)
        user.set_password(password)
        user.save(using = self._db)
        return user
    def create_superuser(self, email , password = None , **extra_fields):
        extra_fields.setdefault("is_staff" , True)
        extra_fields.setdefault("is_superuser" , True)
        return self.create_user(email, password , **extra_fields)
    

class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=[("student", "Student"), ("driver", "Driver"), ("admin", "Admin")])
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    phone = models.CharField(max_length=15, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()
    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "role"]

    def __str__(self):
        return f"({self.email})({self.role}))"
    

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="student_profile")
    enrollment_no = models.CharField(max_length=30, unique=True)
    department = models.CharField(max_length=50)
    year_of_study = models.IntegerField()
    
    # Transport mode preference
    transport_mode = models.CharField(
        max_length=20,
        choices=[
            ("morning", "Morning Only"),
            ("evening", "Evening Only"),
            ("both", "Morning & Evening"),
            ("none", "No Transport")
        ],
        default="both"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} {self.enrollment_no}"
    
class Driver(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="driver_profile")
    license_number = models.CharField(max_length=50, unique=True)
    license_expiry = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} - {self.license_number}"