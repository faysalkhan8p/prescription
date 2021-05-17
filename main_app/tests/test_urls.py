from django.test import SimpleTestCase
from django.urls import resolve, reverse
import main_app.views


class TestUrls(SimpleTestCase):
    def test_home_url_is_resolved(self):
        url = reverse('home')
        self.assertEqual(resolve(url).func, main_app.views.home)

    def test_main_url_is_resolved(self):
        url = reverse('main')
        self.assertEqual(resolve(url).func, main_app.views.main)

    def test_signup_url_is_resolved(self):
        url = reverse('signup')
        self.assertEqual(resolve(url).func, main_app.views.signup)

    def test_prescriptions_index_url_is_resolved(self):
        found = resolve('/prescriptions/')
        self.assertEqual(found.func, main_app.views.prescriptions_index)

    def test_prescriptions_detail_url_is_resolved(self):
        found = (resolve('/prescriptions/1/'))
        self.assertEqual(found.func, main_app.views.prescriptions_detail)

    def test_add_dosing_url_is_resolved(self):
        url = resolve('/prescriptions/1/add_dosing/')
        self.assertEqual(url.func, main_app.views.add_dosing)

    def test_remove_dosing_url_is_resolved(self):
        url = resolve('/prescriptions/1/remove_dosing/19/')
        self.assertEqual(url.func, main_app.views.remove_dosing)

    def test_add_note_url_is_resolved(self):
        url = resolve('/prescriptions/1/add_note/')
        self.assertEqual(url.func, main_app.views.add_note)

    def test_remove_note_url_is_resolved(self):
        url = resolve('/prescriptions/1/remove_note/4/')
        self.assertEqual(url.func, main_app.views.remove_note)
