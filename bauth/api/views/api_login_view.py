from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import transaction
from rest_framework import status
from bauth.api.serializers.login_serializer import LoginSerializer


class APILoginView(APIView):
    serializer_class = LoginSerializer

    @csrf_exempt
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user_instance = authenticate(username=serializer.validated_data['username'],
                         password=serializer.validated_data['password'])

            if user_instance:
                with transaction.atomic():
                    token, created = Token.objects.get_or_create(user_id=user_instance.pk)
                    return Response({'token': token.key, 'success': True})
        return Response({'message': 'Cannot login with provided credentials.', 'success': False},
                        status=status.HTTP_400_BAD_REQUEST)
