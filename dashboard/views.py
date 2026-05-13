from django.shortcuts import render
from django.db.models import Count, Sum
from donors.models import Donor
from projects.models import Donation, Project, Recruitment
from beneficiaries.models import Beneficiary
from lms.models import Course
from reports.models import Report
from django.db.models.functions import TruncMonth

def dashboard_view(request):
    # Charts data - ensure we have default empty data
    donor_data = list(Donor.objects.annotate(
        donation_count=Count('donations')
    ).values('name', 'donation_count')[:5]) or []

    # Literacy level data
    literacy_data = list(Beneficiary.objects.values('literacy_level').annotate(
        count=Count('id')
    ).values('literacy_level', 'count')) or []

    # Project progress data
    project_data = list(Project.objects.annotate(
        beneficiary_count=Count('beneficiary')
    ).values('name', 'beneficiary_count')[:5]) or []

    # Course enrollment data
    course_data = list(Course.objects.annotate(
        enrollment_count=Count('enrollments')
    ).values('title', 'enrollment_count')[:5]) or []

    # Monthly donations (simplified)
    donation_trends = (
        Donation.objects
        .annotate(month=TruncMonth('date'))
        .values('month')
        .annotate(total=Sum('amount'))
        .order_by('month')[:12]
    )
    # Convert to list with proper formatting for JavaScript
    donation_trends_list = []
    for item in donation_trends:
        donation_trends_list.append({
            'month': item['month'].strftime('%Y-%m') if item['month'] else 'Unknown',
            'total': float(item['total']) if item['total'] else 0
        })
    donation_trends_list = donation_trends_list or []

    # Beneficiary attendance distribution
    attendance_data = list(Beneficiary.objects.values('attendance').annotate(
        count=Count('id')
    ).values('attendance', 'count').order_by('attendance')[:10]) or []

    context = {
        'donor_data': donor_data,
        'literacy_data': literacy_data,
        'project_data': project_data,
        'course_data': course_data,
        'donation_trends': donation_trends_list,
        'attendance_data': attendance_data,
        'dashboard_projects_count': Project.objects.count(),
        'dashboard_donors_count': Donor.objects.count(),
        'dashboard_beneficiaries_count': Beneficiary.objects.count(),
        'dashboard_recruitments_count': Recruitment.objects.count(),
        'dashboard_courses_count': Course.objects.filter(is_active=True).count(),
        'dashboard_reports_count': Report.objects.count(),
    }
    return render(request, 'dashboard/index.html', context)
# from django.shortcuts import render
# from django.db.models import Count, Sum
# from django.db.models.functions import TruncMonth
# from donors.models import Donor
# from projects.models import Donation, Project
# from beneficiaries.models import Beneficiary
# from lms.models import Course

# def dashboard_view(request):
#     # Summary counts for top tiles
#     total_projects = Project.objects.count()
#     total_donors = Donor.objects.count()
#     total_beneficiaries = Beneficiary.objects.count()
#     active_courses = Course.objects.filter(is_active=True).count()  # adjust field name

#     # Donor Contributions tile
#     # Top 5 donors by total donated amount
#     top_donors = (
#         Donor.objects
#         .annotate(total_given=Sum('donation__amount'))   # use actual related_name if different
#         .values('id', 'name', 'total_given')
#         .order_by('-total_given')[:5]
#     )

#     # Literacy Levels tile
#     literacy_breakdown = (
#         Beneficiary.objects
#         .values('literacy_level')
#         .annotate(count=Count('id'))
#         .order_by('-count')
#     )

#     # Project Beneficiaries tile
#     top_projects = (
#         Project.objects
#         .annotate(beneficiary_count=Count('beneficiary'))  # adjust related_name if needed
#         .values('id', 'name', 'beneficiary_count')
#         .order_by('-beneficiary_count')[:5]
#     )

#     # Course Enrollments tile
#     top_courses = (
#         Course.objects
#         .annotate(enrollment_count=Count('enrollments'))  # adjust related_name if needed
#         .values('id', 'title', 'enrollment_count')
#         .order_by('-enrollment_count')[:5]
#     )

#     # Donation trends for a mini chart
#     donation_trends = (
#         Donation.objects
#         .annotate(month=TruncMonth('date'))
#         .values('month')
#         .annotate(total=Sum('amount'))
#         .order_by('month')[:12]
#     )

#     context = {
#         'total_projects': total_projects,
#         'total_donors': total_donors,
#         'total_beneficiaries': total_beneficiaries,
#         'active_courses': active_courses,
#         'top_donors': list(top_donors),
#         'literacy_breakdown': list(literacy_breakdown),
#         'top_projects': list(top_projects),
#         'top_courses': list(top_courses),
#         'donation_trends': list(donation_trends),
#     }
#     return render(request, 'dashboard/index.html', context)
