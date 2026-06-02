from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator,MaxValueValidator
from phonenumber_field.modelfields import PhoneNumberField

class UserProfile(AbstractUser):
     age = models.PositiveSmallIntegerField(validators=[MinValueValidator(18),MaxValueValidator(60)],
                                            null=True ,blank=True)
     phone_number =  PhoneNumberField(null=True,blank=True)
     avatar = models.ImageField(upload_to='user_images',null=True,blank=True)
     StatusChoices = (
     ('gold','gold'), #75%
     ('silver','silver'), #50%
     ('bronze','bronze'), #25%
     ('simple','simple') #0%
     )
     status = models.CharField(max_length=30,choices=StatusChoices,default='simple')
     data_register = models.DateField(auto_now_add=True)

     def __str__(self):
         return f'{self.first_name},{self.last_name}'
