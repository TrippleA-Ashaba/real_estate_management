from django.urls import path

from .views import (
    business_detail,
    businesses,
    dashboard,
    projects,
    add_project,
    project_detail,
)

urlpatterns = [
    path("", dashboard, name="dashboard"),
    path("businesses/", businesses, name="businesses"),
    path("business_detail/<int:id>/", business_detail, name="business_detail"),
    path("projects/", projects, name="projects"),
    path("add_project/<int:id>/", add_project, name="add_project"),
    path("project_detail/<int:id>/", project_detail, name="project_detail"),
]
