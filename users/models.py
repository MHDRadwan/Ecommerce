
from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField 
from PIL import Image
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], blank=True)
    address = models.CharField(max_length=255, blank=True)
    country_of_origin = CountryField(blank_label='(select country)', blank=True)
    country_of_residence = CountryField(blank_label='(select country)', blank=True)
    city = models.CharField(max_length=100, blank=True)
    image = models.ImageField(default='profile_pics/placeholder.png',upload_to="profile_pics")
    phone_number = PhoneNumberField(blank=True, null=True) 

    def __str__(self):
        return f'{self.user.username} Profile'

#This method overrides the default save method to resize the uploaded image if it's larger than 300x300 pixels.
#It opens the image, checks its dimensions, resizes it if necessary,and saves it back to the same path.
#This ensures that all images are uniform in size, which can be useful for display purposes.
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.image.path)
