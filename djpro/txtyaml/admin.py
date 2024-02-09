from django.contrib import admin
from txtyaml.models import TextFile, UploadFileForm


# Register your models here.
admin.site.register(TextFile)
admin.site.register(UploadFileForm)