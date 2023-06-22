from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from .models import Task
from .serializers import TaskSerializer
from django.db.models import Q


class TaskListApiView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]

    # 1. List all
    def get(self, request, *args, **kwargs):
        """
        List all the task items created by requested user
        """
        tasks = Task.objects.filter(
            Q(created_by=request.user.id) | Q(assignee=request.user.id)
        )
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 2. Create
    def post(self, request, *args, **kwargs):
        """
        Create the task
        """
        data = {
            "name": request.data.get("name"),
            "description": request.data.get("description"),
            "due_date": request.data.get("due_date"),
            "priority": request.data.get("priority"),
            "assignee": request.data.get("assignee"),
        }
        serializer = TaskSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskDetailApiView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, id):
        """
        Helper method to get the object with given id
        """
        try:
            return Task.objects.get(id=id)
        except Task.DoesNotExist:
            return None

    # 3. Retrieve
    def get(self, request, id, *args, **kwargs):
        """
        Retrieves the object with given id
        """
        instance = self.get_object(id)
        if not instance:
            return Response(
                {"res": "Object with task id does not exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = TaskSerializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 4. Update
    def put(self, request, id, *args, **kwargs):
        """
        Updates the object with given id if exists
        """
        instance = self.get_object(id)
        if not instance:
            return Response(
                {"res": "Object with task id does not exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        data = {
            "name": request.data.get("name"),
            "description": request.data.get("description"),
            "completed": request.data.get("completed"),
            "priority": request.data.get("priority"),
            "due_date": request.data.get("due_date"),
            "assignee": request.data.get("assignee"),
        }
        serializer = TaskSerializer(instance=instance, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 5. Delete
    def delete(self, request, id, *args, **kwargs):
        """
        Deletes the object with given id if exists
        """
        instance = self.get_object(id)
        if not instance:
            return Response(
                {"res": "Object with task id does not exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        instance.delete()
        return Response({"res": "Object deleted!"}, status=status.HTTP_200_OK)
