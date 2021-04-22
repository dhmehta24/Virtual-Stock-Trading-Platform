from django.db import models
from django.contrib.auth.models import User


class Investor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = [
        ('Male','Male'),
        ('Female','Female')
    ]
    phone = models.IntegerField()
    gender = models.CharField(choices=gender,max_length=25)
    dob = models.DateField()

    def __str__(self):
        return (User.first_name + " " + User.last_name)

