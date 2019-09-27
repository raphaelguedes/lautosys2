from django import forms
from .models import Arquivo

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Arquivo
        fields = ('description', 'document',)