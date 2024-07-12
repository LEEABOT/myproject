import uuid

from django.db import models

# Create your models here.


class userInfo(models.Model):
    user_id=models.CharField(primary_key=True,max_length=20)
    user_name=models.CharField(max_length=20)
    user_password=models.CharField(max_length=20)

class Food(models.Model):
    foodname = models.CharField(max_length=255)
    picsrc = models.CharField(max_length=255)
    foodmaterial = models.TextField()
    foodstep = models.TextField()
    class Meta:
        db_table = 'foods'

    def __str__(self):
        return self.foodname
