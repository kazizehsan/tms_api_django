from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions, generics, pagination

from utils.paginators import CustomPagination
from .models import Task
from .serializers import TaskSerializer
from django.db.models import Q


class TaskListCreateView(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination

    def list(self, request, *args, **kwargs):
        """
        List all the task items created by requested user
        """
        queryset = self.get_queryset()
        queryset = queryset.filter(
            Q(created_by=request.user.id) | Q(assignee=request.user.id)
        )

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
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
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, id):
        queryset = self.get_queryset()
        instance = None
        try:
            instance = queryset.get(id=id)
            # May raise a permission denied
            self.check_object_permissions(self.request, instance)
        except Task.DoesNotExist:
            pass
        return instance

    def retrieve(self, request, id, *args, **kwargs):
        """
        Retrieves the object with given id
        """
        instance = self.get_object(id)
        if not instance:
            return Response(
                {"res": "Object with task id does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, id, *args, **kwargs):
        """
        Updates the object with given id if exists
        """
        instance = self.get_object(id)
        if not instance:
            return Response(
                {"res": "Object with task id does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )
        data = {
            "name": request.data.get("name"),
            "description": request.data.get("description"),
            "completed": request.data.get("completed"),
            "priority": request.data.get("priority"),
            "due_date": request.data.get("due_date"),
            "assignee": request.data.get("assignee"),
        }
        serializer = self.get_serializer(instance, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            if getattr(instance, "_prefetched_objects_cache", None):
                # If 'prefetch_related' has been applied to a queryset, we need to
                # forcibly invalidate the prefetch cache on the instance.
                instance._prefetched_objects_cache = {}
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, id, *args, **kwargs):
        """
        Deletes the object with given id if exists
        """
        instance = self.get_object(id)
        if not instance:
            return Response(
                {"res": "Object with task id does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
