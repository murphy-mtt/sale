from django import forms
from .models import SaleData
from django.forms import ModelForm, Textarea, TextInput, DateInput


class UploadFileForm(ModelForm):
    class Meta:
        model = SaleData
        fields = ['template_file']
        widgets = {
            'template_file': forms.ClearableFileInput(attrs={'multiple': True})
        }
