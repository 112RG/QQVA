from django.db import models
import uuid
class Users(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_name = models.CharField(max_length=20, null=False, default="")
    reg_date = models.TimeField(null=True)
    is_admin = models.BooleanField(default=False)

class VoiceFingerprint(models.Model):
    voice_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    id = models.ForeignKey("Users", on_delete=models.CASCADE)
    #voice_fingerprint using BinaryField but probably needs to be fixed
    voice_fingerprint = models.CharField(max_length=1000)

class Command(models.Model):
    command_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    id = models.ForeignKey("Users", on_delete=models.CASCADE, null=True)
    command_time = models.TimeField(auto_now=False, auto_now_add=True)
    command = models.CharField(max_length=20, null=False, default="")