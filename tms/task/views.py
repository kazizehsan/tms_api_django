from rest_framework.response import Response
from rest_framework import status, permissions, generics, filters
from django_filters.rest_framework import DjangoFilterBackend

from utils.paginators import CustomPagination
from .models import Task
from .serializers import TaskSerializer


class TaskListCreateView(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.DjangoModelPermissions]
    pagination_class = CustomPagination
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["assignee", "completed", "due_date", "priority"]
    search_fields = ["name", "description"]
    ordering_fields = ["due_date", "priority"]

    def list(self, request, *args, **kwargs):
        requestSerializer = self.get_serializer(
            data=self.request.query_params, partial=True
        )
        if not requestSerializer.is_valid():
            return Response(
                requestSerializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.DjangoModelPermissions]

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

        serializer = self.get_serializer(instance, data=request.data, partial=True)
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
