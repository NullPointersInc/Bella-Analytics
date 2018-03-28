from django.db import models
import bcrypt

# Create your models here.

class User(models.Model):
    user_name = models.CharField(max_length=64, primary_key=True)
    full_name = models.CharField(max_length=64)
    password = models.CharField(max_length=128)

    def save(self, *args, **kwargs):
        self.password = bcrypt.hashpw(self.password.encode(), bcrypt.gensalt(5)).decode()
        super().save(*args, **kwargs)
                
