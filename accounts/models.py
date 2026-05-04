from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    """
    AbstractUser extend गर्दैछौं किनभने
    Django को default User पर्याप्त छैन हाम्रो role logic को लागि
    """
    
    class Role(models.TextChoices):
        ADMIN = 'admin', 'Admin'
        MANAGER = 'manager', 'Manager'  
        STAFF = 'staff', 'Staff'
    
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.STAFF
    )

    # Properties - DB hit नगरी check गर्न
    @property
    def is_admin(self):
        return self.role == self.Role.ADMIN
    
    @property
    def is_manager(self):
        return self.role in [self.Role.ADMIN, self.Role.MANAGER]
    
    def __str__(self):
        return f"{self.username} ({self.role})"