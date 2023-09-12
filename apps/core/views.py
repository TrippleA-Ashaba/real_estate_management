from django.shortcuts import get_object_or_404, redirect, render

from apps.accounts.forms import SignUpForm

from .forms import (
    BusinessCreationForm,
    ProjectBudgetForm,
    ProjectContactPersonForm,
    ProjectCreationForm,
    ProjectExpenseForm,
)
from .models import (
    Business,
    BusinessAdmin,
    Project,
    ProjectBudget,
    ProjectContactPerson,
    ProjectExpense,
)

# Create your views here.
# def dashboard(request):
#     business = Business.objects.get(admin__user=request.user)
#     context = {"business": business}
#     return render(request, "core/dashboard.html", context)


def businesses(request):
    businesses = Business.objects.all().order_by("-created_at")
    form = BusinessCreationForm()

    if request.method == "POST":
        form = BusinessCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("businesses")
    context = {"form": form, "businesses": businesses}
    return render(request, "core/businesses.html", context)


def business_detail(request, id):
    business = get_object_or_404(Business, id=id)
    admin = None
    try:
        admin = BusinessAdmin.objects.get(business=business)
    except BusinessAdmin.DoesNotExist:
        pass

    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            admin = BusinessAdmin.objects.create(user=user, business=business)
            admin.save()
            return redirect("business_detail", id=business.id)
    context = {"business": business, "form": form, "admin": admin}
    return render(request, "core/business_detail.html", context)


def projects(request):
    user = request.user
    try:
        business = Business.objects.get(admin__user=user)
    except Business.DoesNotExist:
        pass

    if business:
        projects = Project.objects.filter(business=business)

    print(business)
    form = ProjectCreationForm()
    context = {"form": form, "projects": projects, "business": business}
    return render(request, "core/projects.html", context)


def project_edit(request, id):
    project = get_object_or_404(Project, id=id)
    form = ProjectCreationForm(instance=project)
    if request.method == "POST":
        form = ProjectCreationForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect("projects")
    context = {"form": form, "project": project}
    return render(request, "core/project_edit.html", context)


def project_delete(request, id):
    if request.method == "POST":
        project = Project.objects.get(id=id)
        project.delete()
        return redirect("projects")


def add_project(request, id):
    business = get_object_or_404(Business, id=id)
    if request.method == "POST":
        form = ProjectCreationForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            project = form.save(commit=False)
            project.business = business
            project.save()

    return redirect("projects")


def project_detail(request, id):
    project = get_object_or_404(Project, id=id)
    try:
        budget = ProjectBudget.objects.get(project=project)
    except ProjectBudget.DoesNotExist:
        budget = None

    if project:
        contact_persons = ProjectContactPerson.objects.filter(project=project)
    else:
        contact_persons = None

    try:
        expenses = ProjectExpense.objects.filter(project=project).order_by(
            "-created_at"
        )
    except ProjectExpense.DoesNotExist:
        expenses = None

    print(budget)
    print(project)
    budget_form = ProjectBudgetForm(instance=budget)
    contact_person_form = ProjectContactPersonForm()
    expense_form = ProjectExpenseForm()

    context = {
        "project": project,
        "budget_form": budget_form,
        "budget": budget,
        "expenses": expenses,
        "contact_persons": contact_persons,
        "contact_person_form": contact_person_form,
        "expense_form": expense_form,
    }
    return render(request, "core/project_detail.html", context)


def edit_budget(request, id):
    project = get_object_or_404(Project, id=id)
    budget, created = ProjectBudget.objects.get_or_create(project=project)
    if request.method == "POST":
        form = ProjectBudgetForm(request.POST, instance=project.budget)
        if form.is_valid():
            print("*" * 50)
            form.save()
            return redirect("project_detail", id=project.id)


def add_contact_person(request, id):
    project = get_object_or_404(Project, id=id)
    if request.method == "POST":
        form = ProjectContactPersonForm(request.POST)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.project = project
            contact.save()
            return redirect("project_detail", id=project.id)


def add_expense(request, id):
    project = get_object_or_404(Project, id=id)
    if request.method == "POST":
        form = ProjectExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.project = project
            expense.save()
            return redirect("project_detail", id=project.id)


def expense_edit(request, id):
    expense = get_object_or_404(ProjectExpense, id=id)
    project = get_object_or_404(Project, id=expense.project.id)
    form = ProjectExpenseForm(instance=expense)
    if request.method == "POST":
        form = ProjectExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            return redirect("project_detail", id=expense.project.id)
    context = {"form": form, "expense": expense, "project": project}
    return render(request, "core/expense_edit.html", context)


def expense_delete(request, id):
    if request.method == "POST":
        expense = ProjectExpense.objects.get(id=id)
        project = Project.objects.get(id=expense.project.id)
        expense.delete()
        return redirect("project_detail", id=project.id)
