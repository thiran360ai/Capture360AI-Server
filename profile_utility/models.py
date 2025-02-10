from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('member', 'Member'),
    )
    
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='member')
    location = models.CharField(max_length=255)
       # Specify unique related names for reverse accessors
    groups = models.ManyToManyField('auth.Group',verbose_name='groups',blank=True,related_name='customuser_set')
    user_permissions = models.ManyToManyField(
        'auth.Permission',verbose_name='user permissions',blank=True,related_name='customuser_set',  related_query_name='user',
    )  # Remove the comma here
    def __str__(self) -> str:
        return self.username
    
    

class Post(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    project_name = models.CharField(max_length=255, blank=True, null=True)
    company_name = models.CharField(max_length=255, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self) -> str:
        return self.project_name

class ItemList(models.Model):
    project = models.ForeignKey(Post, on_delete=models.CASCADE, blank=True, null=True)
    image = models.ImageField(null=True, blank=True)
    total_floors = models.CharField(max_length=255, blank=True, null=True)
    no_of_employees = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self) -> str:
        return self.total_floors or "Unnamed Item"

class Plan(models.Model):
    project = models.ForeignKey(Post, on_delete=models.CASCADE, blank=True, null=True)
    floor = models.ForeignKey(ItemList, on_delete=models.CASCADE, blank=True, null=True)
    floor_or_name = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(null=True, blank=True)

    def __str__(self) -> str:
        return self.floor_or_name or "Unnamed Plan"

class Location(models.Model):
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE,blank=True, null=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

class SaveJson(models.Model):
    project = models.ForeignKey(Post, on_delete=models.CASCADE,blank=True, null=True)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE,blank=True, null=True)
    floor = models.ForeignKey(ItemList, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    data = models.JSONField(null=True, blank=True)
    
    # def get_floor(self):
    #     return self.plan.floor if self.plan else None

    def __str__(self) -> str:
        return self.name

class VideoUpload(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    floor = models.ForeignKey(ItemList, on_delete=models.CASCADE, blank=True, null=True)
    description = models.TextField()
    file = models.FileField(upload_to='videos/', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='thumbnails/', blank=True, null=True)
    upload_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, blank=True, null=True)
    json = models.ForeignKey(SaveJson, on_delete=models.CASCADE, blank=True, null=True)


class VideoFrame(models.Model):
    video = models.ForeignKey(VideoUpload, on_delete=models.CASCADE)
    frame_number = models.IntegerField()
    image = models.ImageField(upload_to='video_frames/')
    timestamp = models.DateTimeField(auto_now_add=True)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, blank=True, null=True)
    json = models.ForeignKey(SaveJson, on_delete=models.CASCADE, blank=True, null=True)

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
        ('Python Django Development', 'Python Django Development'),
    )

    username = models.CharField(max_length=50, null=True, blank=True)
    email_id = models.CharField(max_length=255, null=True, blank=True)
    course = models.CharField(max_length=100, choices=COURSE_CHOICES, null=True, blank=True)
    mobile = models.CharField(max_length=10, null=True, blank=True)
    designation = models.CharField(max_length=200, null=True, blank=True)
    college_name = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    resume = models.FileField(upload_to='uploads/Resume', null=True, blank=True)

    def __str__(self) -> str:
        return self.username or "Unnamed Customer"

