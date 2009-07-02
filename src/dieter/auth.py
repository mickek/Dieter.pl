from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User

class EmailBackend(ModelBackend):
    """Authentication backend that uses users' email as the main
    id."""

    def authenticate(self, username=None, password=None):
        try:
            user = User.objects.get(email=username)
        except User.DoesNotExist: #@UndefinedVariable
            return None
        else:
            if user.check_password(password):
                return user
