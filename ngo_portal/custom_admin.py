from django.contrib.admin import AdminSite

class NGOAdminSite(AdminSite):
    site_header = "Inclusive Learning Hub Administration"
    site_title = "Inclusive Learning Hub Admin"
    index_title = "Welcome to the Inclusive Learning Hub Dashboard"

ngo_admin_site = NGOAdminSite(name='ngo_admin')