from django.urls import path, include
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("api/", include("employees.api_urls")),
    path("register/", views.register, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),

    path("dashboard/", views.dashboard_redirect, name="dashboard_redirect"),
    path("admin-dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("employee-dashboard/", views.employee_dashboard, name="employee_dashboard"),

    path("employees/", views.employee_list, name="employee_list"),
    path("employees/add/", views.employee_create, name="employee_create"),
    path("employees/edit/<int:pk>/", views.employee_update, name="employee_update"),
    path("employees/delete/<int:pk>/", views.employee_delete, name="employee_delete"),
]
