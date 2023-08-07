from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate
from .serializers import AuthorizationValidateSerializer, RegistrationValidateSerializer
from django.contrib.auth.models import User


@api_view(['GET'])
def registration_api_view(request):
    serializer = RegistrationValidateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    username = serializer.validated_data.get('username')
    password = serializer.validated_data.get('password')

    user = User.objects.create_user(username=username, password=password)
    return Response(status=201, data={'user_is': user.id})


@api_view(['POST'])
def authorization_api_view(request):
    # Step0: Validation
    serializer = AuthorizationValidateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    # Step1: Get data from client
    username = serializer.validated_data.get('username')
    password = serializer.validated_data.get('password')
    # Step2: Search user by credentials
    user = authenticate(username=username, password=password)
    # Step3: Return Key
    if user is not None:
        token_, created = Token.objects.get_or_create(user=user)
        return Response(data={'key': token_.key})
    # Step4: Return Error
    return Response(status=401, data={'message': "user is not found"})
