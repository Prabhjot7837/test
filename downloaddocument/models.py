from django.db import models

# Create your models here.

class Potholedata(models.Model):
    CHOICE = (("bad", "Bad"),
    ("good","Good"),
    ("danger","Dangerous"),
    ("very_bad","Deadly_bad"))
    Address = models.TextField()
    Road_condition = models.CharField(max_length=10,choices=CHOICE)
    kms_covered = models.FloatField()
    anomalies_detected = models.IntegerField()
    pothole = models.IntegerField()
    cracks = models.IntegerField()
    patches = models.IntegerField()

class Pothole_density(models.Model):
    data = models.ForeignKey(Potholedata,on_delete=models.CASCADE)
    p500 = models.IntegerField()
    p1000 = models.IntegerField()
    p1500 = models.IntegerField()
    p2000 = models.IntegerField()
    p2500 = models.IntegerField()