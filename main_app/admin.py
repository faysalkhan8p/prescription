from django.contrib import admin
from .models import Prescription, Note, Dosing

# Register your models here.
admin.site.register(Prescription)
admin.site.register(Dosing)
admin.site.register(Note)
