from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import F, Sum, Q
from django.shortcuts import get_object_or_404, redirect, render

from apps.accounts.forms import SignUpForm

from .forms import (
    BusinessCreationForm,
    ProjectBudgetForm,
    ProjectContactPersonForm,
    ProjectCreationForm,
    ProjectCustomerForm,
    ProjectExpenseForm,
    ProjectSalesForm,
)
from .models import (
    Business,
    BusinessAdmin,
    Project,
    ProjectBudget,
    ProjectContactPerson,
    ProjectCustomer,
    ProjectExpense,
    ProjectStatus,
)


def is_system_admin(user):
    return user.is_superuser


def not_system_admin(user):
    return not user.is_superuser


# Create your views here.
# def dashboard(request):
#     business = Business.objects.get(admin__user=request.user)
#     context = {"business": business}
#     return render(request, "core/dashboard.html", context)


@login_required
@user_passes_test(is_system_admin)
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


@login_required
@user_passes_test(is_system_admin)
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


@login_required
@user_passes_test(not_system_admin)
def projects(request):
    user = request.user
    try:
        business = Business.objects.get(admin__user=user)
    except Business.DoesNotExist:
        pass

    if business:
        projects = Project.objects.filter(business=business)
        project_count = projects.count()

    total_expenses_business = (
        ProjectExpense.objects.filter(project__business=business)
        .annotate(total_expense=F("quantity") * F("unit_price"))
        .aggregate(total=Sum("total_expense"))["total"]
    )

    print(business)
    form = ProjectCreationForm()
    context = {
        "form": form,
        "projects": projects,
        "business": business,
        "project_count": project_count,
        "total_expenses_business": total_expenses_business,
        "ProjectStatus": ProjectStatus,
    }
    return render(request, "core/projects.html", context)


@login_required
@user_passes_test(not_system_admin)
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


@login_required
@user_passes_test(not_system_admin)
def project_delete(request, id):
    if request.method == "POST":
        project = Project.objects.get(id=id)
        project.delete()
        return redirect("projects")


@login_required
@user_passes_test(not_system_admin)
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


@login_required
@user_passes_test(not_system_admin)
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

    total_expenses_project = (
        ProjectExpense.objects.filter(project=project)
        .annotate(total_expense=F("quantity") * F("unit_price"))
        .aggregate(total=Sum("total_expense"))["total"]
    )
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
        "total_expenses": total_expenses_project,
    }
    return render(request, "core/project_detail.html", context)


@login_required
@user_passes_test(not_system_admin)
def edit_budget(request, id):
    project = get_object_or_404(Project, id=id)
    budget, created = ProjectBudget.objects.get_or_create(project=project)
    if request.method == "POST":
        form = ProjectBudgetForm(request.POST, instance=project.budget)
        if form.is_valid():
            print("*" * 50)
            form.save()
            return redirect("project_detail", id=project.id)


@login_required
@user_passes_test(not_system_admin)
def add_contact_person(request, id):
    project = get_object_or_404(Project, id=id)
    if request.method == "POST":
        form = ProjectContactPersonForm(request.POST)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.project = project
            contact.save()
            return redirect("project_detail", id=project.id)


@login_required
@user_passes_test(not_system_admin)
def add_expense(request, id):
    project = get_object_or_404(Project, id=id)
    if request.method == "POST":
        form = ProjectExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.project = project
            expense.save()
            return redirect("project_detail", id=project.id)


@login_required
@user_passes_test(not_system_admin)
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


@login_required
@user_passes_test(not_system_admin)
def expense_delete(request, id):
    if request.method == "POST":
        expense = ProjectExpense.objects.get(id=id)
        project = Project.objects.get(id=expense.project.id)
        expense.delete()
        return redirect("project_detail", id=project.id)


@login_required
@user_passes_test(not_system_admin)
def expenses(request):
    business = get_object_or_404(Business, admin__user=request.user)
    expenses = ProjectExpense.objects.filter(project__business=business)

    context = {"expenses": expenses}
    return render(request, "core/expenses.html", context)


@login_required
@user_passes_test(not_system_admin)
def project_sale_detail(request, id):
    project = get_object_or_404(Project, id=id)

    try:
        customer = project.customer
    except Project.customer.RelatedObjectDoesNotExist:
        customer = None
    try:
        sales = project.sales
    except Project.sales.RelatedObjectDoesNotExist:
        sales = None

    total_expenses_project = (
        ProjectExpense.objects.filter(project=project)
        .annotate(total_expense=F("quantity") * F("unit_price"))
        .aggregate(total=Sum("total_expense"))["total"]
    )

    customer_form = ProjectCustomerForm(instance=customer)
    sales_form = ProjectSalesForm()

    context = {
        "project": project,
        "customer_form": customer_form,
        "sales_form": sales_form,
        "customer": customer,
        "sales": sales,
        "total_expenses_project": total_expenses_project,
    }
    return render(request, "core/project_sale.html", context)


@login_required
@user_passes_test(not_system_admin)
def project_customer_add(request, id):
    if request.method == "POST":
        project = get_object_or_404(Project, id=id)
        form = ProjectCustomerForm(request.POST)
        if form.is_valid():
            customer, created = ProjectCustomer.objects.get_or_create(
                project=project, defaults=form.cleaned_data
            )
            if not created:
                for field, value in form.cleaned_data.items():
                    setattr(customer, field, value)
                customer.save()
            return redirect("project_sale_detail", id=id)


@login_required
@user_passes_test(not_system_admin)
def project_sale(request, id):
    if request.method == "POST":
        form = ProjectSalesForm(request.POST)
        project = get_object_or_404(Project, id=id)
        if form.is_valid():
            sale = form.save(commit=False)
            sale.project = project
            sale.customer = project.customer
            sale.save()
            project.status = "sold"
            project.save()
            return redirect("project_sale_detail", id=id)


def search_project(request):
    business = get_object_or_404(Business, admin__user=request.user)
    search = request.GET.get("projects_search")
    projects = Project.objects.filter(business=business)
    if search:
        projects = projects.filter(
            Q(name__icontains=search)
            | Q(description__icontains=search)
            | Q(location__icontains=search)
            | Q(status__icontains=search)
        )
    print(search)
    context = {"search": search, "projects": projects}
    return render(request, "core/partials/projects_table.html", context)


def select_property_status(request):
    projects = Project.objects.filter(business__admin__user=request.user)
    status = request.GET.get("status")
    print(status)
    if status:
        projects = projects.filter(status=status)
    context = {"projects": projects}
    return render(request, "core/partials/projects_table.html", context)
