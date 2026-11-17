
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .models import Employee


class EmployeeUserRegistrationForm(forms.Form):
    username = forms.CharField(max_length=150)
    email = forms.EmailField()
    password = forms.CharField(
        widget=forms.PasswordInput,
        validators=[validate_password]
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput
    )

    employee_id = forms.CharField(max_length=20)

    def clean_username(self):
        username = self.cleaned_data["username"]

        if User.objects.filter(username=username).exists():
            raise ValidationError("Username already exists.")

        return username

    def clean_email(self):
        email = self.cleaned_data["email"]

        if User.objects.filter(email=email).exists():
            raise ValidationError("Email already registered.")

        return email

    def clean_employee_id(self):
        employee_id = self.cleaned_data["employee_id"]

        if not Employee.objects.filter(
            employee_id=employee_id,
            user__isnull=True
        ).exists():
            raise ValidationError(
                "Invalid employee ID or account already linked."
            )

        return employee_id

    def clean(self):
        cleaned_data = super().clean()

        if cleaned_data.get("password") != cleaned_data.get("confirm_password"):
            self.add_error("confirm_password", "Passwords do not match.")

        return cleaned_data

from .models import Department, Project


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = [
            "employee_id",
            "name",
            "email",
            "phone",
            "department",
            "job_role",
            "date_of_joining",
            "projects",
        ]

        widgets = {
            "date_of_joining": forms.DateInput(
                attrs={"type": "date"}
            ),
            "projects": forms.CheckboxSelectMultiple(),
        }

    def clean_employee_id(self):
        employee_id = self.cleaned_data["employee_id"]
        queryset = Employee.objects.filter(employee_id=employee_id)

        if self.instance.pk:
            queryset = queryset.exclude(pk=self.instance.pk)

        if queryset.exists():
            raise forms.ValidationError(
                "This employee ID already exists."
            )

        return employee_id

    def clean_email(self):
        email = self.cleaned_data["email"]
        queryset = Employee.objects.filter(email=email)

        if self.instance.pk:
            queryset = queryset.exclude(pk=self.instance.pk)

        if queryset.exists():
            raise forms.ValidationError(
                "This email address already exists."
            )

        return email

    def clean_phone(self):
        phone = self.cleaned_data["phone"]

        if not phone.isdigit() or len(phone) != 10:
            raise forms.ValidationError(
                "Enter a valid 10-digit phone number."
            )

        return phone
