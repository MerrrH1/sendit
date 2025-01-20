from rest_framework.views import APIView
from rest_framework import status
from rest_framework import permissions
from rest_framework.response import Response
from sendit_app.models import User, Shipment, Payment, Review
from api.serializers import UserSerializer, LoginSerializer, ShipmentSerializer, ReviewSerializer, PaymentSerializer
from rest_framework import generics
from rest_framework.authtoken.models import Token
from django.contrib.auth import login as django_login, logout as django_logout
from django.http import HttpResponse, JsonResponse
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from .paginators import CustomPagination

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        
        if serializer.is_valid():
            return Response(
                {
                    'status': 'success',
                    'message': 'Login berhasil',
                    'token': serializer.validated_data['token']
                },
                status=status.HTTP_200_OK
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            # Ambil token dari header Authorization
            token = request.auth  # `request.auth` adalah token yang digunakan oleh user yang terautentikasi

            # Hapus token untuk logout
            token.delete()

            return Response(
                {'message': 'Logout berhasil'},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {'message': 'Gagal melakukan logout', 'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        
class UserListView(APIView):
    def get(self, request, *args, **kwargs):
        users = User.objects.all()
        serializer = UserSerializer(users, many = True)
        return Response(serializer.data, status = status.HTTP_200_OK)
        
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
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        
class PaymentListView(APIView):
    def get(self, request, *args, **kwargs):
        payments = Payment.objects.all()
        serializer = PaymentSerializer(payments, many = True)
        return Response(serializer.data, status = status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        data = {
            'shipments' : request.data.get('shipment'),
            'amount' : request.data.get('amount'),
            'payment_method' : request.data.get('payment_method'),
            'status' : request.data.get('status')
        }
        serializer = PaymentSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            response = {
                'status' : status.HTTP_201_CREATED,
                'message' : "Shipment data created successfully...",
                'data' : serializer.data
            }
            return Response(response, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    
class PaymentDetailView(APIView):
    def get_object(self, id):
        try:
            return Payment.objects.get(id = id)
        except:
            return None
        
    def get(self, request, id, *args, **kwargs):
        payment_instance = self.get_object(id)
        if not payment_instance:
            return Response(
                {
                    'status' : status.HTTP_404_NOT_FOUND,
                    'message' : "Data does not exists...",
                    'data' : {}
                }, status = status.HTTP_404_NOT_FOUND
            )
        serializer = PaymentSerializer(payment_instance)
        response = {
            'status' : status.HTTP_200_OK,
            'message' : "Data Retreived Successfully...",
            'data' : serializer.data
        }
        return Response(response, status.HTTP_200_OK)

    def put(self, request, id, *args, **kwargs):
        payment_instance = self.get_object(id)
        if not payment_instance:
            return Response(
                {
                    'status' : status.HTTP_404_NOT_FOUND,
                    'message' : "Data does not exists...",
                    'data' : {}
                }, status = status.HTTP_404_NOT_FOUND
            )
        data = {
            'shipments' : request.data.get('shipment'),
            'amount' : request.data.get('amount'),
            'payment_method' : request.data.get('payment_method'),
            'status' : request.data.get('status')
        }
        serializer = PaymentSerializer(payment_instance, data = data, partial = True)
        if serializer.is_valid():
            serializer.save()
            response = {
                'status' : status.HTTP_201_CREATED,
                'message' : "Shipment data created successfully...",
                'data' : serializer.data
            }
            return Response(response, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class ReviewtListView(APIView):
    def get(self, request, *args, **kwargs):
        reviews = Review.objects.all()
        serializer = ReviewSerializer(reviews, many = True)
        return Response(serializer.data, status = status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        data = {
            'shipments' : request.data.get('shipment'),
            'user' : request.data.get('user'),
            'rating' : request.data.get('rating'),
            'comment' : request.data.get('comment')
        }
        serializer = ReviewSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            response = {
                'status' : status.HTTP_201_CREATED,
                'message' : "Shipment data created successfully...",
                'data' : serializer.data
            }
            return Response(response, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    
class ReviewDetailView(APIView):
    def get_object(self, id):
        try:
            return Review.objects.get(id = id)
        except:
            return None
        
    def get(self, request, id, *args, **kwargs):
        review_instances = self.get_object(id)
        if not review_instances:
            return Response(
                {
                    'status' : status.HTTP_404_NOT_FOUND,
                    'message' : "Data does not exists...",
                    'data' : {}
                }, status = status.HTTP_404_NOT_FOUND
            )
        serializer = ReviewSerializer(review_instances)
        response = {
            'status' : status.HTTP_200_OK,
            'message' : "Data Retreived Successfully...",
            'data' : serializer.data
        }
        return Response(response, status.HTTP_200_OK)

    def put(self, request, id, *args, **kwargs):
        review_instances = self.get_object(id)
        if not review_instances:
            return Response(
                {
                    'status' : status.HTTP_404_NOT_FOUND,
                    'message' : "Data does not exists...",
                    'data' : {}
                }, status = status.HTTP_404_NOT_FOUND
            )
        data = {
            'shipments' : request.data.get('shipment'),
            'user' : request.data.get('user'),
            'rating' : request.data.get('rating'),
            'comment' : request.data.get('comment')
        }
        serializer = ReviewSerializer(review_instances, data = data, partial = True)
        if serializer.is_valid():
            serializer.save()
            response = {
                'status' : status.HTTP_201_CREATED,
                'message' : "Shipment data created successfully...",
                'data' : serializer.data
            }
            return Response(response, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
