from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Business(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class BusinessAdmin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    business = models.OneToOneField(
        Business, on_delete=models.CASCADE, related_name="admin"
    )


class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    role = models.CharField(max_length=50)
    can_login = models.BooleanField(default=False)


class ProjectStatus(models.TextChoices):
    BACKLOG = "backlog", "backlog"
    PLANNED = "planned", "planned"
    IN_PROGRESS = "in_progress", "in progress"
    PAUSED = "paused", "paused"
    CANCELED = "canceled", "canceled"
    COMPLETED = "completed", "completed"
    SOLD = "sold", "sold"


class Project(models.Model):
    business = models.ForeignKey(
        Business, related_name="projects", on_delete=models.CASCADE
    )
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    location = models.CharField(max_length=255)
    status = models.CharField(
        max_length=255, choices=ProjectStatus.choices, default=ProjectStatus.BACKLOG
    )
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class ProjectContactPerson(models.Model):
    project = models.ForeignKey(
        Project, related_name="contact_persons", on_delete=models.CASCADE
    )
    name = models.CharField(max_length=50)
    designation = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    phone_number = models.CharField(max_length=50)
    address = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name


class ProjectBudget(models.Model):
    project = models.OneToOneField(
        Project, related_name="budget", on_delete=models.CASCADE
    )
    amount = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.amount}"


class ProjectExpense(models.Model):
    project = models.ForeignKey(
        Project, related_name="expenses", on_delete=models.CASCADE
    )
    item = models.CharField(max_length=50)
    description = models.CharField(max_length=50)
    quantity = models.PositiveIntegerField()
    unit_price = models.PositiveIntegerField()
    supplier = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)


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
    settled = models.BooleanField(default=False)


class ProjectPayments(models.Model):
    sales = models.ForeignKey(
        ProjectSales, related_name="payments", on_delete=models.CASCADE
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    amount = models.PositiveIntegerField()
