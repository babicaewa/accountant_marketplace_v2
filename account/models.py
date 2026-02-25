from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
import datetime

class Service(models.Model):
    service_name = models.CharField(max_length=255)

    def __str__(self):
        return self.service_name

class Languages(models.Model):
    language = models.CharField(max_length=255)

    def __str__(self): 
         return self.language

class Professional(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    bio = models.TextField()
    bio_quote = models.TextField()
    services_available = models.ManyToManyField(Service, through='ServiceInfo')
    languages_spoken = models.ManyToManyField(Languages)

    def __str__(self): 
         return self.first_name + " " + self.last_name
    
class Client(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    def __str__(self): 
         return self.first_name + " " + self.last_name
    
class OfficeLocations(models.Model):
    professional = models.ForeignKey(Professional, on_delete=models.CASCADE)
    address = models.CharField(max_length=1000, null=True)
    city = models.CharField(max_length=1000, null=True)
    province = models.CharField(max_length=2, null=True)
    postal_code = models.CharField(max_length=7, null=True)
    lat = models.FloatField()
    long = models.FloatField()

    def __str__(self):
        return f"{self.address} - {self.professional.first_name} {self.professional.last_name}"

class ExperienceDetails(models.Model):
    professional = models.ForeignKey(Professional, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=255)
    role = models.CharField(max_length=255)
    start_year = models.IntegerField(max_length=4)
    end_year = models.IntegerField(max_length=4, null=True, blank=True)
    focus = models.TextField()

    def __str__(self):
        return self.professional.first_name + " " + self.professional.last_name + " " + self.role + " " + str(self.start_year)

class Reviews(models.Model):
    professional = models.ForeignKey(Professional, related_name="reviews", on_delete=models.CASCADE)
    date_posted = models.DateTimeField()
    review_rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    review_text = models.TextField()

    def __str__(self): 
         return f"{self.professional.first_name} {self.professional.last_name} {self.date_posted} Rating:{self.review_rating}"

class ServiceInfo(models.Model):
    professional = models.ForeignKey(Professional, related_name="professional_services", on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    fee = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.professional.first_name + " " + self.professional.last_name + " " + self.service.service_name + " " + str(self.fee)

    



# Create your models here.
