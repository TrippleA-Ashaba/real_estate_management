from django.contrib import admin

from .models import (
    Business,
    BusinessAdmin,
    Project,
    ProjectBudget,
    ProjectContactPerson,
    ProjectCustomer,
    ProjectExpense,
    ProjectPayments,
    ProjectSales,
    Staff,
)

admin.site.register(Business)
admin.site.register(Project)
admin.site.register(ProjectBudget)
admin.site.register(ProjectContactPerson)
admin.site.register(ProjectCustomer)
admin.site.register(ProjectExpense)
admin.site.register(ProjectPayments)
admin.site.register(ProjectSales)
admin.site.register(BusinessAdmin)
admin.site.register(Staff)
