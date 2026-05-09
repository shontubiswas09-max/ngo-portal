from django.contrib.admin import AdminSite
from django.urls import reverse
from django.http import HttpResponse
from django.template.response import TemplateResponse

class NGOAdminSite(AdminSite):
    site_header = "Inclusive Learning Hub Administration"
    site_title = "Inclusive Learning Hub Admin"
    index_title = "Welcome to the Inclusive Learning Hub Dashboard"

    def index(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['dashboard_url'] = reverse('dashboard:index')
        return super().index(request, extra_context)

ngo_admin_site = NGOAdminSite(name='ngo_admin')