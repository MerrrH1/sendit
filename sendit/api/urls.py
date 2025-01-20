from django.urls import path, include
from api import views
from rest_framework.urlpatterns import format_suffix_patterns
from api.views import UserListView, LoginView, ShipmentListView, ShipmentDetailView, PaymentListView, PaymentDetailView, ReviewtListView, ReviewDetailView, LogoutView

app_name = 'api'

urlpatterns = [
    path('api/login', views.LoginView.as_view()),
    path('api/logout', views.LogoutView.as_view()),
    path('api/user', views.UserListView.as_view()),
    path('api/shipment', views.ShipmentListView.as_view()),
    path('api/shipment/<int:id>', views.ShipmentDetailView.as_view()),
    path('api/payment', views.PaymentListView.as_view()),
    path('api/payment/<int:id>', views.PaymentDetailView.as_view()),
    path('api/review', views.ReviewtListView.as_view()),
    path('api/review/<int:id>', views.ReviewDetailView.as_view())
]