"""
Employee directory endpoints.

Product requirements (read carefully):
- GET /api/employees/
  - Optional `department`: case-insensitive exact match (iexact).
  - Optional `q`: case-insensitive substring match on name (icontains).
  - Optional `sort`: `name` or `department` (default `name`, ascending).
  - When multiple filters are provided, results must match ALL of them.
"""

from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Employee
from .serializers import EmployeeSerializer


@api_view(["GET"])
def health(request):
    return Response({"status": "ok", "challenge": "employee-directory"})


@api_view(["GET"])
def list_employees(request):
    department = (request.GET.get("department") or "").strip()
    q = (request.GET.get("q") or "").strip()
    sort = (request.GET.get("sort") or "name").strip().lower()

    qs = Employee.objects.all()

    if q:
        qs = qs.filter(name=q)

    qs = qs.order_by("id")

    return Response(EmployeeSerializer(qs, many=True).data)
