from django.contrib.sessions.models import Session
from django.utils import timezone

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken

from apps.base.views import delete_sessions
from apps.users.api.serializers import UserTokenSerializer

class UserToken(APIView):
    def get(self, request, *args, **kwargs):
        username = request.GET.get('username')
        try:
            user_token = Token.objects.get(
                user = UserTokenSerializer().Meta.model.objects.filter(username = username).first()
            )
            return Response({
                'token': user_token.key
            })
        except:
            return Response({
                'error': 'Credenciales enviadas incorrectas'
            }, status= status.HTTP_400_BAD_REQUEST)


class Login(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        login_serializer = self.serializer_class(data=request.data, context={'request': request})
        if login_serializer.is_valid():
            user = login_serializer.validated_data['user']
            if user.is_active:
                token, created = Token.objects.get_or_create(user=user)
                user_serializer = UserTokenSerializer(user)
                if created:
                    return Response({
                        'token': token.key,
                        'user': user_serializer.data,
                        'message': 'Inicio de Sesión Exitoso',
                    }, status=status.HTTP_201_CREATED)
                else:
                    delete_sessions(user)
                    token.delete()
                    token = Token.objects.create(user=user)
                    return Response({
                        'token': token.key,
                        'user': user_serializer.data,
                        'message': 'Inicio de Sesión Exitoso',
                    }, status=status.HTTP_201_CREATED)
            else:
                return Response({'error': 'Este usuario no puede iniciar sesión'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'error': 'Nombre de usuario o contraseña incorrectos.'}, status=status.HTTP_400_BAD_REQUEST)


class Logout(APIView):

    def post(self, request, *args, **kwargs):
        token = Token.objects.filter(key=request.POST['token']).first()

        if token:
            user = token.user

            delete_sessions(user)
            token.delete()

            session_message = 'Sesiones de usuario eliminadas.'
            token_message = 'Token eliminado.'
            return Response({
                'token_message': token_message,
                'session_message': session_message,
            }, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'No se ha encontrado un usuario con este token'},
                            status=status.HTTP_400_BAD_REQUEST)
