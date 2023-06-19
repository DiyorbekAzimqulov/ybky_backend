from datetime import datetime, timedelta, timezone
from django.conf import settings
from django.db.models import Q
from .models import Booking, Room


def can_create_booking(start_time, end_time, room: Room):
    return Booking.objects.filter(
        Q(start_time__lte=start_time, end_time__gt=start_time)
        | Q(start_time__lt=end_time, end_time__gte=end_time),
        room=room,
    ).exists() is False


def create_booking(start_time, end_time, room: Room, resident):
    if can_create_booking(start_time, end_time, room):
        return Booking.objects.create(
            start_time=start_time,
            end_time=end_time,
            room=room,
            resident=resident,
        )
    return None


def calculate_available_periods(
    room: Room,
    date: datetime = None,
):
    office_start = settings.OFFICE_HOURS['start_time']
    office_end = settings.OFFICE_HOURS['end_time']
    if date is None:
        date = datetime.now().replace(hour=0,
                                      minute=0,
                                      second=0,
                                      microsecond=0,
                                      tzinfo=timezone.utc)
    start_time = date
    end_time = date + timedelta(days=1) - timedelta(seconds=1)
    office_start = date.replace(
        hour=office_start.hour,
        minute=office_start.minute,
        second=0,
        microsecond=0,
        tzinfo=timezone.utc,
    )
    office_end = date.replace(
        hour=office_end.hour,
        minute=office_end.minute,
        second=0,
        microsecond=0,
        tzinfo=timezone.utc,
    )
    bookings = list(
        Booking.objects.filter(room=room,
                               start_time__gte=start_time,
                               end_time__lte=end_time).values(
                                   'start_time',
                                   'end_time').order_by('start_time'))
    available_periods = []
    current_time = office_start

    for booking in bookings:
        print('current_time', current_time, 'booking_start_time',
              booking['start_time'])
        if current_time < booking['start_time']:
            available_periods.append({
                'start_time': current_time,
                'end_time': booking['start_time']
            })

        current_time = booking['end_time']

    if current_time < office_end:
        available_periods.append({
            'start_time': current_time,
            'end_time': office_end
        })
    return available_periods
