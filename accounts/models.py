from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("L'email est obligatoire.")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    ROLES = (
        ('ADMIN', 'Administrateur'),
        ('DOCTOR', 'Médecin'),
        ('ASSISTANT', 'Assistant médecin'),
        ('PATIENT', 'Patient'),
        ('DIRECTOR', 'Directeur'),
    )
    SUB_ROLES = (
        ('STUDENT', 'Étudiant'),
        ('ATS', 'ATS'),
        ('TEACHER', 'Enseignant'),
    )
    role = models.CharField(max_length=10, choices=ROLES)
    sub_role = models.CharField(max_length=10, choices=SUB_ROLES, null=True, blank=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    is_active = models.BooleanField(default=False)
    email_verified = models.BooleanField(default=False) 

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return f"{self.email} ({self.role})"