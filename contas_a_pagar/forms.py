from django import forms
from .models import Conta

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Conta
        fields = ('document',)