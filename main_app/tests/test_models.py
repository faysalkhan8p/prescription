from django.test import TestCase
from django.contrib.auth.models import User
from ..models import Prescription, Note, Dosing
import datetime

t = datetime.date.today()


class PrescriptionTest(TestCase):
    def setUp(self):
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

    def test_prescription_created(self):
        self.assertEqual(self.prescription1.rx_number, 10)


class NoteTest(TestCase):
    def setUp(self):
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

        self.note1 = Note.objects.create(
            date=datetime.date.today(),
            content='First Note',
            prescription=self.prescription1
        )

    def test_note_created(self):
        self.assertEqual(self.note1.content, 'First Note')


class NoteTest(TestCase):

    def setUp(self):
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
            date=t,
            time=datetime.time(),
            prescription=self.prescription1)

    def test_dose_created(self):
        self.assertEqual(self.dosing1.date, t)
