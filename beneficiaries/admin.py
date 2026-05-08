from django.contrib import admin
from django.contrib import admin

#from ngo_portal.projects.admin_action import export_as_csv
from .models import Beneficiary
admin.site.register(Beneficiary)
# Register your models here.
# from django.contrib import admin
# from .models import Beneficiary

# @admin.register(Beneficiary)
class BeneficiaryAdmin(admin.ModelAdmin):
    list_display = ("name", "village", "project", "literacy_level", "attendance", "courses_completed")
    search_fields = ("name", "village")
    list_filter = ("literacy_level", "project")