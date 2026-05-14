from django.db import models

class ServiceProvider_Model(models.Model):
    username = models.CharField(max_length=300)
    email = models.EmailField(max_length=400)
    password = models.CharField(max_length=300)
    phoneno = models.CharField(max_length=300)
    country = models.CharField(max_length=300)
    state = models.CharField(max_length=300)
    city = models.CharField(max_length=300)
    address = models.CharField(max_length=3000)
    gender = models.CharField(max_length=300)
