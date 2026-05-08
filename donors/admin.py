from django.contrib import admin
from django.contrib import admin

#from ngo_portal.projects.admin_action import export_as_csv
from .models import Donor
admin.site.register(Donor)
# Register your models here.
