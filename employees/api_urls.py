
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter
from .api_views import (
    EmployeeViewSet,
    DepartmentViewSet,
    ProjectViewSet,
    CurrentUserAPIView,
)
from .api_views import EmployeeViewSet, DepartmentViewSet
from .api_views_class import EmployeeAPIView
from .api_generic_views import (
    EmployeeGenericListCreateView,
    EmployeeGenericDetailView,
)

router = DefaultRouter()
router.register(r'employees', EmployeeViewSet, basename='employee')
router.register(r'departments', DepartmentViewSet, basename='department')
router.register(r'projects', ProjectViewSet, basename='project')
urlpatterns = [
    path(
    "auth/token/",
    obtain_auth_token,
    name="api-token-auth"
    ),
    path(
    "auth/user/",
    CurrentUserAPIView.as_view(),
    name="current-user",
    ),
    path(
        "apiview/employees/",
        EmployeeAPIView.as_view(),
        name="employee-apiview-list"
    ),
    path(
        "apiview/employees/<int:pk>/",
        EmployeeAPIView.as_view(),
        name="employee-apiview-detail"
    ),

    path(
        "generic/employees/",
        EmployeeGenericListCreateView.as_view(),
        name="employee-generic-list"
    ),
    path(
        "generic/employees/<int:pk>/",
        EmployeeGenericDetailView.as_view(),
        name="employee-generic-detail"
    ),
]

urlpatterns += router.urls
