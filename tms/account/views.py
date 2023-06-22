from rest_framework.views import APIView

from .models import User
from .serializers import UserSerializer
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
    permission_classes = [permissions.IsAuthenticated]

    # Retrieve
    def get(self, request, id, *args, **kwargs):
        """
        Retrieves the object with given id
        """
        instance = None
        try:
            instance = User.objects.select_related().get(id=id)
        except User.DoesNotExist:
            pass
        
        if not instance:
            return Response(
                {"res": "Object with task id does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = UserSerializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
