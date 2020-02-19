from django.contrib import admin
from .models import Allergy, Diagnosis, Lab, Medication, Microlab, Stay

# Register your models here.
admin.site.register(Allergy)
admin.site.register(Diagnosis)
admin.site.register(Lab)
admin.site.register(Medication)
admin.site.register(Microlab)
admin.site.register(Stay)
