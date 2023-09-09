from django import forms
from .models import Business


class BusinessCreationForm(forms.ModelForm):
    class Meta:
        model = Business
        fields = "__all__"
