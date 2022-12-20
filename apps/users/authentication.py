from django.utils import timezone
from django.conf import settings
from datetime import timedelta

from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed

from apps.base.views import delete_sessions

class ExpiringTokenAuthentication(TokenAuthentication):
    expired = False

    def expires_in(self, token):
        time_elapsed = timezone.now() - token.created
        left_time = timedelta(seconds=settings.TOKEN_EXPIRED_AFTER_SECONDS) - time_elapsed
        return left_time

    def is_token_expired(self, token):
        return self.expires_in(token) < timedelta(seconds=0)

    def token_expire_handler(self, token):
        is_expired = self.is_token_expired(token)
        if is_expired:
            self.expired = True
            user = token.user
            token.delete()
            token = self.get_model().objects.create(user=user)

        return is_expired, token

    def authenticate_credentials(self, key):
        message, token, user = None, None, None
        try:
            token = self.get_model().objects.select_related('user').get(key=key)

            # Verificar si el usuario esta activo
            user = token.user
            if not token.user.is_active:
                message = 'Usuario eliminado o inactivo'

            # Verificar si el token del usuario expiro
            is_expired = self.token_expire_handler(token)
            if is_expired:
                message = 'Su Token ha expirado'

        except self.get_model().DoesNotExist:
            message = 'Token inválido'
            self.expired = True

        return user, token, message, self.expired
