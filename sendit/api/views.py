from rest_framework.views import APIView
from rest_framework import status
from rest_framework import permissions
from rest_framework.response import Response
from sendit_app.models import User, Shipment, Payment, Review
from api.serializers import RegisterUserSerializer, LoginSerializer, ShipmentSerializer
from rest_framework import generics
from rest_framework.authtoken.models import Token
from django.contrib.auth import login as django_login, logout as django_logout
from django.http import HttpResponse, JsonResponse
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from .paginators import CustomPagination

class RegisterUserView(APIView):
    serializer_class = RegisterUserSerializer
    
    def post(self, request, format = None):
        serializer = self.serializer_class(data = request.data)
        if serializer.is_valid():
            serializer.save()
            response_data = {
                'status' : status.HTTP_201_CREATED,
                'message' : "Selamat Anda Telah Terdaftar...",
                'data' : serializer.data
            }
            return Response(response_data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    serializer_class = LoginSerializer
    
    def post(self, request):
        serializer = LoginSerializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        user = serializer.validated_data['user']
        django_login(request, user)
        token, created = Token.objects.get_or_create(user = user)
        return JsonResponse({
            'status' : 200,
            'message' : "Selamat anda berhasil masuk...",
            'data' : {
                'token' : token.key,
                'id' : user.id,
                'first_name' : user.first_name,
                'last_name' : user.last_name,
                'password' : user.password,
                'email' : user.email,
                'is_active' : user.is_active,
                'role' : user.role
            }
        })
        
class ShipmentListView(APIView):
    def get(self, request, *args, **kwargs):
        shipments = Shipment.objects.all()
        serializer = ShipmentSerializer(shipments, many = True)
        return Response(serializer.data, status = status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        data = {
            'sender' : request.data.get('sender'),
            'receiver' : request.data.get('receiver'),
            'courier' : request.data.get('courier'),
            'origin' : request.data.get('origin'),
            'destination' : request.data.get('destination')
        }
        serializer = ShipmentSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            response = {
                'status' : status.HTTP_201_CREATED,
                'message' : "Shipment data created successfully...",
                'data' : serializer.data
            }
            return Response(response, status = status.HTTP_201_CREATED)
        return Response(response.errors, status = status.HTTP_400_BAD_REQUEST)

    
class ShipmentDetailView(APIView):
    def get_object(self, id):
        try:
            return Shipment.objects.get(id = id)
        except:
            return None
        
    def get(self, request, id, *args, **kwargs):
        shipment_instance = self.get_object(id)
        if not shipment_instance:
            return Response(
                {
                    'status' : status.HTTP_404_NOT_FOUND,
                    'message' : "Data does not exists...",
                    'data' : {}
                }, status = status.HTTP_404_NOT_FOUND
            )
        serializer = ShipmentSerializer(shipment_instance)
        response = {
            'status' : status.HTTP_200_OK,
            'message' : "Data Retreived Successfully...",
            'data' : serializer.data
        }
        return Response(response, status.HTTP_200_OK)

    def put(self, request, id, *args, **kwargs):
        shipment_instance = self.get_object(id)
        if not shipment_instance:
            return Response(
                {
                    'status' : status.HTTP_404_NOT_FOUND,
                    'message' : "Data does not exists...",
                    'data' : {}
                }, status = status.HTTP_404_NOT_FOUND
            )
        data = {
            'sender' : request.data.get('sender'),
            'receiver' : request.data.get('receiver'),
            'courier' : request.data.get('courier'),
            'origin' : request.data.get('origin'),
            'destination' : request.data.get('destination')
        }
        serializer = ShipmentSerializer(shipment_instance, data = data, partial = True)
        if serializer.is_valid():
            serializer.save()
            response = {
                'status' : status.HTTP_201_CREATED,
                'message' : "Shipment data created successfully...",
                'data' : serializer.data
            }
            return Response(response, status = status.HTTP_201_CREATED)
        return Response(response.errors, status = status.HTTP_400_BAD_REQUEST)
    
class ShipmentView(APIView):
    authentication_classes = [BasicAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        shipments = Shipment.objects.filter(status = "pending")
        serializer = ShipmentSerializer(shipments, many = True)
        response = {
            'status' : status.HTTP_200_OK,
            'message' : "Pembacaan seluruh data berhasil...",
            'user' : str(request.user),
            'auth' : str(request.auth),
            'data' : serializer.data
        }
        return Response(response, status = status.HTTP_200_OK)