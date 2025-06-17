from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import JobPost, JobApplication
from .forms import JobPostForm, JobApplicationForm
from django.utils import timezone
from django.contrib import messages
from django.db.models import Q
from notifications.models import Notification
from django.urls import reverse
from emails.utils import send_dynamic_email


@login_required
def post_job(request):
    if request.method == 'POST':
        form = JobPostForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.posted_by = request.user
            job.save()
            messages.success(request, "Job posted successfully.")

            Notification.objects.create(
                user=request.user,
                message=f"📢 You posted a new job: '{job.title}' for {job.date_needed}",
                url=reverse('my_posted_jobs')
            )

            send_dynamic_email(
                subject='Job Post Confirmation - Wage Way',
                to_email=request.user.email,
                template_name='emails/job_post_confirmation.html',
                context={'user': request.user, 'job': job}
            )

            return redirect('my_posted_jobs')
    else:
        form = JobPostForm()
    return render(request, 'jobboard/post_job.html', {'form': form})

@login_required
def job_list(request):
    jobs = JobPost.objects.filter(is_assigned=False, date_needed__gte=timezone.now().date()).order_by('date_needed')
    query = request.GET.get('q')
    if query:
        jobs = jobs.filter(Q(title__icontains=query) | Q(description__icontains=query) | Q(category__icontains=query))
    return render(request, 'jobboard/job_list.html', {'jobs': jobs})

@login_required
def job_detail(request, job_id):
    job = get_object_or_404(JobPost, id=job_id)
    applications = None
    try:
        applications = job.applications.all() if request.user == job.posted_by else None
    except:
        applications = None

    has_applied = JobApplication.objects.filter(job=job, applicant=request.user).exists()
    return render(request, 'jobboard/job_detail.html', {
        'job': job,
        'applications': applications,
        'has_applied': has_applied
    })

@login_required
def apply_to_job(request, job_id):
    job = get_object_or_404(JobPost, id=job_id)
    if JobApplication.objects.filter(job=job, applicant=request.user).exists():
        messages.warning(request, "You have already applied to this job.")
        return redirect('job_detail', job_id=job_id)

    if request.method == 'POST':
        form = JobApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            app = form.save(commit=False)
            app.job = job
            app.applicant = request.user
            app.save()
            messages.success(request, "Application submitted.")

            Notification.objects.create(
                user=job.posted_by,
                message=f"📩 New application from {request.user.username} for your job: '{job.title}'",
                url=reverse('job_detail', args=[job.id])
            )

            Notification.objects.create(
                user=request.user,
                message=f"✅ You applied for '{job.title}'",
                url=reverse('job_detail', args=[job.id])
            )

            send_dynamic_email(
                subject='New Application Received - Wage Way',
                to_email=job.posted_by.email,
                template_name='emails/job_application_received.html',
                context={'user': job.posted_by, 'applicant': request.user, 'job': job, 'application': app}
            )

            send_dynamic_email(
                subject='Application Submitted - Wage Way',
                to_email=request.user.email,
                template_name='emails/job_application_confirmation.html',
                context={'user': request.user, 'job': job, 'application': app}
            )

            return redirect('job_detail', job_id=job.id)
    else:
        form = JobApplicationForm()
    return render(request, 'jobboard/apply_job.html', {'form': form, 'job': job})

@login_required
def my_posted_jobs(request):
    jobs = JobPost.objects.filter(posted_by=request.user)
    return render(request, 'jobboard/my_posted_jobs.html', {'jobs': jobs})

@login_required
def my_applications(request):
    apps = JobApplication.objects.filter(applicant=request.user).select_related('job')
    return render(request, 'jobboard/my_applications.html', {'applications': apps})

@login_required
def accept_application(request, application_id):
    app = get_object_or_404(JobApplication, pk=application_id, job__posted_by=request.user)
    job = app.job

    if job.is_assigned:
        messages.warning(request, "This job has already been assigned.")
    else:
        app.status = 'accepted'
        app.save()
        # Mark others as rejected
        JobApplication.objects.filter(job=job).exclude(id=app.id).update(status='rejected')
        job.is_assigned = True
        job.save()
        messages.success(request, f"{app.applicant.username} has been accepted for the job.")

        Notification.objects.create(
            user=app.applicant,
            message=f"🎉 You have been accepted for the job: '{job.title}'",
            url=reverse('job_detail', args=[job.id])
        )

        Notification.objects.create(
            user=request.user,
            message=f"✅ You accepted {app.applicant.username} for the job: '{job.title}'",
            url=reverse('job_detail', args=[job.id])
        )

        send_dynamic_email(
            subject='You’ve Been Accepted! - Wage Way',
            to_email=app.applicant.email,
            template_name='emails/job_application_accepted.html',
            context={'user': app.applicant, 'job': job, 'poster': request.user}
        )

        send_dynamic_email(
            subject='Applicant Accepted - Wage Way',
            to_email=request.user.email,
            template_name='emails/job_application_accepted_notify_poster.html',
            context={'user': request.user, 'applicant': app.applicant, 'job': job}
        )

    return redirect('job_detail', job_id=job.id)

@login_required
def reject_application(request, application_id):
    app = get_object_or_404(JobApplication, pk=application_id, job__posted_by=request.user)
    if app.status not in ['accepted', 'rejected']:
        app.status = 'rejected'
        app.save()
        messages.success(request, "Application rejected.")

        Notification.objects.create(
            user=app.applicant,
            message=f"❌ Your application was rejected for '{app.job.title}'",
            url=reverse('job_detail', args=[app.job.id])
        )

        send_dynamic_email(
            subject='Application Rejected - Wage Way',
            to_email=app.applicant.email,
            template_name='emails/job_application_rejected.html',
            context={'user': app.applicant, 'job': app.job}
        )

    return redirect('job_detail', job_id=app.job.id)

