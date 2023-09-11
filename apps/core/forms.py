from django import forms

from .models import Business, Project


class BusinessCreationForm(forms.ModelForm):
    class Meta:
        model = Business
        fields = "__all__"


class ProjectCreationForm(forms.ModelForm):
    class Meta:
        model = Project
        exclude = ("business",)

        widgets = {
            "start_date": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }
