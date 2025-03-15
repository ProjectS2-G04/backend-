from django.db import models

from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

from .managers import CustomUserManager

class User(AbstractUser):

    ROLE_CHOICES = [
 
        ("etudiant", "Étudiant"),
        ("enseignant", "Enseignant"),
        ("ATS", "ATS"),
        
        ("medecin", "Médecin"),
        ("assistant_medical", "Assistant Médical"),
        ("directeur", "Directeur"),
    ]
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="etudiant")
    username = None
    email =models.EmailField(_('email address'), unique= True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ([])
    objects = CustomUserManager()

    def __str__(self):
        return self.email
    




class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image=models.ImageField(upload_to='profile_pics'  ,default='profile_pics/image.jpg')
    
    def __str__(self):
        return f"{self.user.email}'s Profile"
    
def validate_esi_sba_email(value):

    if not value.endswith("@esi-sba.dz"):
        raise ValidationError("Email must end with '@esi-sba.dz'.")    
    
    
class ListePatient(models.Model):
    email = models.EmailField(max_length=100 , unique=True ,validators=[validate_esi_sba_email])
    def __str__(self):
        return self.email
