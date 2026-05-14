from django.db import models

# Create your models here.
from django.db.models import CASCADE


class ClientRegister_Model(models.Model):

    username = models.CharField(max_length=30)
    email = models.EmailField(max_length=30)
    password = models.CharField(max_length=10)
    phoneno = models.CharField(max_length=10)
    country = models.CharField(max_length=30)
    state = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    gender = models.CharField(max_length=30)
    address = models.CharField(max_length=30)


class predict_cyber_attack(models.Model):

    Fid= models.CharField(max_length=300)
    Timestamp= models.CharField(max_length=300)
    Source_IP_Address= models.CharField(max_length=300)
    Destination_IP_Address= models.CharField(max_length=300)
    Source_Port= models.CharField(max_length=300)
    Destination_Port= models.CharField(max_length=300)
    Protocol= models.CharField(max_length=300)
    Packet_Length= models.CharField(max_length=300)
    Packet_Type= models.CharField(max_length=300)
    Traffic_Type= models.CharField(max_length=300)
    Alerts_Warnings= models.CharField(max_length=300)
    Action_Taken= models.CharField(max_length=300)
    Severity_Level= models.CharField(max_length=300)
    Device_Information= models.CharField(max_length=300)
    Network_Segment= models.CharField(max_length=300)
    Geolocation_Data= models.CharField(max_length=300)
    ProxyInformation= models.CharField(max_length=300)
    FirewallLogs= models.CharField(max_length=300)
    IDS_IPS_Alerts= models.CharField(max_length=300)
    Log_Source= models.CharField(max_length=300)
    Prediction= models.CharField(max_length=300)

class detection_accuracy(models.Model):

    names = models.CharField(max_length=300)
    ratio = models.CharField(max_length=300)

class detection_ratio(models.Model):

    names = models.CharField(max_length=300)
    ratio = models.CharField(max_length=300)



