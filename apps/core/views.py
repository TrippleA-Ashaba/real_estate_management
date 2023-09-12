from django.shortcuts import get_object_or_404, redirect, render

from apps.accounts.forms import SignUpForm

from .forms import BusinessCreationForm, ProjectCreationForm
from .models import Business, BusinessAdmin, Project


# Create your views here.
def dashboard(request):
    business = Business.objects.get(admin__user=request.user)
    context = {"business": business}
    return render(request, "core/dashboard.html", context)


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
    context = {}
    return render(request, "core/project_detail.html", context)
