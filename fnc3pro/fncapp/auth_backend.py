from django.contrib.auth.models import User
from django.contrib.auth.backends import ModelBackend

class EmailOrUsernameModelBackend(ModelBackend):
    """
    Autenticazione basata su email o username.
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # Cerca l'utente usando username o email
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            try:
                user = User.objects.get(email=username)
            except User.DoesNotExist:
                return None

        # Verifica la password e ritorna l'utente se valida
        if user.check_password(password):
            return user
        return None
