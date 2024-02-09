from django.forms import ModelForm
from .models import TextFile, UploadFileForm
from django import forms


class UploadFileForm(forms.ModelForm):
    class Meta:
        model = UploadFileForm
        fields = ["name", "file"]



class TextFile(ModelForm):
    class Meta:
        model = TextFile
        fields = ["name", "description"]



