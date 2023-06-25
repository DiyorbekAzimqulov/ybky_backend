from datetime import datetime, timezone
from django.conf import settings
import pytest
from .models import Booking, Room, Availability
from .services import can_create_booking, calculate_available_periods

OFFICE_START = settings.OFFICE_HOURS['start_time']
OFFICE_END = settings.OFFICE_HOURS['end_time']


@pytest.fixture
def room():
    return Room.objects.create(name='test room', capacity=10, type='focus')


@pytest.fixture
def booking(room):
    return Booking.objects.create(
        room=room,
        resident={'name': 'test user'},
        start_time=datetime.strptime(
            '2023-06-10 10:00:00',
            '%Y-%m-%d %H:%M:%S').replace(tzinfo=timezone.utc),
        end_time=datetime.strptime(
            '2023-06-10 11:00:00',
            '%Y-%m-%d %H:%M:%S').replace(tzinfo=timezone.utc),
    )


@pytest.mark.django_db
def test_can_create_booking(booking):
    assert can_create_booking(
        room=booking.room,
        start_time=datetime.strptime(
            '2023-06-10 09:00:00',
            '%Y-%m-%d %H:%M:%S').replace(tzinfo=timezone.utc),
        end_time=datetime.strptime(
            '2023-06-10 10:00:00',
            '%Y-%m-%d %H:%M:%S').replace(tzinfo=timezone.utc),
    )
    assert not can_create_booking(
        room=booking.room,
        start_time=datetime.strptime(
            '2023-06-10 10:00:00',
            '%Y-%m-%d %H:%M:%S').replace(tzinfo=timezone.utc),
        end_time=datetime.strptime(
            '2023-06-10 11:00:00',
            '%Y-%m-%d %H:%M:%S').replace(tzinfo=timezone.utc),
    )
    assert can_create_booking(
        room=booking.room,
        start_time=datetime.strptime(
            '2023-06-10 9:10:00',
            '%Y-%m-%d %H:%M:%S').replace(tzinfo=timezone.utc),
        end_time=datetime.strptime(
            '2023-06-10 10:00:00',
            '%Y-%m-%d %H:%M:%S').replace(tzinfo=timezone.utc),
    )
    assert not can_create_booking(
        room=booking.room,
        start_time=datetime.strptime(
            '2023-06-10 10:10:00',
            '%Y-%m-%d %H:%M:%S').replace(tzinfo=timezone.utc),
        end_time=datetime.strptime(
            '2023-06-10 10:50:00',
            '%Y-%m-%d %H:%M:%S').replace(tzinfo=timezone.utc),
    )


@pytest.mark.django_db
def test_calculate_availability(room, booking):
    date = datetime(2023, 6, 10, 9, 0, 0, tzinfo=timezone.utc)
    availability = calculate_available_periods(room, date)
    office_start = date.replace(
        hour=OFFICE_START.hour,
        minute=OFFICE_START.minute,
        second=0,
        microsecond=0,
    )
    office_end = date.replace(
        hour=OFFICE_END.hour,
        minute=OFFICE_END.minute,
        second=0,
        microsecond=0,
    )
    assert availability == [
        {
            'start_time': office_start,
            'end_time': booking.start_time,
        },
        {
            'start_time': booking.end_time,
            'end_time': office_end,
        },
    ]
