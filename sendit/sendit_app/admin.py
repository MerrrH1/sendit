from django.contrib import admin
from sendit_app.models import User, Shipment, Payment, Review

admin.site.register(User)
admin.site.register(Shipment)
admin.site.register(Payment)
admin.site.register(Review)