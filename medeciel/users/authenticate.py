from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()

class EmailAuthBackend(ModelBackend):
    """
    Custom authentication backend that allows users to log in with their email.
    """
    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            user = User.objects.get(email=email)  
            if user.check_password(password):  # Verify password
                return user
        except User.DoesNotExist:
            return None
