from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from emails.utils import send_dynamic_email
from .models import Booking
from .forms import BookingForm
from services.models import Service
from django.contrib.auth.decorators import login_required
from django.utils.timezone import datetime
from notifications.models import Notification
from django.http import HttpResponseForbidden
from django.utils.timezone import now
from django.utils.timezone import make_aware



@login_required
def create_booking(request, service_id):
    service = get_object_or_404(Service, pk=service_id)

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.customer = request.user
            booking.service = service

            # Get cleaned date/time from form
            booking_date = form.cleaned_data['booking_date']
            booking_time = form.cleaned_data['booking_time']

            # 🔒 Prevent booking in the past
            booking_dt = make_aware(datetime.combine(booking_date, booking_time))

            if booking_dt < now():
                form.add_error(None, "Cannot book in the past.")
                return render(request, 'bookings/book_service.html', {'form': form, 'service': service})

            # ✅ Validate based on service.job_type
            if service.job_type == 'one_time':
                if not service.job_date:
                    form.add_error('booking_date', "This service doesn't have a valid date.")
                elif booking_date != service.job_date:
                    form.add_error('booking_date', f"This is a one-time service available only on {service.job_date}.")
            elif service.job_type == 'recurring':
                weekday = booking_date.strftime('%a').lower()[:3]  # e.g. 'mon'
                if weekday not in service.available_days:
                    form.add_error('booking_date', f"This service is not available on {booking_date.strftime('%A')}.")

            # 🔒 Prevent double bookings
            exists = Booking.objects.filter(
                service=service,
                booking_date=booking_date,
                booking_time=booking_time,
                status__in=['pending', 'confirmed']
            ).exists()
            if exists:
                form.add_error(None, "This time slot is already booked. Please choose another.")

            # 🚀 Save if no errors
            if not form.errors:
                booking.status = 'pending'
                booking.provider_response = 'waiting'
                booking.save()

                # Notify Provider
                Notification.objects.create(
                    user=service.provider.user,
                    message=f"🔔 Booking request from {request.user.username} for '{service.title}' on {booking.booking_date} at {booking.booking_time}",
                    url=reverse('provider_bookings')
                )

                # Notify Customer
                Notification.objects.create(
                    user=request.user,
                    message=f"✅ Booking request sent for '{service.title}'. Awaiting provider confirmation.",
                    url=reverse('my_bookings')
                )

                # After booking.save()
                send_dynamic_email(
                    subject='Booking Confirmation - Wage Way',
                    to_email=request.user.email,
                    template_name='emails/booking_confirmation.html',
                    context={'user': request.user, 'booking': booking}
                )

                return redirect('my_bookings')
    else:
        form = BookingForm()

    return render(request, 'bookings/book_service.html', {'form': form, 'service': service})


@login_required
def accept_booking(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id, service__provider=request.user.providerprofile)
    if booking.provider_response != 'waiting':
        return HttpResponseForbidden("Already responded.")
    booking.status = 'confirmed'
    booking.provider_response = 'accepted'
    booking.save()

    Notification.objects.create(
        user=booking.customer,
        message=f"🎉 Your booking for '{booking.service.title}' was accepted!",
        url=reverse('my_bookings')
    )

    send_dynamic_email(
        subject='Your Booking is Approved!',
        to_email=booking.customer.email,
        template_name='emails/booking_approved.html',
        context={'user': booking.customer, 'booking': booking}
    )

    return redirect('provider_bookings')


@login_required
def reject_booking(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id, service__provider=request.user.providerprofile)

    if booking.provider_response != 'waiting':
        return HttpResponseForbidden("Already responded.")

    booking.status = 'rejected'
    booking.provider_response = 'rejected'
    booking.save()

    Notification.objects.create(
        user=booking.customer,
        message=f"⚠️ Your booking for '{booking.service.title}' was rejected by the provider.",
        url=reverse('my_bookings')
    )

    send_dynamic_email(
        subject='Booking Rejected',
        to_email=booking.customer.email,
        template_name='emails/booking_rejected.html',
        context={'user': booking.customer, 'booking': booking}
    )

    return redirect('provider_bookings')


@login_required
def customer_bookings(request):
    bookings = request.user.customer_bookings.all().order_by('-booking_date')
    return render(request, 'bookings/my_bookings.html', {'bookings': bookings})


@login_required
def provider_bookings(request):
    bookings = Booking.objects.filter(service__provider=request.user.providerprofile).order_by('-booking_date')
    return render(request, 'bookings/provider_bookings.html', {'bookings': bookings})

@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id, customer=request.user)
    if request.method == 'POST':
        booking.status = 'cancelled'
        booking.save()

        Notification.objects.create(
            user=booking.service.provider.user,
            message=f"{request.user.username} cancelled the booking for '{booking.service.title}' on {booking.booking_date}.",
            url=reverse('provider_bookings')
        )

        Notification.objects.create(
            user=request.user,
            message=f"You cancelled your booking for '{booking.service.title}' with {booking.service.provider.user.username}.",
            url=reverse('my_bookings')
        )

        send_dynamic_email(
            subject='Booking Cancelled',
            to_email=request.user.email,
            template_name='emails/booking_cancelled.html',
            context={'user': request.user, 'booking': booking}
        )

        return redirect('my_bookings')
    return render(request, 'bookings/confirm_cancel.html', {'booking': booking})

