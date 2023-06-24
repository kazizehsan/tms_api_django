from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import Group
import urllib

from account.models import User

from .models import Task


class TaskManagerTests(APITestCase):
    def setUp(self):
        # create a user and assign group 'Manager'
        self.manager_user = User.objects.create_user(
            name="Manager User", email="manager@tms.com", password="123"
        )
        manager_group_qs = Group.objects.filter(name="Manager")
        self.manager_user.groups.set(manager_group_qs)

        # create a user and assign group 'Officer'
        self.officer_user = User.objects.create_user(
            name="Officer User", email="officer@tms.com", password="123"
        )
        officer_group_qs = Group.objects.filter(name="Officer")
        self.officer_user.groups.set(officer_group_qs)

        # create some tasks for list filtering and ordering test
        Task.objects.create(name="Task#1", priority=4, due_date="2023-06-26")
        Task.objects.create(name="Task#2", priority=3, due_date="2023-06-28")
        Task.objects.create(name="Task#3", priority=2, due_date="2023-06-28")

    def test_task_creation_by_manager(self):
        self.client.force_authenticate(user=None)
        self.client.force_authenticate(self.manager_user)

        url = "/task/"
        data = {"name": "Task#4", "priority": 1, "due_date": "2023-06-29"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # 3 tests exists from `setUp`
        self.assertEqual(Task.objects.count(), 4)
        self.assertEqual(Task.objects.get(id=response.data.get("id")).name, "Task#4")

    def test_task_creation_failure_by_officer(self):
        self.client.force_authenticate(user=None)
        self.client.force_authenticate(self.officer_user)

        url = "/task/"
        data = {"name": "Task#5"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_task_list_by_priority_desc_order(self):
        self.client.force_authenticate(user=None)
        self.client.force_authenticate(self.officer_user)

        url = "/task/"
        query_params = {"ordering": "-priority"}
        url += "?" + urllib.parse.urlencode(query_params)

        response = self.client.get(url)
        self.assertEqual(response.data.get('results')[0].get('priority'), 4)
    
    def test_task_list_by_priority_asc_order(self):
        self.client.force_authenticate(user=None)
        self.client.force_authenticate(self.officer_user)

        url = "/task/"
        query_params = {"ordering": "priority"}
        url += "?" + urllib.parse.urlencode(query_params)

        response = self.client.get(url)
        self.assertEqual(response.data.get('results')[0].get('priority'), 2)
    
    def test_task_filtering_by_due_date(self):
        self.client.force_authenticate(user=None)
        self.client.force_authenticate(self.officer_user)

        url = "/task/"
        query_params = {"due_date": "2023-06-28"}
        url += "?" + urllib.parse.urlencode(query_params)

        response = self.client.get(url)
        self.assertEqual(response.data.get('count'), 2)
