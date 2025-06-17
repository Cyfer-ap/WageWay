from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Review
from .forms import PosterToWorkerReviewForm, WorkerToPosterReviewForm
from jobboard.models import JobPost
from django.db import IntegrityError
from bookings.models import Booking

@login_required
def review_worker(request, job_id):
    job = get_object_or_404(JobPost, id=job_id)

    # Must be job poster and job must be assigned and complete
    if job.posted_by != request.user or not job.is_assigned:
        messages.error(request, "You are not allowed to review this job.")
        return redirect('job_detail', job_id=job_id)

    accepted_app = job.applications.filter(status='accepted').first()
    if not accepted_app:
        messages.error(request, "No accepted worker for this job.")
        return redirect('job_detail', job_id=job_id)

    worker = accepted_app.applicant

    if Review.objects.filter(reviewer=request.user, job=job, review_type='poster_to_worker').exists():
        messages.warning(request, "You have already reviewed this worker.")
        return redirect('job_detail', job_id=job.id)

    if request.method == 'POST':
        form = PosterToWorkerReviewForm(request.POST)
        if form.is_valid():
            try:
                review = form.save(commit=False)
                review.reviewer = request.user
                review.reviewed_user = worker
                review.job = job
                review.review_type = 'poster_to_worker'
                review.save()
                messages.success(request, "Review submitted.")
                return redirect('job_detail', job_id=job.id)
            except IntegrityError:
                messages.error(request, "You have already submitted a review.")
    else:
        form = PosterToWorkerReviewForm()

    return render(request, 'reviews/review_worker.html', {'form': form, 'worker': worker, 'job': job})


@login_required
def review_poster(request, job_id):
    job = get_object_or_404(JobPost, id=job_id)

    accepted_app = job.applications.filter(applicant=request.user, status='accepted').first()
    if not accepted_app or not job.is_assigned:
        messages.error(request, "You are not allowed to review this job.")
        return redirect('job_list')

    if Review.objects.filter(reviewer=request.user, job=job, review_type='worker_to_poster').exists():
        messages.warning(request, "You have already reviewed this job poster.")
        return redirect('job_detail', job_id=job.id)

    if request.method == 'POST':
        form = WorkerToPosterReviewForm(request.POST)
        if form.is_valid():
            try:
                review = form.save(commit=False)
                review.reviewer = request.user
                review.reviewed_user = job.posted_by
                review.job = job
                review.review_type = 'worker_to_poster'
                review.save()
                messages.success(request, "Review submitted.")
                return redirect('job_detail', job_id=job.id)
            except IntegrityError:
                messages.error(request, "You have already submitted a review.")
    else:
        form = WorkerToPosterReviewForm()

    return render(request, 'reviews/review_poster.html', {'form': form, 'poster': job.posted_by, 'job': job})



@login_required
def review_provider_for_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, customer=request.user)

    if not booking.is_fully_completed:
        messages.error(request, "You can only review after the job is fully completed.")
        return redirect('customer_bookings')

    provider = booking.service.provider.user
    if Review.objects.filter(reviewer=request.user, booking=booking, review_type='poster_to_worker').exists():
        messages.warning(request, "You have already reviewed this provider.")
        return redirect('customer_bookings')

    if request.method == 'POST':
        form = PosterToWorkerReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.reviewer = request.user
            review.reviewed_user = provider
            review.booking = booking
            review.review_type = 'poster_to_worker'
            review.save()
            messages.success(request, "Review submitted.")
            return redirect('customer_bookings')
    else:
        form = PosterToWorkerReviewForm()

    return render(request, 'reviews/review_worker.html', {'form': form, 'worker': provider, 'booking': booking})


@login_required
def review_customer_for_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, service__provider__user=request.user)

    if not booking.is_fully_completed:
        messages.error(request, "You can only review after the job is fully completed.")
        return redirect('provider_bookings')

    customer = booking.customer
    if Review.objects.filter(reviewer=request.user, booking=booking, review_type='worker_to_poster').exists():
        messages.warning(request, "You have already reviewed this customer.")
        return redirect('provider_bookings')

    if request.method == 'POST':
        form = WorkerToPosterReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.reviewer = request.user
            review.reviewed_user = customer
            review.booking = booking
            review.review_type = 'worker_to_poster'
            review.save()
            messages.success(request, "Review submitted.")
            return redirect('provider_bookings')
    else:
        form = WorkerToPosterReviewForm()

    return render(request, 'reviews/review_poster.html', {'form': form, 'poster': customer, 'booking': booking})
