from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Watch, WatchGroup
from decimal import Decimal
class WatchTests(TestCase):
    def setUp(self):
        # create test client and user
        self.client = Client()
        self.test_user = User.objects.create_user(
            username='watchfan',
            password='pass1234'
        )
        # make a test watch
        self.test_watch = Watch.objects.create(
            name='Speedmaster',
            brand='Omega',
            price=Decimal('4999.99'),
            retail_price=Decimal('5999.99'),
            description='Moon watch test'
        )
    def test_watch_list(self):
        # check if watch list page works
        response = self.client.get(reverse('watch_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/watch_list.html')
        self.assertContains(response, self.test_watch.name)
    def test_watch_detail(self):
        # check if watch detail page works
        response = self.client.get(reverse('watch_detail', args=[self.test_watch.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/watch_detail.html')
        self.assertContains(response, self.test_watch.name)
class GroupTests(TestCase):
    def setUp(self):
        # create test client and user
        self.client = Client()
        self.test_user = User.objects.create_user(
            username='groupadmin',
            password='pass1234'
        )
        # make a test group
        self.test_group = WatchGroup.objects.create(
            name='Omega Fans',
            description='For fans of Omega watches',
            admin=self.test_user
        )
    def test_group_creation(self):
        # log in and try to make a new group
        self.client.login(username='groupadmin', password='pass1234')
        response = self.client.post(reverse('group_create'), {
            'name': 'Rolex Club',
            'description': 'Discussion about Rolex'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(WatchGroup.objects.filter(name='Rolex Club').exists())