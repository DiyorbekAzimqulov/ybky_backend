from datetime import datetime, timedelta, timezone
from django.conf import settings
from django.db.models import Q
from .models import Booking, Room
from .utils import reverse_change_date_format, get_datetime_str


def get_office_start_end_datetime(date: datetime = None):
    office_start = settings.OFFICE_HOURS['start_time']
    office_end = settings.OFFICE_HOURS['end_time']
    office_start = date.replace(
        hour=office_start.hour,
        minute=office_start.minute,
        second=office_start.second,
        microsecond=0,
        tzinfo=timezone.utc,
    )
    office_end = date.replace(
        hour=office_end.hour,
        minute=office_end.minute,
        second=office_end.second,
        microsecond=0,
        tzinfo=timezone.utc,
    )
    return office_start, office_end


def can_create_booking(start_time, end_time, room: Room):
    office_start, office_end = get_office_start_end_datetime(start_time)
    office_start = office_start.replace(tzinfo=None)
    office_end = office_end.replace(tzinfo=None)
    print(office_start, office_end, start_time, end_time)
    if start_time < office_start or end_time > office_end:
        print('Office hours are from {} to {}'.format(office_start,
                                                      office_end))
        return False
    print('hello')
    result = Booking.objects.filter(
        Q(start_time__lte=start_time, end_time__gt=start_time)
        | Q(start_time__lt=end_time, end_time__gte=end_time)
        | Q(start_time__gte=start_time, start_time__lt=end_time),
        room=room,
    ).exists()
    a = Booking.objects.filter(
        Q(start_time__lte=start_time, end_time__gt=start_time)
        | Q(start_time__lt=end_time, end_time__gte=end_time)
        | Q(start_time__gte=start_time, start_time__lt=end_time),
        room=room,
    )
    print(list(a.values('start_time', 'end_time')))
    return result is False


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
        second=office_start.second,
        microsecond=0,
        tzinfo=timezone.utc,
    )
    office_end = date.replace(
        hour=office_end.hour,
        minute=office_end.minute,
        second=office_end.second,
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
        if current_time < booking['start_time']:
            available_periods.append({
                'start':
                reverse_change_date_format(get_datetime_str(current_time)),
                'end':
                reverse_change_date_format(
                    get_datetime_str(booking['start_time']))
            })

        current_time = booking['end_time']

    if current_time < office_end:
        available_periods.append({
            'start':
            reverse_change_date_format(get_datetime_str(current_time)),
            'end':
            reverse_change_date_format(get_datetime_str(office_end))
        })
    return available_periods
