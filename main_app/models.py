from django.db import models
from django.urls import reverse
from datetime import date, datetime
from pytz import timezone

from django.contrib.auth.models import User


# Create your models here.
class Prescription(models.Model):
    rx_number = models.IntegerField()
    prescription_issue_date = models.DateField()
    times_per_day = models.IntegerField()
    medicine = models.CharField(max_length=100)
    condition = models.CharField(max_length=100)
    revisit = models.IntegerField()
    tests = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('detail', kwargs={'prescription_id': self.id})

    def taken_today(self):
        return self.dosing_set.filter(date=date.today()).count() >= self.times_per_day

    def times_taken(self):
        # Convert date to Pacific time.
        format = "%Y-%m-%d"
        now_utc = datetime.now(timezone('UTC'))
        now_wc = now_utc.astimezone(timezone('US/Pacific'))

        return self.times_per_day - self.dosing_set.filter(date=now_wc.strftime(format)).count()


class Dosing(models.Model):
    date = models.DateField('Administration Date')
    time = models.TimeField()

    prescription = models.ForeignKey(Prescription, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.date} at {self.time}"

    class Meta:
        ordering = ['-date']


class Note(models.Model):
    date = models.DateField('Note Date')
    content = models.CharField(max_length=250)

    prescription = models.ForeignKey(Prescription, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-date']
