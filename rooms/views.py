# rooms/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Room
from bookings.models import Booking

# Display all rooms
@login_required(login_url='accounts:login')  # Only logged-in users can view rooms
def room_list(request):
    rooms = Room.objects.all()
    return render(request, 'rooms/room_list.html', {'rooms': rooms})

# Booking a room
@login_required(login_url='accounts:login')
def book_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)

    if request.method == 'POST':
        # For now, we are using dummy payment logic
        # In real scenario, integrate with a payment gateway
        booking = Booking.objects.create(
            user=request.user,
            room=room,
            status='Pending'  # Status can later be 'Paid' after real payment
        )
        # Redirect to payment page (or dummy payment)
        return redirect('rooms:payment', booking_id=booking.id)

    return render(request, 'rooms/book_room.html', {'room': room})

# Dummy payment page
@login_required(login_url='accounts:login')
def payment(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)

    if request.method == 'POST':
        # Here we assume payment is always successful
        booking.status = 'Paid'
        booking.save()
        return redirect('rooms:payment_success', booking_id=booking.id)

    return render(request, 'rooms/payment.html', {'booking': booking})

# Payment success page
@login_required(login_url='accounts:login')
def payment_success(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    return render(request, 'rooms/payment_success.html', {'booking': booking})
