from django.contrib import admin
from django.contrib.admin import AdminSite
from django.urls import reverse
from django.urls.exceptions import NoReverseMatch
from django.apps import apps

class NGOAdminSite(AdminSite):
    site_header = "Inclusive Learning Hub Administration"
    site_title = "Inclusive Learning Hub Admin"
    index_title = "Welcome to the Inclusive Learning Hub Dashboard"
    login_template = 'admin/login.html'

    def index(self, request, extra_context=None):
        extra_context = extra_context or {}
        try:
            extra_context['dashboard_url'] = reverse('dashboard:index')
        except NoReverseMatch:
            extra_context['dashboard_url'] = '/dashboard/'
        return super().index(request, extra_context)

ngo_admin_site = NGOAdminSite(name='admin')

# Register all models with the custom admin site
def register_models():
    # Import models and register them
    try:
        from beneficiaries.models import Beneficiary
        from donors.models import Donor
        from projects.models import Project, Donation, Notification, Publication, Recruitment
        from reports.models import Report

        class BeneficiaryAdmin(admin.ModelAdmin):
            list_display = ("name", "village", "project", "literacy_level", "attendance", "courses_completed")
            search_fields = ("name", "village")
            list_filter = ("literacy_level", "project")

        class DonorAdmin(admin.ModelAdmin):
            list_display = ('name', 'email', 'phone', 'profile_picture', 'document')

        class ProjectAdmin(admin.ModelAdmin):
            list_display = ('name', 'description', 'image')

        class DonationAdmin(admin.ModelAdmin):
            list_display = ('donor', 'project', 'amount', 'date')

        class NotificationAdmin(admin.ModelAdmin):
            list_display = ('title', 'created_at', 'is_read')

        class PublicationAdmin(admin.ModelAdmin):
            list_display = ('title', 'published_date', 'document')

        class RecruitmentAdmin(admin.ModelAdmin):
            list_display = ('job_title', 'posted_date', 'deadline', 'document')

        class ReportAdmin(admin.ModelAdmin):
            list_display = ("module_name", "report_name", "generated_on")
            search_fields = ("module_name", "report_name")

        ngo_admin_site.register(Beneficiary, BeneficiaryAdmin)
        ngo_admin_site.register(Donor, DonorAdmin)
        ngo_admin_site.register(Project, ProjectAdmin)
        ngo_admin_site.register(Donation, DonationAdmin)
        ngo_admin_site.register(Notification, NotificationAdmin)
        ngo_admin_site.register(Publication, PublicationAdmin)
        ngo_admin_site.register(Recruitment, RecruitmentAdmin)
        ngo_admin_site.register(Report, ReportAdmin)

    except ImportError:
        # Models not ready yet, will be registered later
        pass

# Try to register models immediately
register_models()

