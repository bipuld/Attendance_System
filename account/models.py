from django.conf import settings
from django.db import models

class UserInfo(models.Model):
    GENDER_CHOOSE = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Others')
    )
    
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name="system_user", 
        primary_key=True
    )
    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOOSE,
        default="male"
    )
    phone = models.CharField(
        max_length=255,
        help_text="If you have more than one number, write them separated by commas."
    )
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    is_verify = models.BooleanField(default=False)
    

    @property
    def full_name(self):
        return f"{self.user.first_name} {self.user.last_name}" if self.user else None
        
    def __str__(self):
        return f"{self.user.id} - {self.first_name} - {self.user.email} {self.user}" if self.user else "Anonymous User"
