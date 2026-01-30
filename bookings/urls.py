from django.urls import path
from . import views

app_name = 'bookings'

urlpatterns = [
    path('book/<int:room_id>/', views.book_room, name='book_room'),
    path('payment/<int:booking_id>/', views.payment, name='payment'),
    path('payment-success/<int:booking_id>/', views.payment_success, name='payment_success'),
]
