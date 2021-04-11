from django.shortcuts import render, redirect

from .models import Prescription, Note, Dosing

# Form import(s)
from .forms import DosingForm, NoteForm

S3_BASE_URL = 'https://s3.us-east-1.amazonaws.com/'
BUCKET = 'django-pillpal-bucket'

# CBV imports
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


def home(request):
    if request.user.is_authenticated:
        return redirect('main')
    else:
        return render(request, 'home.html')


@login_required
def main(request):
    return render(request, 'main.html')


@login_required
def prescriptions_index(request):
    prescriptions = Prescription.objects.filter(user=request.user)

    return render(request, 'prescriptions/index.html',
                  {'prescriptions': prescriptions})


@login_required
def prescriptions_detail(request, prescription_id):
    prescription = Prescription.objects.get(id=prescription_id)
    dosing_form = DosingForm()
    note_form = NoteForm()

    return render(request, 'prescriptions/detail.html',
                  {'prescription': prescription, 'dosing_form': dosing_form, 'note_form': note_form})


@login_required
def add_dosing(request, prescription_id):
    form = DosingForm(request.POST)
    if form.is_valid():
        new_dosing = form.save(commit=False)
        new_dosing.prescription_id = prescription_id
        new_dosing.save()
    return redirect('detail', prescription_id=prescription_id)


@login_required
def remove_dosing(request, prescription_id, dosing_id):
    Dosing.objects.get(id=dosing_id).delete()
    return redirect('detail', prescription_id=prescription_id)


@login_required
def add_note(request, prescription_id):
    form = NoteForm(request.POST)
    if form.is_valid():
        new_note = form.save(commit=False)
        new_note.prescription_id = prescription_id
        new_note.save()
    return redirect('detail', prescription_id=prescription_id)


@login_required
def remove_note(request, prescription_id, note_id):
    Note.objects.get(id=note_id).delete()
    return redirect('detail', prescription_id=prescription_id)


class PrescriptionCreate(LoginRequiredMixin, CreateView):
    model = Prescription
    fields = ['rx_number', 'prescription_issue_date', 'prescription_filled_date', 'times_per_day',
              'delivery', 'dosage', 'refills']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    success_url = '/prescriptions/'


class PrescriptionUpdate(LoginRequiredMixin, UpdateView):
    model = Prescription
    fields = ['rx_number', 'prescription_issue_date', 'prescription_filled_date', 'times_per_day',
              'delivery', 'dosage', 'refills']


class PrescriptionDelete(LoginRequiredMixin, DeleteView):
    model = Prescription
    success_url = '/prescriptions/'


'''
Sign up
'''


def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('main')
        else:
            error_message = 'Invalid sign up - try again.'
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)
