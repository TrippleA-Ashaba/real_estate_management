from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Business(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)


class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    business = models.ForeignKey(Business, on_delete=models.CASCADE)


class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    can_login = models.BooleanField(default=False)


class ProjectStatus(models.TextChoices):
    NOTSTARTED = "not_started", "not_started"
    INPROGRESS = "in_progress", "in_progress"
    CANCELLED = "cancelled", "cancelled"
    COMPLETED = "completed", "completed"
    SOLD = "sold", "sold"


class Project(models.Model):
    business = models.ForeignKey(
        Business, related_name="projects", on_delete=models.CASCADE
    )
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    status = models.CharField(
        max_length=255, choices=ProjectStatus.choices, default=ProjectStatus.NOTSTARTED
    )


class ProjectContactPerson(models.Model):
    project = models.ForeignKey(
        Project, related_name="contact_persons", on_delete=models.CASCADE
    )
    name = models.CharField(max_length=255)
    designation = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    phone_number = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    status = models.CharField(max_length=255)


class ProjectBudget(models.Model):
    project = models.OneToOneField(
        Project, related_name="budget", on_delete=models.CASCADE
    )
    amount = models.PositiveIntegerField()


class ProjectExpense(models.Model):
    project = models.ForeignKey(
        Project, related_name="expenses", on_delete=models.CASCADE
    )
    item = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField()
    amount = models.PositiveIntegerField()


class ProjectCustomer(models.Model):
    project = models.ForeignKey(
        Project, related_name="customers", on_delete=models.CASCADE
    )
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    phone = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    nin = models.CharField(max_length=255)


class ProjectSales(models.Model):
    project = models.OneToOneField(
        Project, related_name="sales", on_delete=models.CASCADE
    )
    customer = models.OneToOneField(
        ProjectCustomer, related_name="customers", on_delete=models.CASCADE
    )
    amount = models.PositiveIntegerField()
    period = models.PositiveIntegerField()


class ProjectPayments(models.Model):
    sales = models.ForeignKey(
        ProjectSales, related_name="payments", on_delete=models.CASCADE
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    amount = models.PositiveIntegerField()
