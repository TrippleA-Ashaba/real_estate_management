from django import forms

from .models import (
    Business,
    Project,
    ProjectBudget,
    ProjectContactPerson,
    ProjectExpense,
    ProjectCustomer,
    ProjectSales,
)


class BusinessCreationForm(forms.ModelForm):
    class Meta:
        model = Business
        fields = "__all__"


class ProjectCreationForm(forms.ModelForm):
    class Meta:
        model = Project
        exclude = ("business",)

        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "end_date": forms.DateInput(attrs={"type": "date"}),
        }


class ProjectBudgetForm(forms.ModelForm):
    class Meta:
        model = ProjectBudget
        fields = ("amount",)


class ProjectContactPersonForm(forms.ModelForm):
    class Meta:
        model = ProjectContactPerson
        exclude = ("project",)


class ProjectExpenseForm(forms.ModelForm):
    class Meta:
        model = ProjectExpense
        exclude = ("project",)


class ProjectCustomerForm(forms.ModelForm):
    class Meta:
        model = ProjectCustomer
        exclude = ("project",)


class ProjectSalesForm(forms.ModelForm):
    class Meta:
        model = ProjectSales
        exclude = ("project", "customer")
