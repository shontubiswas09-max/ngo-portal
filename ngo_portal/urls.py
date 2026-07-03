from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from ngo_portal.custom_admin import ngo_admin_site
from . import accounts_views

urlpatterns = [
    path('admin/', ngo_admin_site.urls),
    path('accounts/register/', accounts_views.register, name='register'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('projects/', include('projects.urls')),
    path('donors/', include('donors.urls')),
    path('beneficiaries/', include('beneficiaries.urls')),
    path('reports/', include('reports.urls')),
    path('lms/', include('lms.urls')),  # LMS module
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

