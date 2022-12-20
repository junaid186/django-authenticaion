from multiprocessing import context
from os import stat
from pickle import NONE
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializer import SendPasswordEmailSerializer, UserChangePasswordSerializer, UserSerializer
from .serializer import UserLoginSerializer, ResetPasswordSerializer
from .serializer import SendPasswordEmailSerializer
from django.contrib.auth import authenticate
from rest_framework.renderers import JSONRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from .serializer import UserProfileSerializer
from rest_framework.permissions import IsAuthenticated





# generting token manually
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
class UserRegistrationView(APIView):
    def post(self,request,format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            token = get_tokens_for_user(user)
            return Response({'token':token,'msg':'registration success'},
            status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class userLoginView(APIView):
    def post(self, request, format=None):
        seralizer = UserLoginSerializer(data=request.data)
        if seralizer.is_valid(raise_exception=True):
            email = seralizer.data.get("email")
            password = seralizer.data.get("password")
            user = authenticate(email=email,password=password)
            if user is not None:
                token = get_tokens_for_user(user)
                return Response({'token':token,'msg':'login success'},
                status=status.HTTP_200_OK)
            else:
                return Response({"error":{"non_field_errors":["Email or password is not valid"]}},
                status=status.HTTP_404_NOT_FOUND)
        return Response(seralizer.errors,status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request,format=None):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data,status=status.HTTP_200_OK)

class UserChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request,format=None):
        serializer = UserChangePasswordSerializer(data=request.data,
        context = {'user':request.user})
        if serializer.is_valid(raise_exception=True):
            return Response({"msg":"password changed successfully"},
            status=status.HTTP_200_OK)
        return Response(serializer.errors,
        status=status.HTTP_400_BAD_REQUEST)



class SendPasswordEmailView(APIView):
    def post(self,request,format=None):
        serializer = SendPasswordEmailSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
           return Response({"msg":"Password reset link send. Please check your email"},
           status=status.HTTP_200_OK)
        print("Now we are going to give error.")
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class ResetPasswordView(APIView):
    def post(self,request, uid, token, format=None):
        serializer = ResetPasswordSerializer(data=request.data,
        context={"uid":uid,"token":token})
        if serializer.is_valid(raise_exception=True):
            return Response({"msg":"msg':'Password Reset Successfully"},
           status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
