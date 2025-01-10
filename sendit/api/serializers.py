from rest_framework import serializers
from sendit_app.models import User, Shipment

from django.contrib.auth import authenticate
from rest_framework.validators import UniqueValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password

class RegisterUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required = True, validators = [UniqueValidator(queryset = User.objects.all())])
    password1 = serializers.CharField(write_only = True, required = True, validators = [validate_password])
    password2 = serializers.CharField(write_only = True, required = True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'phone', 'address']
        extra_kwargs = {
            'password1' : {'write_only' : True},
            'password2' : {'write_only' : True}
        }
    
    def validate(self, attrs):
        if attrs['password1'] != attrs['password2']:
            raise serializers.ValidationError({
                'password' : "Kata Sandi dan Ulang Kata Sandi Tidak Sama..."
            })
        return attrs
    
    def create(self, validated_data):
        user = User.objects.create(
            username = validated_data['username'],
            email = validated_data['email'],
            phone = validated_data['phone'],
            address = validated_data['address'],
            first_name = validated_data['first_name'],
            last_name = validated_data['last_name']
        )
        user.set_password(validated_data['password1'])
        user.save()
        return user

class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField()
    
    def validate(self, data):
        username = data.get('username', '')
        password = data.get('password', '')
        
        if username and password:
            user = authenticate(username = username, password = password)
            if user:
                if user.is_active:
                    data['user'] = user
                else:
                    msg = "Status pengguna tidak aktif..."
                    raise ValidationError({'message' : msg})
            else:
                msg = "Anda tidak memiliki akses masuk..."
                raise ValidationError({'message' : msg})
        else:
            msg = "Mohon mengisi kolom username dan password..."
            raise ValidationError({'message' : msg})
        return data
    
    class Meta:
        model = User
        fields = ['username', 'password']

class ShipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shipment
        fields = "__all__"