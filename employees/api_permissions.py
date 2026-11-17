
from rest_framework.permissions import BasePermission, SAFE_METHODS


def is_admin(user):
    return (
        user.is_authenticated
        and (
            user.is_superuser
            or user.groups.filter(name="Admin").exists()
        )
    )


def is_employee(user):
    return (
        user.is_authenticated
        and user.groups.filter(name="Employee").exists()
    )


class IsAdminOrEmployeeReadOnly(BasePermission):
    """
    Admin: Full access.
    Employee: Read-only access.
    """

    def has_permission(self, request, view):
        user = request.user

        if not user or not user.is_authenticated:
            return False

        if is_admin(user):
            return True

        return is_employee(user) and request.method in SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        user = request.user

        if is_admin(user):
            return True

        return (
            is_employee(user)
            and request.method in SAFE_METHODS
            and getattr(obj, "user_id", None) == user.id
        )
