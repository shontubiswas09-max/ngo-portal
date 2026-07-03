from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from ngo_portal.custom_admin import ngo_admin_site

urlpatterns = [
    path('admin/', ngo_admin_site.urls),
    path('accounts/login/', RedirectView.as_view(pattern_name='admin:login', permanent=False, query_string=True), name='login'),
    path('dashboard/', include('dashboard.urls')),
    path('projects/', include('projects.urls')),
    path('donors/', include('donors.urls')),
    path('beneficiaries/', include('beneficiaries.urls')),
    path('reports/', include('reports.urls')),
    path('lms/', include('lms.urls')),  # LMS module
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

