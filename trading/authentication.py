from rest_framework import authentication
from rest_framework import exceptions

from .models import EtUsers, EtAuthTokens
from datetime import datetime


class TradeAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        token = request.META.get('HTTP_AUTHORIZATION')
        if not token:
            return None
        try:
            token_obj = EtAuthTokens.objects.get(token=token.split(' ')[1])
            token_exp = datetime.fromtimestamp(int(token_obj.date_expiration))
            if datetime.now() > token_exp:
                raise exceptions.AuthenticationFailed('The lifetime of this token has expired')
            user = EtUsers.objects.get(login=token_obj.login)
        except EtUsers.DoesNotExist:
            raise exceptions.AuthenticationFailed('No such user')
        except EtAuthTokens.DoesNotExist:
            raise exceptions.AuthenticationFailed('Incorrect authentication token')

        return (user, None)