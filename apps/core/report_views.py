import io
from django.http import FileResponse, HttpResponse
from reportlab.pdfgen import canvas
from .models import ProjectExpense, Project
from reportlab.lib.pagesizes import letter


def gen_project_expense_report(request, id):
    expenses = ProjectExpense.objects.filter(project__id=id)

    project_name = expenses[0].project.name if expenses else ""

    c = canvas.Canvas("expense_report.pdf", pagesize=letter)
    width, height = letter

    # Set up the header
    c.setFont("Helvetica-Bold", 14)
    c.drawString(30, height - 30, f"Expense Report for Project {project_name}")

    c.setFont("Helvetica-Bold", 12)
    headers = ["Item", "Description", "Quantity", "Unit Price", "Cost", "Supplier"]
    x_offset = 30  # Starting position of the table
    y_offset = height - 100  # Rows will be drawn at this height and below

    for i, header in enumerate(headers):
        c.drawString(x_offset + (i * 100), y_offset, header)

    # Draw the rows
    c.setFont("Helvetica", 10)
    for expense in expenses:
        y_offset -= 20  # Move to the next row
        row_data = [
            expense.item[:20],
            expense.description[:10],
            str(expense.quantity),
            str(expense.unit_price),
            str(format(expense.total, ",")),
            expense.supplier[:10],
        ]
        for i, data in enumerate(row_data):
            c.drawString(x_offset + (i * 100), y_offset, data)

    c.showPage()
    c.save()

    response = FileResponse(
        open("expense_report.pdf", "rb"), content_type="application/pdf"
    )

    # Set the Content-Disposition header to make the browser download the file
    response["Content-Disposition"] = f"attachment; filename=expense_report_{id}.pdf"

    return response
