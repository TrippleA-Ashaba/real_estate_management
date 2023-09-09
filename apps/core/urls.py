from django.urls import path
from .views import dashboard, create_business

urlpatterns = [
    path("", dashboard, name="dashboard"),
    path("business/create/", create_business, name="create_business"),
]
