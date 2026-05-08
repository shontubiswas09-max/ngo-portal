from django.contrib import admin
from .models import Project, Donor, Donation, Notification, Publication, Recruitment
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'image')


@admin.register(Donor)
class DonorAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'profile_picture', 'document')


@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ('donor', 'project', 'amount', 'date')


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'is_read')


@admin.register(Publication)
class PublicationAdmin(admin.ModelAdmin):
    list_display = ('title', 'published_date', 'document')


@admin.register(Recruitment)
class RecruitmentAdmin(admin.ModelAdmin):
    list_display = ('job_title', 'posted_date', 'deadline', 'document')

# projects/admin.py



admin.site.site_header = "Inclusive Learning Hub Administration"
admin.site.site_title = "Inclusive Learning Hub Admin"
admin.site.index_title = "Welcome to the Inclusive Learning Hub Dashboard"