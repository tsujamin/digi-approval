from django.db import models

class UserFile(models.Model):
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to="userfiles")
    viruschecked = models.BooleanField(default=False)
