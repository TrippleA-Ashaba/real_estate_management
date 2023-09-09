from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import BusinessCreationForm


# Create your views here.
def dashboard(request):
    return render(request, "core/dashboard.html")


def create_business(request):
    form = BusinessCreationForm()
    context = {
        "form": form,
    }
    return render(request, "core/create_business.html", context)
