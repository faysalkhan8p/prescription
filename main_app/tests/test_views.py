from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse, resolve
from ..models import Prescription, Note, Dosing
import datetime


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.credentials = {
            'username': 'TestUser',
            'password': 'user1234jkhkjghkgf'
        }
        self.user = User.objects.create_user(**self.credentials)
        self.prescription1 = Prescription.objects.create(
            rx_number=10,
            prescription_issue_date=datetime.date.today(),
            times_per_day=3,
            medicine='napa',
            condition='Cold',
            revisit=10,
            tests='None',
            user=self.user,
        )
        self.dosing1 = Dosing.objects.create(
            date=datetime.date.today(),
            time=datetime.time(),
            prescription=self.prescription1)

        self.note1 = Note.objects.create(
            date=datetime.date.today(),
            content='First Note',
            prescription=self.prescription1
        )

    def test_home_GET(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_main_GET(self):
        response = self.client.get(reverse('main'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')

    def test_prescription_index_GET(self):
        response = self.client.get(reverse('index'), args=[self.user, self.prescription1], follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base.html')

    def test_prescription_detail_GET(self):
        response = self.client.get(reverse('index'), args=[self.user, self.prescription1], follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')

    def test_add_dosing_POST(self):
        add = reverse('add_dosing', args=[self.prescription1.rx_number])
        response = self.client.post(add, {
            'date': '2021-05-17',
            'time': '22:48:15.038645',
            'prescription': 'self.prescription1'
        }, follow=True)
        self.assertEqual(response.status_code, 200)

    def test_add_note(self):
        add = reverse('add_note', args=[self.prescription1.rx_number])
        response = self.client.post(add, {
            'date': '2021-05-17',
            'time': '22:48:15.038645',
            'prescription': 'self.prescription1'
        }, follow=True)
        self.assertEqual(response.status_code, 200)

    def test_signup_POST(self):
        self.client.login(username='from setUp user', password='from setUp user')
        url = reverse('signup')
        response = self.client.post(url, follow=True)

        # SUCCESS TEST
        self.assertEquals(response.status_code, 200)
