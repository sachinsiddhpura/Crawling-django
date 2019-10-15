import unittest
from django.urls import reverse
from django.test import Client
from .models import MainProject
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.contrib.contenttypes.models import ContentType


def create_django_contrib_auth_models_user(**kwargs):
    defaults = {}
    defaults["username"] = "username"
    defaults["email"] = "username@tempurl.com"
    defaults.update(**kwargs)
    return User.objects.create(**defaults)


def create_django_contrib_auth_models_group(**kwargs):
    defaults = {}
    defaults["name"] = "group"
    defaults.update(**kwargs)
    return Group.objects.create(**defaults)


def create_django_contrib_contenttypes_models_contenttype(**kwargs):
    defaults = {}
    defaults.update(**kwargs)
    return ContentType.objects.create(**defaults)


def create_mainproject(**kwargs):
    defaults = {}
    defaults["PROJECT_NAME"] = "PROJECT_NAME"
    defaults["HOMEPAGE"] = "HOMEPAGE"
    defaults.update(**kwargs)
    return MainProject.objects.create(**defaults)


class MainProjectViewTest(unittest.TestCase):
    '''
    Tests for MainProject
    '''
    def setUp(self):
        self.client = Client()

    def test_list_mainproject(self):
        url = reverse('mainapp_mainproject_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_mainproject(self):
        url = reverse('mainapp_mainproject_create')
        data = {
            "PROJECT_NAME": "PROJECT_NAME",
            "HOMEPAGE": "HOMEPAGE",
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)

    def test_detail_mainproject(self):
        mainproject = create_mainproject()
        url = reverse('mainapp_mainproject_detail', args=[mainproject.pk,])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_mainproject(self):
        mainproject = create_mainproject()
        data = {
            "PROJECT_NAME": "PROJECT_NAME",
            "HOMEPAGE": "HOMEPAGE",
        }
        url = reverse('mainapp_mainproject_update', args=[mainproject.pk,])
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)

