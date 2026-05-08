from django.db.models import Count, Sum
from projects.models import Project, Donor, Recruitment
from beneficiaries.models import Beneficiary
from lms.models import Course, Certification
from reports.models import Report


def sidebar_stats(request):
    """Context processor to provide sidebar statistics to all templates"""
    try:
        # Projects stats
        projects_count = Project.objects.count()
        donors_count = Donor.objects.count()

        # Beneficiaries stats
        beneficiaries_count = Beneficiary.objects.count()
        courses_completed = Beneficiary.objects.aggregate(
            total=Sum('courses_completed')
        )['total'] or 0

        # LMS stats
        courses_count = Course.objects.filter(is_active=True).count()
        certifications_count = Certification.objects.count()

        # Recruitment stats
        recruitments_count = Recruitment.objects.count()

        # Reports stats
        reports_count = Report.objects.count()

        # Projects completed count only if the field exists
        project_field_names = {field.name for field in Project._meta.fields}
        if 'status' in project_field_names:
            projects_completed = Project.objects.filter(status='completed').count()
        else:
            projects_completed = 0

        # Overall stats
        total_projects = projects_count
        total_beneficiaries = beneficiaries_count

        return {
            # App stats for sidebar
            'projects_count': projects_count,
            'donors_count': donors_count,
            'beneficiaries_count': beneficiaries_count,
            'courses_completed': courses_completed,
            'courses_count': courses_count,
            'certifications_count': certifications_count,
            'recruitments_count': recruitments_count,
            'reports_count': reports_count,
            'projects_completed': projects_completed,
            'total_projects': total_projects,
            'total_beneficiaries': total_beneficiaries,
        }
    except Exception as e:
        # Return default values if there's an error
        return {
            'projects_count': 0,
            'donors_count': 0,
            'beneficiaries_count': 0,
            'courses_completed': 0,
            'courses_count': 0,
            'certifications_count': 0,
            'reports_count': 0,
            'projects_completed': 0,
            'total_projects': 0,
            'total_beneficiaries': 0,
        }