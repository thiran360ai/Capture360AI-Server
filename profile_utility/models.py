# from django.contrib.auth.models import AbstractUser
from django.db import models

# class CustomUser(models.Model):
#     name = models.CharField(max_length=255)
#     email = models.EmailField(unique=True)
#     ROLE_CHOICES = (
#         ('admin', 'Admin'),
#         ('member', 'Member'),
#     )
#     role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='member')
#     location = models.CharField(max_length=255)
#     password= models.CharField(max_length=255)
# CustomUser.groups.field.related_name = 'custom_user_groups'
# CustomUser.user_permissions.field.related_name = 'custom_user_permissions'
from django.contrib.auth.models import AbstractUser
from rest_framework.authtoken.models import Token


class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('member', 'Member'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='member')
    location = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    
    # Specify unique related names for reverse accessors
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        related_name='customuser_set',  # Unique related name for groups
        related_query_name='user',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        related_name='customuser_set',  # Unique related name for user permissions
        related_query_name='user',
    )  # Remove the comma here
    def __str__(self) -> str:
        return self.username

class Post(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE,blank=True,null=True)
    project_name=models.CharField(max_length=255,blank=True,null=True)
    company_name=models.CharField(max_length=255,blank=True,null=True)
    location=models.CharField(max_length=255,blank=True,null=True)
    
    def __str__(self) -> str:
        return self.project_name
    
class ItemList(models.Model):
    project=models.ForeignKey(Post,on_delete=models.CASCADE,blank=True,null=True)
    image=models.ImageField(null=True,blank=True)
    total_floors=models.CharField(max_length=255,blank=True,null=True)
    no_of_employees=models.CharField(max_length=255,blank=True,null=True)
    
    def __str__(self) -> str:   
        return self.total_floors
    
class Plan(models.Model):
    project=models.ForeignKey(Post,on_delete=models.CASCADE,blank=True,null=True)
    floor=models.ForeignKey(ItemList,on_delete=models.CASCADE,blank=True,null=True)
    floor_or_name=models.CharField(max_length=255,blank=True,null=True)
    image=models.ImageField(null=True,blank=True)    
    