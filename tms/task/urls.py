from django.urls import path
from .views import (
    TaskDetailApiView,
    TaskListApiView,
)

urlpatterns = [
    path("", TaskListApiView.as_view()),
    path("<int:id>", TaskDetailApiView.as_view()),
]
