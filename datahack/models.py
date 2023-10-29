from django.db import models
class FilesUpload(models.Model):
    file = models.FileField(upload_to='files/')

# Create your models here.
