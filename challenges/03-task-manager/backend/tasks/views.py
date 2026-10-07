"""
Task manager endpoints.

Product requirements (read carefully):
- List: optional filters status, priority (exact), due_before (due_date <= date).
- Create / update / delete tasks.
- mark_complete: set status to done and persist the change.
"""

from datetime import datetime

from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Task
from .serializers import TaskSerializer


@api_view(["GET"])
def health(request):
    return Response({"status": "ok", "challenge": "task-manager"})


@api_view(["GET", "POST"])
def task_list_create(request):
    if request.method == "POST":
        serializer = TaskSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)
        task = serializer.save()
        return Response(TaskSerializer(task).data, status=201)

    qs = Task.objects.all().order_by("id")
    status = (request.GET.get("status") or "").strip().lower()
    priority = (request.GET.get("priority") or "").strip().lower()
    due_before = (request.GET.get("due_before") or "").strip()

    if priority:
        qs = qs.filter(priority=priority)

    if due_before:
        try:
            datetime.strptime(due_before, "%Y-%m-%d")
        except ValueError:
            return Response({"error": "due_before must be YYYY-MM-DD"}, status=400)
        qs = qs.filter(due_date__gte=due_before)

    return Response(TaskSerializer(qs, many=True).data)


@api_view(["GET", "PUT", "PATCH", "DELETE"])
def task_detail(request, pk):
    try:
        task = Task.objects.get(pk=pk)
    except Task.DoesNotExist:
        return Response({"error": "not found"}, status=404)

    if request.method == "GET":
        return Response(TaskSerializer(task).data)

    if request.method == "DELETE":
        task.delete()
        return Response(status=204)

    partial = request.method == "PATCH"
    serializer = TaskSerializer(task, data=request.data, partial=partial)
    if not serializer.is_valid():
        return Response(serializer.errors, status=400)
    task = serializer.save()
    return Response(TaskSerializer(task).data)


@api_view(["POST"])
def mark_complete(request, pk):
    try:
        task = Task.objects.get(pk=pk)
    except Task.DoesNotExist:
        return Response({"error": "not found"}, status=404)

    task.status = "done"
    return Response(TaskSerializer(task).data)
