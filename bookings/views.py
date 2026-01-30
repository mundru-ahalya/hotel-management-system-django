from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from datetime import datetime
from rooms.models import Room
from .models import Booking
'''
@login_required(login_url='accounts:login')
def book_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)

    if request.method == 'POST':
        check_in = request.POST.get('check_in')
        check_out = request.POST.get('check_out')

        check_in_date = datetime.strptime(check_in, '%Y-%m-%d').date()
        check_out_date = datetime.strptime(check_out, '%Y-%m-%d').date()

        # Check for overlapping bookings
        overlapping_bookings = Booking.objects.filter(
            room=room,
            status=True,  # Only consider confirmed bookings
        ).filter(
            check_in__lt=check_out_date,
            check_out__gt=check_in_date
        )

        if overlapping_bookings.exists():
            error = "Sorry! This room is already booked for the selected dates."
            return render(request, 'booking.html', {'room': room, 'error': error})

        # Calculate total price
        nights = (check_out_date - check_in_date).days
        total_price = room.price_per_night * nights

        # Create booking with pending status
        booking = Booking.objects.create(
            user=request.user,
            room=room,
            check_in=check_in_date,
            check_out=check_out_date,
            total_price=total_price,
            status=False  # pending payment
        )

        return redirect('bookings:payment', booking_id=booking.id)

    return render(request, 'booking.html', {'room': room})
'''
'''
from datetime import datetime
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from rooms.models import Room
from .models import Booking

@login_required(login_url='accounts:login')
def book_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)

    if request.method == 'POST':
        check_in = request.POST.get('check_in')
        check_out = request.POST.get('check_out')

        check_in_date = datetime.strptime(check_in, '%Y-%m-%d').date()
        check_out_date = datetime.strptime(check_out, '%Y-%m-%d').date()

        if check_in_date >= check_out_date:
            error = "Check-out date must be after check-in date."
            return render(request, 'booking.html', {'room': room, 'error': error})

        # Check for any booking overlapping (ignore status)
        overlapping_bookings = Booking.objects.filter(
            room=room,
        ).filter(
            check_in__lt=check_out_date,
            check_out__gt=check_in_date
        )

        if overlapping_bookings.exists():
            error = "Sorry! This room is already booked for the selected dates."
            return render(request, 'booking.html', {'room': room, 'error': error})

        # Calculate total price
        nights = (check_out_date - check_in_date).days
        total_price = room.price_per_night * nights

        # Create booking
        booking = Booking.objects.create(
            user=request.user,
            room=room,
            check_in=check_in_date,
            check_out=check_out_date,
            total_price=total_price,
            status=False  # Pending payment
        )

        return redirect('bookings:payment', booking_id=booking.id)

    return render(request, 'booking.html', {'room': room})

@login_required(login_url='accounts:login')
def payment(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)

    if request.method == 'POST':
        booking.status = "Paid"
        booking.save()
        return redirect('bookings:payment_success', booking_id=booking.id)

    return render(request, 'payment.html', {'booking': booking})


@login_required(login_url='accounts:login')
def payment_success(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    return render(request, 'payment_success.html', {'booking': booking})
'''




from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.core.mail import send_mail
from django.conf import settings

from rooms.models import Room
from .models import Booking


@login_required(login_url='accounts:login')
def book_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)

    if request.method == 'POST':
        check_in = request.POST.get('check_in')
        check_out = request.POST.get('check_out')

        check_in_date = datetime.strptime(check_in, '%Y-%m-%d').date()
        check_out_date = datetime.strptime(check_out, '%Y-%m-%d').date()

        if check_in_date >= check_out_date:
            return render(request, 'booking.html', {
                'room': room,
                'error': 'Check-out date must be after check-in date.'
            })

        overlapping_bookings = Booking.objects.filter(
            room=room,
            check_in__lt=check_out_date,
            check_out__gt=check_in_date
        )

        if overlapping_bookings.exists():
            return render(request, 'booking.html', {
                'room': room,
                'error': 'Sorry! This room is already booked for the selected dates.'
            })

        nights = (check_out_date - check_in_date).days
        total_price = room.price_per_night * nights

        booking = Booking.objects.create(
            user=request.user,
            room=room,
            check_in=check_in_date,
            check_out=check_out_date,
            total_price=total_price,
            status="Pending"
        )

        return redirect('bookings:payment', booking_id=booking.id)

    return render(request, 'booking.html', {'room': room})


@login_required(login_url='accounts:login')
def payment(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)

    if request.method == 'POST':
        booking.status = "Paid"
        booking.save()
        return redirect('bookings:payment_success', booking_id=booking.id)

    return render(request, 'payment.html', {'booking': booking})


@login_required(login_url='accounts:login')
def payment_success(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)

    send_mail(
        subject='Room Booking Confirmed – Hotel Management',
        message=f'''
Hello {booking.user.username},

Your room booking is CONFIRMED ✅

Room Number : {booking.room.room_number}
Room Type   : {booking.room.room_type}
Check-in    : {booking.check_in}
Check-out   : {booking.check_out}
Total Price : ₹{booking.total_price}

Thank you for choosing our hotel.
We look forward to welcoming you!

Hotel Management Team
''',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[booking.user.email],
        fail_silently=False
    )

    return render(request, 'payment_success.html', {'booking': booking})
