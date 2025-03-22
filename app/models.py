from django.db import models


# Property Model
class Property(models.Model):
    name = models.CharField(max_length=100)  # Property Name
    contact_number = models.CharField(max_length=15)  # Contact Number

    def __str__(self):
        return self.name

# Banner Model
class Banner(models.Model):
    image = models.ImageField(upload_to='banners/')  # Banner Image

    def __str__(self):
        return f"Banner {self.id}"



from django.db import models

class LocationExample(models.Model):
    # Country Choices (2 Countries)
    COUNTRY_CHOICES = [
        ('india', 'India'),
        ('usa', 'USA'),
    ]

    # State Choices (Each Country's States)
    STATE_CHOICES = [
        # India
        ('tamil_nadu', 'Tamil Nadu'),
        ('karnataka', 'Karnataka'),
        ('maharashtra', 'Maharashtra'),
        # USA
        ('california', 'California'),
        ('texas', 'Texas'),
        ('new_york', 'New York'),
    ]

    # District Choices (Each State's Districts)
    DISTRICT_CHOICES = [
        # India → Tamil Nadu
        ('chennai', 'Chennai'),
        ('madurai', 'Madurai'),
        # India → Karnataka
        ('bangalore', 'Bangalore'),
        ('mysore', 'Mysore'),
        # India → Maharashtra
        ('mumbai', 'Mumbai'),
        ('pune', 'Pune'),
        
        # USA → California
        ('los_angeles', 'Los Angeles'),
        ('san_francisco', 'San Francisco'),
        # USA → Texas
        ('houston', 'Houston'),
        ('dallas', 'Dallas'),
        # USA → New York
        ('manhattan', 'Manhattan'),
        ('brooklyn', 'Brooklyn'),
    ]


    country = models.CharField(max_length=20, choices=COUNTRY_CHOICES, default='india')
    state = models.CharField(max_length=20, choices=STATE_CHOICES, default='tamil_nadu')
    district = models.CharField(max_length=20, choices=DISTRICT_CHOICES, default='chennai')
    # role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')

    def __str__(self):
        return f"{self.get_district_display()}, {self.get_state_display()}, {self.get_country_display()} ({self.get_role_display()})"


# Land Listing Model
class LandListing(models.Model):
    district = models.ForeignKey(LocationExample, on_delete=models.CASCADE, related_name="lands")  # District (City)
    image = models.ImageField(upload_to="land_images/")  # Land Image
    title = models.CharField(max_length=255)  # Land Title
    description = models.TextField()  # Short Description
    detail_description = models.TextField()  # Detailed Description
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Price
    latitude = models.FloatField()  # Latitude for Map
    longitude = models.FloatField()  # Longitude for Map

    def __str__(self):
        return self.title
