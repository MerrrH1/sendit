from django.urls import path, include
from api import views
from rest_framework.urlpatterns import format_suffix_patterns
from api.views import RegisterUserView, LoginView, ShipmentView, ShipmentListView, ShipmentDetailView

app_name = 'api'

urlpatterns = [
    path('api/register', views.RegisterUserView.as_view()),
    path('api/login', views.LoginView.as_view()),
    path('api/shipment', views.ShipmentListView.as_view()),
    path('api/shipment/<int:id>', views.ShipmentDetailView.as_view()),
    path('api/shipment_auth', views.ShipmentView.as_view()),
]