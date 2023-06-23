from rest_framework.views import APIView

from utils.permissions import IsRequestedUser
from django.contrib.auth.models import Group

from .models import User
from .serializers import (
    GroupSerializer,
    UserGroupUpdateRequestSerializer,
    UserSerializer,
)
from rest_framework.response import Response
from rest_framework import permissions, status


# view for registering users
class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class UserDetailView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAdminUser | IsRequestedUser]

    def get_object(self, id):
        instance = None
        try:
            instance = User.objects.select_related().get(id=id)
            self.check_object_permissions(self.request, instance)
        except User.DoesNotExist:
            pass
        return instance

    # Retrieve
    def get(self, request, id, *args, **kwargs):
        instance = self.get_object(id)
        if not instance:
            return Response(
                {"res": "Object with task id does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = UserSerializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Update
    def put(self, request, id, *args, **kwargs):
        # exclusive for admins
        is_admin_user = bool(request.user and request.user.is_staff)
        if not is_admin_user:
            self.permission_denied(
                request,
            )

        instance = self.get_object(id)
        if not instance:
            return Response(
                {"res": "Object with task id does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )

        request_serializer = UserGroupUpdateRequestSerializer(data=request.data)
        if not request_serializer.is_valid():
            return Response(
                request_serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

        groups = Group.objects.filter(pk__in=request.data.get("groups"))
        instance.groups.set(groups)

        serializer = UserSerializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GroupListView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request, *args, **kwargs):
        queryset = Group.objects.all()
        serializer = GroupSerializer(queryset, many=True)
        return Response(serializer.data)
