from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.urls import reverse


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            next_url = request.GET.get('next') or request.POST.get('next') or reverse('lms:course_list')
            return redirect(next_url)
    else:
        form = UserCreationForm()
        next_url = request.GET.get('next', '')
    return render(request, 'registration/register.html', {'form': form, 'next': next_url})
