
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .api_permissions import IsAdminOrEmployeeReadOnly
from .models import Employee
from .serializers import EmployeeSerializer


class EmployeeAPIView(APIView):
    permission_classes = [IsAdminOrEmployeeReadOnly]
    # GET all employees
    def get(self, request, pk=None):
       if request.user.is_superuser or request.user.groups.filter(name="Admin").exists():
        queryset = Employee.objects.all()
       else:
        queryset = Employee.objects.filter(user=request.user)

       if pk is not None:
        employee = get_object_or_404(queryset, pk=pk)
        serializer = EmployeeSerializer(employee)
        return Response(serializer.data)

        serializer = EmployeeSerializer(queryset, many=True)
        return Response(serializer.data)
    # POST create employee
    def post(self, request):
        serializer = EmployeeSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    # PUT update complete employee
    def put(self, request, pk):
        employee = get_object_or_404(Employee, pk=pk)
        serializer = EmployeeSerializer(
            employee,
            data=request.data
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    # PATCH partial employee update
    def patch(self, request, pk):
        employee = get_object_or_404(Employee, pk=pk)
        serializer = EmployeeSerializer(
            employee,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    # DELETE employee
    def delete(self, request, pk):
        employee = get_object_or_404(Employee, pk=pk)
        employee.delete()

        return Response(
            status=status.HTTP_204_NO_CONTENT
        )
