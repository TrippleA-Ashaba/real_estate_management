from django.urls import path

from .views import (
    add_contact_person,
    add_project,
    business_detail,
    businesses,
    edit_budget,
    project_detail,
    projects,
    add_expense,
    project_edit,
    project_delete,
    expense_edit,
    expense_delete,
)

urlpatterns = [
    path("", projects, name="projects"),
    path("businesses/", businesses, name="businesses"),
    path("business_detail/<int:id>/", business_detail, name="business_detail"),
    path("add_project/<int:id>/", add_project, name="add_project"),
    path("project_edit/<int:id>/", project_edit, name="project_edit"),
    path("project_delete/<int:id>/", project_delete, name="project_delete"),
    path("project_detail/<int:id>/", project_detail, name="project_detail"),
    path("edit_budget/<int:id>/", edit_budget, name="edit_budget"),
    path("add_contact_person/<int:id>/", add_contact_person, name="add_contact_person"),
    path("add_expense/<int:id>/", add_expense, name="add_expense"),
    path("expense_edit/<int:id>/", expense_edit, name="expense_edit"),
    path("expense_delete/<int:id>/", expense_delete, name="expense_delete"),
]
