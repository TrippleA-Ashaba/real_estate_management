from django.urls import path
from .report_views import gen_project_expense_report

from .views import (
    add_contact_person,
    add_expense,
    add_project,
    business_detail,
    businesses,
    edit_budget,
    expense_delete,
    expense_edit,
    expenses,
    project_customer_add,
    project_delete,
    project_detail,
    project_edit,
    project_sale,
    project_sale_detail,
    projects,
    search_project,
    select_property_status,
    navbar_search,
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
    path("expenses", expenses, name="expenses"),
    path(
        "project_sale_detail/<int:id>/", project_sale_detail, name="project_sale_detail"
    ),
    path(
        "project_customer_add/<int:id>/",
        project_customer_add,
        name="project_customer_add",
    ),
    path("project_sale/<int:id>/", project_sale, name="project_sale"),
    path("report/<int:id>/", gen_project_expense_report, name="report"),
    path("search_project/", search_project, name="search_project"),
    path(
        "select_property_status/", select_property_status, name="select_property_status"
    ),
    path("navbar_search/", navbar_search, name="navbar_search"),
]
