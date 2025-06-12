from django.shortcuts import render, redirect, get_object_or_404
from .models import Booking
from .forms import BookingForm
from services.models import Service
from django.contrib.auth.decorators import login_required
from django.utils.timezone import datetime

@login_required
def create_booking(request, service_id):
    service = get_object_or_404(Service, pk=service_id)
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.customer = request.user
            booking.service = service

            # Check for conflict
            exists = Booking.objects.filter(
                service=service,
                booking_date=booking.booking_date,
                booking_time=booking.booking_time,
                status__in=['pending', 'confirmed']
            ).exists()

            if exists:
                form.add_error(None, "This slot is already booked.")
            else:
                booking.save()
                return redirect('my_bookings')
    else:
        form = BookingForm()
    return render(request, 'bookings/book_service.html', {'form': form, 'service': service})

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
        return redirect('my_bookings')
    return render(request, 'bookings/confirm_cancel.html', {'booking': booking})
