from django.db import models

# Create your models here.

class Users(models.Model):
    user = models.CharField(max_length=200)

#this is for testing purposes...

    def __str__(self):
        return self.user

class Name(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    complete = models.BooleanField()

    def __str__(self):
        return self.text