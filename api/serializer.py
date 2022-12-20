from dataclasses import fields
import email
from pyexpat import model
from tkinter.ttk import Style
from unittest.util import _MAX_LENGTH
from rest_framework import serializers
from .models import MyUser
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from .utils import Util
from rest_framework.response import Response



class UserSerializer(serializers.ModelSerializer):
    # password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)
    class Meta:
        model = MyUser
        fields = ['email', 'name', 'password']
        extra_kwargs={
            'password':{'write_only':True}
        }

    def validate(self, attrs):
        # password = attrs.get('password')
        # password2 = attrs.get('password2')
        # if password != password2:
        #     raise serializers.ValidationError("Password and Confirm Password doesn't match")
        print("validation done")
        return attrs

    def create(self, validate_data):
     return MyUser.objects.create_user(**validate_data)

class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    class Meta:
        model = MyUser
        fields = ['email','password']


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ['id', 'email', 'name']

class UserChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField()
    password2 = serializers.CharField()
    class Meta:
        fields = ['password','password2']

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        user = self.context.get('user')
        if password != password2:
            raise serializers.ValidationError("password and confrim password doesn't match")
        user.set_password(password)
        user.save()
        return attrs



class SendPasswordEmailSerializer(serializers.Serializer):
    email = serializers.CharField()
    class Meta:
        fields = ['email']
    def validate(self, attrs):
        email = attrs.get("email")
        if MyUser.objects.filter(email = email).exists():
            user = MyUser.objects.get(email = email)
            uid = urlsafe_base64_encode(force_bytes(user.id))
            print("Encode user id is: ",uid)
            token = PasswordResetTokenGenerator().make_token(user=user)
            print("token is: ", token)
            link = 'http://localhost:3000/api/user/reset/'+uid+'/'+token
            print("Password Reset Link is: ",link)
            body = 'click following link to reset your password\n'+link
            data = {
                "subject":"Rest Your Password",
                'body':body,
                'to_email':user.email
            }
            Util.send_email(data)
            return attrs
        else:
                raise serializers.ValidationError("This email is not registered")
            # raise ValueError("You are not register user")

class ResetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField()
    password2 = serializers.CharField()
    class Meta:
        fields = ['password','password2']

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            password2 = attrs.get('password2')
            uid = self.context.get('uid')
            token = self.context.get('token')
            if password != password2:
                raise serializers.ValidationError("password and confrim password doesn't match")
            id = smart_str(urlsafe_base64_decode(uid))
            user = MyUser.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise serializers.ValidationError('Token is not Valid or Expired')
            user.set_password(password)
            user.save()
            return attrs
        except DjangoUnicodeDecodeError as identifier:
            PasswordResetTokenGenerator().check_token(user, token)
            raise serializers.ValidationError('Token is not Valid or Expired')
