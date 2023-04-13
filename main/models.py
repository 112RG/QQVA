from django.db import models

class Users(models.Model):
    id = models.UUIDField(primary_key=True, null=False)
    user_name = models.CharField(max_length=20, null=False)
    reg_date = models.TimeField()
    is_admin = models.BooleanField(default=False)
