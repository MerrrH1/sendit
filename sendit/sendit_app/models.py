import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    role_choices = (
        ('customer', 'Customer'),
        ('admin', 'Admin'),
        ('courier', 'Courier')
    )
    phone = models.CharField(max_length = 20, blank = True, null = True)
    address = models.TextField()
    role = models.CharField(max_length = 15, choices = role_choices, default = "customer")
    
    def __str__(self):
        return self.username
    
def get_tracking_number():
    dt = datetime.datetime.now()
    year = str(dt.year).zfill(2)
    month = str(dt.month).zfill(2)
    day = str(dt.day).zfill(2)
    hour = str(dt.hour).zfill(2)
    minute = str(dt.minute).zfill(2)
    second = str(dt.second).zfill(2)
    return "SI-0" + year[2:4] + month + day + hour + minute + second
    
class Shipment(models.Model):
    status_choices = (
        ('pending', 'Pending'),
        ('in_transit', 'In Transit'),
        ('delivered', 'Delivered')
    )
    payment_status = (
        ('paid','Paid'),
        ('unpaid', 'Unpaid')
    )
    tracking_number = models.CharField(max_length = 20, default = get_tracking_number, editable = False, unique = True)
    sender = models.CharField(max_length = 50, blank = True, null = True)
    receiver = models.CharField(max_length = 50, blank = True, null = True)
    courier = models.ForeignKey(User, related_name = "courier_shipment", blank = True, null = True, on_delete = models.SET_NULL)
    origin = models.TextField(blank = True, null = True)
    destination = models.TextField(blank = True, null = True)
    status = models.CharField(max_length = 25, choices = status_choices, default = "pending")
    created_by = models.ForeignKey(User, related_name = 'created_by_shipment', blank = True, null = True, on_delete = models.SET_NULL)
    modified_by = models.ForeignKey(User, related_name = 'modified_by_shipment', blank = True, null = True, on_delete = models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add = True)
    last_modified = models.DateTimeField(auto_now = True)
    
    def __str__(self):
        return f"Shipment {self.tracking_number} - {self.status}"
    
class Payment(models.Model):
    payment_status = (
        ('paid', 'Paid'),
        ('unpaid', 'Unpaid')
    )
    payment_choices = (
        ('cash', 'Cash'),
        ('transfer', 'Transfer')
    )
    shipment = models.OneToOneField(Shipment, related_name = 'shipment_payment', on_delete = models.CASCADE)
    amount = models.DecimalField(max_digits = 10, decimal_places = 2, default = 0),
    payment_method = models.CharField(max_length = 15, choices = payment_choices, default = 'cash')
    status = models.CharField(max_length = 15, choices = payment_status, default = 'unpaid')
    created_at = models.DateTimeField(auto_now_add = True)
    last_modified = models.DateTimeField(auto_now = True)
    
    def __str__(self):
        return f"Payment for Shipment {self.shipment.tracking_number}"
    
class Review(models.Model):
    shipment = models.ForeignKey(Shipment, related_name = 'shipment_review', on_delete = models.CASCADE)
    user = models.ForeignKey(User, related_name = 'user_review', on_delete = models.CASCADE)
    rating = models.IntegerField(choices = [(i, str(i)) for i in range(1,6)])
    comment = models.TextField(blank = True, null = True)
    created_at = models.DateTimeField(auto_now_add = True)
    last_modified = models.DateTimeField(auto_now = True)
    
    def __str__(self):
        return f"Review for Shipment {self.shipment.tracking_number}"