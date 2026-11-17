
from functools import wraps

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User, Group
from django.db import transaction
from django.db.models import Q
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from .forms import EmployeeForm, EmployeeUserRegistrationForm
from .models import Employee, Department, Project



def is_admin(user):
    return user.is_authenticated and (
        user.is_superuser
        or user.groups.filter(name="Admin").exists()
    )


def is_employee(user):
    return user.is_authenticated and user.groups.filter(
        name="Employee"
    ).exists()


def admin_required(view_func):
    @wraps(view_func)
    @login_required
    def wrapper(request, *args, **kwargs):
        if not is_admin(request.user):
            return HttpResponseForbidden(
                "403 Forbidden - Admin access only."
            )

        return view_func(request, *args, **kwargs)

    return wrapper



def home(request):
    if request.user.is_authenticated:
        return redirect("dashboard_redirect")

    return render(request, "employees/home.html")


@login_required
def dashboard_redirect(request):
    if is_admin(request.user):
        return redirect("admin_dashboard")

    elif is_employee(request.user):
        return redirect("employee_dashboard")

    else:
        logout(request)
        messages.error(
            request,
            "Your account does not have an assigned role."
        )
        return redirect("login")



def register(request):
    if request.user.is_authenticated:
        return redirect("dashboard_redirect")

    if request.method == "POST":
        form = EmployeeUserRegistrationForm(request.POST)

        if form.is_valid():
            with transaction.atomic():

                user = User.objects.create_user(
                    username=form.cleaned_data["username"],
                    email=form.cleaned_data["email"],
                    password=form.cleaned_data["password"]
                )

                employee = Employee.objects.get(
                    employee_id=form.cleaned_data["employee_id"],
                    user__isnull=True
                )

                employee.user = user
                employee.save()

                employee_group, created = Group.objects.get_or_create(
                    name="Employee"
                )

                user.groups.add(employee_group)

            messages.success(
                request,
                "Registration successful! You can now log in."
            )

            return redirect("login")

    else:
        form = EmployeeUserRegistrationForm()

    return render(
        request,
        "employees/register.html",
        {"form": form}
    )


def login_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard_redirect")

    if request.method == "POST":
        form = AuthenticationForm(
            request,
            data=request.POST
        )

        if form.is_valid():
            user = form.get_user()
            login(request, user)

            messages.success(
                request,
                "Login successful!"
            )

            return redirect("dashboard_redirect")

    else:
        form = AuthenticationForm(request)

    return render(
        request,
        "employees/login.html",
        {"form": form}
    )



@login_required
@require_POST
def logout_view(request):
    logout(request)

    messages.success(
        request,
        "You have logged out successfully."
    )

    return redirect("login")



@admin_required
def admin_dashboard(request):

    context = {
        "employee_count": Employee.objects.count(),
        "department_count": Department.objects.count(),
        "project_count": Project.objects.count(),

        "employees": Employee.objects.select_related(
            "department",
            "user"
        ).prefetch_related("projects").all(),
    }

    return render(
        request,
        "employees/admin_dashboard.html",
        context
    )



@login_required
@user_passes_test(is_employee)
def employee_dashboard(request):

    try:
        employee = Employee.objects.select_related(
            "department"
        ).prefetch_related(
            "projects"
        ).get(user=request.user)

    except Employee.DoesNotExist:
        return render(
            request,
            "employees/no_employee_profile.html"
        )

    return render(
        request,
        "employees/employee_dashboard.html",
        {"employee": employee}
    )


@admin_required
def employee_list(request):

    employees = Employee.objects.select_related(
        "department",
        "user"
    ).prefetch_related("projects")

    search_query = request.GET.get(
        "search",
        ""
    ).strip()

    department_id = request.GET.get(
        "department",
        ""
    )

    if search_query:
        employees = employees.filter(
            Q(name__icontains=search_query)
            | Q(employee_id__icontains=search_query)
            | Q(email__icontains=search_query)
            | Q(job_role__icontains=search_query)
        )

    if department_id:
        employees = employees.filter(
            department_id=department_id
        )

    departments = Department.objects.all()

    context = {
        "employees": employees,
        "departments": departments,
        "search_query": search_query,
        "selected_department": department_id,
    }

    return render(
        request,
        "employees/employee_list.html",
        context
    )


@admin_required
def employee_create(request):

    if request.method == "POST":

        form = EmployeeForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Employee added successfully!"
            )

            return redirect("employee_list")

        messages.error(
            request,
            "Please correct the errors below."
        )

    else:
        form = EmployeeForm()

    return render(
        request,
        "employees/employee_form.html",
        {
            "form": form,
            "title": "Add Employee"
        }
    )


@admin_required
def employee_update(request, pk):

    employee = get_object_or_404(
        Employee,
        pk=pk
    )

    if request.method == "POST":

        form = EmployeeForm(
            request.POST,
            instance=employee
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Employee updated successfully!"
            )

            return redirect("employee_list")

        messages.error(
            request,
            "Please correct the errors below."
        )

    else:
        form = EmployeeForm(instance=employee)

    return render(
        request,
        "employees/employee_form.html",
        {
            "form": form,
            "title": "Edit Employee"
        }
    )



@admin_required
@require_POST
def employee_delete(request, pk):

    employee = get_object_or_404(
        Employee,
        pk=pk
    )

    employee.delete()

    messages.success(
        request,
        "Employee deleted successfully!"
    )

    return redirect("employee_list")
