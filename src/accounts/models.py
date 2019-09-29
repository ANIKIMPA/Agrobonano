from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Usuario(AbstractUser):
    pass

    def get_absolute_url(self):
        return reverse("accounts:edit-usuario", kwargs={"usuario_id": self.pk})

    def get_delete_url(self):
        return reverse("accounts:delete-usuario", kwargs={"usuario_id": self.pk})
    
    
    