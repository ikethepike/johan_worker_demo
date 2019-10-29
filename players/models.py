from django.db import models

# Create your models here.
class Player(models.Model):
    name = models.CharField(max_length=99)
    height = models.IntegerField(default=0)
    current_average_height = models.IntegerField(null=True)

