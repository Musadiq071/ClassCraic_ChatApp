from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.views.decorators.http import require_POST
from allauth.account.models import EmailAddress

from .models import Profile
from .forms import *


def profile_view(request, username=None):
    if username:
        profile = get_object_or_404(User, username=username).profile
    else:
        try:
            profile = request.user.profile
        except:
            return redirect('account_login')

    return render(request, 'user/profile.html', {
        'profile': profile
    })


@login_required
def profile_edit_view(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)

    if request.method == "POST":
        old_role = profile.role
        form = ProfileForm(request.POST, request.FILES, instance=profile)

        if form.is_valid():
            updated_profile = form.save(commit=False)

            if old_role != 'teacher' and updated_profile.role == 'teacher':
                updated_profile.teacher_approved = False
                messages.info(request, "Your teacher account request has been submitted for admin approval.")

            updated_profile.save()
            return redirect('profile')

    onboarding = request.path == reverse('profile-onboarding')

    return render(request, 'user/profile_edit.html', {
        'form': form,
        'onboarding': onboarding
    })


@login_required
def profile_settings_view(request):
    return render(request, 'user/profile_settings.html')


@login_required
def profile_emailchange(request):
    if request.htmx:
        form = EmailForm(instance=request.user)
        return render(request, 'partials/email_form.html', {
            'form': form
        })

    if request.method == 'POST':
        form = EmailForm(request.POST, instance=request.user)

        if form.is_valid():
            email = form.cleaned_data['email']

            # check email is not already used
            if User.objects.filter(email=email).exclude(id=request.user.id).exists():
                messages.warning(request, f'{email} is already in use.')
                return redirect('profile-settings')

            form.save()

            # signal updates allauth email and marks it unverified
            email_address = EmailAddress.objects.filter(user=request.user).first()

            if email_address:
                email_address.send_confirmation(request)

            messages.success(request, "Verification email sent.")
            return redirect('profile-settings')

        messages.warning(request, 'Form is not valid.')
        return redirect('profile-settings')

    return redirect('home')


@login_required
def profile_emailverify(request):
    email_address = EmailAddress.objects.filter(user=request.user).first()

    if email_address:
        email_address.send_confirmation(request)
        messages.success(request, "Verification email sent!")
    else:
        messages.error(request, "No email found.")

    return redirect('profile-settings')


@login_required
def profile_delete_view(request):
    user = request.user

    if request.method == "POST":
        logout(request)
        user.delete()
        messages.success(request, 'Account deleted Successfully, Sorry you left us.')
        return redirect('home')

    return render(request, 'user/profile_delete.html')


@login_required
def teacher_approval_list(request):
    if not (request.user.is_staff or request.user.is_superuser):
        messages.warning(request, "You are not allowed to access this page.")
        return redirect('home')

    pending_teachers = Profile.objects.filter(
        role='teacher',
        teacher_approved=False
    ).select_related('user')

    approved_teachers = Profile.objects.filter(
        role='teacher',
        teacher_approved=True
    ).select_related('user')

    return render(request, 'user/teacher_approval_list.html', {
        'pending_teachers': pending_teachers,
        'approved_teachers': approved_teachers,
    })


@login_required
@require_POST
def approve_teacher(request, username):
    if not (request.user.is_staff or request.user.is_superuser):
        messages.warning(request, "You are not allowed to do that.")
        return redirect('home')

    profile = get_object_or_404(
        Profile.objects.select_related('user'),
        user__username=username,
        role='teacher'
    )

    profile.teacher_approved = True
    profile.save()

    messages.success(request, f"{profile.user.username} has been approved as a teacher.")
    return redirect('teacher-approval-list')


@login_required
@require_POST
def disapprove_teacher(request, username):
    if not (request.user.is_staff or request.user.is_superuser):
        messages.warning(request, "You are not allowed to do that.")
        return redirect('home')

    profile = get_object_or_404(
        Profile.objects.select_related('user'),
        user__username=username,
        role='teacher'
    )

    profile.teacher_approved = False
    profile.save()

    messages.success(request, f"{profile.user.username} has been disapproved as a teacher.")
    return redirect('teacher-approval-list')