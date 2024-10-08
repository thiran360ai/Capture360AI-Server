# from django.contrib.auth.models import AbstractUser
from django.db import models
# from .models import VideoUpload
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
    
    def __str__(self)-> str:   
        return self.total_floors
    
class Plan(models.Model):
    project=models.ForeignKey(Post,on_delete=models.CASCADE,blank=True,null=True)
    floor=models.ForeignKey(ItemList,on_delete=models.CASCADE,blank=True,null=True)
    floor_or_name=models.CharField(max_length=255,blank=True,null=True)
    image=models.ImageField(null=True,blank=True)    
    
    def __str__(self)-> str: 
        return self.floor_or_name or "Unnamed Plan"

class Location(models.Model):
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    latitude = models.FloatField()
    longitude = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
# models.py
class VideoUpload(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    floor = models.ForeignKey(ItemList, on_delete=models.CASCADE, blank=True, null=True)
    description = models.TextField()
    file = models.FileField(upload_to='videos/', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='thumbnails/', blank=True, null=True)
    upload_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, blank=True, null=True)


from django.db import models
from django.utils import timezone

class VideoFrame(models.Model):
    video = models.ForeignKey(VideoUpload, on_delete=models.CASCADE)
    frame_number = models.IntegerField()
    image = models.ImageField(upload_to='video_frames/')
    timestamp = models.DateTimeField(auto_now_add=True)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, blank=True, null=True)


# class Marker(models.Model):
#     plan = models.ForeignKey(Plan, related_name='markers', on_delete=models.CASCADE)
#     x = models.IntegerField()
#     y = models.IntegerField()
#     distance_to_previous_marker = models.FloatField(null=True, blank=True)
#     distance_to_next_marker = models.FloatField(null=True, blank=True)

#     def __str__(self):
#         return f"Marker at ({self.x}, {self.y})"

#     def calculate_distance(self, other_marker):
#         return math.sqrt((self.x - other_marker.x)**2 + (self.y - other_marker.y)**2)

#     def save(self, *args, **kwargs):
#         super().save(*args, **kwargs)
#         markers = list(self.plan.markers.all())
#         idx = markers.index(self)
        
#         # Calculate distance to the previous marker
#         if idx > 0:
#             previous_marker = markers[idx - 1]
#             self.distance_to_previous_marker = self.calculate_distance(previous_marker)
#         else:
#             self.distance_to_previous_marker = None

#         # Calculate distance to the next marker
#         if idx < len(markers) - 1:
#             next_marker = markers[idx + 1]
#             self.distance_to_next_marker = self.calculate_distance(next_marker)
#         else:
#             self.distance_to_next_marker = None

#         super().save(update_fields=['distance_to_previous_marker', 'distance_to_next_marker'])

class Marker(models.Model):
    plan = models.ForeignKey(Plan, related_name='markers', on_delete=models.CASCADE)
    x = models.IntegerField()
    y = models.IntegerField()
    distance = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"Marker at ({self.x}, {self.y})"


class Customer(models.Model):
    COURSE_CHOICES = (
        ('React Development', 'React Development'),
        ('React Native Development', 'React Native Development'),
         ('Android Java Development', 'Android Java Development'),
        ('PHP Laravel Development', 'PHP Laravel Development'),
         ('Python Django Development', 'Python Django Development')
        # ('member', 'React Native Development'),
    )
    # role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='member')
    username = models.CharField(max_length=50,null=True,blank=True)
    email_id = models.CharField(max_length=255,null=True,blank=True)
    course = models.CharField(max_length=100,choices=COURSE_CHOICES,null=True,blank=True)
    mobile = models.CharField(max_length=10,null=True,blank=True)
    designation= models.CharField(max_length=200,null=True,blank=True)
    college_name = models.CharField(max_length=255,null=True,blank=True)
    address =models.CharField(max_length=255,null=True,blank=True)
    resume= models.FileField(upload_to='uploads/Resume',null=True,blank=True)

    def _str_(self) -> str:
        return self.username
    
class SaveJson(models.Model):
    name= models.CharField(max_length=255,null=True,blank=True)
    data=models.JSONField(null=True,blank=True)
    
    