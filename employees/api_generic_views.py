
from rest_framework import generics
from .models import Employee
from .serializers import EmployeeSerializer
from .api_permissions import IsAdminOrEmployeeReadOnly, is_admin


class EmployeeGenericListCreateView(generics.ListCreateAPIView):
    serializer_class = EmployeeSerializer
    permission_classes = [IsAdminOrEmployeeReadOnly]

    def get_queryset(self):
        user = self.request.user

        if is_admin(user):
            return Employee.objects.all().order_by("id")

        return Employee.objects.filter(user=user).order_by("id")


class EmployeeGenericDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = EmployeeSerializer
    permission_classes = [IsAdminOrEmployeeReadOnly]

    def get_queryset(self):
        user = self.request.user

        if is_admin(user):
            return Employee.objects.all()

        return Employee.objects.filter(user=user)
