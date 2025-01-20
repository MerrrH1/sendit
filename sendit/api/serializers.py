from rest_framework import serializers
from sendit_app.models import User, Shipment, Payment, Review
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.validators import UniqueValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField(style={'input_type': 'password'})

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        # Autentikasi dengan model User kustom
        user = authenticate(username=username, password=password)
        
        if user is None:
            raise serializers.ValidationError("Username atau Password salah.")

        # Dapatkan atau buat token
        token, created = Token.objects.get_or_create(user=user)

        # Kirimkan token sebagai bagian dari data yang valid
        data['token'] = token.key
        return data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

class ShipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shipment
        fields = "__all__"
        
class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"
        
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = "__all__"
        

