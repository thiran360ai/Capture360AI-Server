from django.db import models

# Create your models here.

class Contact(models.Model):
    name =models.CharField(max_length=255,null=True,blank=True) 
    mobile =models.CharField(max_length=255,null=True,blank=True)    
    payment = models.CharField(max_length=255,null=True,blank=True)
    payment_status = models.CharField(max_length=255,null=True,blank=True,default='pending')
    status =models.CharField(max_length=255,null=True,blank=True)
    date = models.DateTimeField(auto_now_add=True)