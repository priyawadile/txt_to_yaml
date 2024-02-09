from django.db import models

class UploadFileForm(models.Model):
    name = models.CharField(max_length=255)
    file = models.FileField(max_length=255)


class TextFile(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name
    
