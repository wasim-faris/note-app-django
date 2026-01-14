from django.db import models
from django.contrib.auth.models import User
import uuid
# Create your models here.
class NoteApp(models.Model):
    notehead = models.CharField(max_length=15)
    notecontent = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    share_token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    is_public = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)
