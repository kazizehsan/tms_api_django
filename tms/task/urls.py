from django.urls import path
from .views import (
    TaskRetrieveUpdateDestroyView,
    TaskListCreateView,
)

urlpatterns = [
    path("", TaskListCreateView.as_view()),
    path("<int:id>", TaskRetrieveUpdateDestroyView.as_view()),
]
