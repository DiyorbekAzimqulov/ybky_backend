import datetime
from django.shortcuts import get_object_or_404
from django.http import Http404
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Booking, Room
from .serializers import RoomSerializer
from .services import calculate_available_periods, create_booking
from .utils import (validate_date, get_datetime_obj, get_datetime_obj_for_date,
                    validate_datetime, change_date_format,
                    reverse_change_date_format,
                    validate_start_end_datetime_same_day)
from .paginations import CustomPagination


class RoomListCreateAPIView(ListCreateAPIView):
    queryset = Room.objects.all()
    pagination_class = CustomPagination
    serializer_class = RoomSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        page_number = self.request.query_params.get('page', 1)
        query_params = self.request.query_params
        for key, value in query_params.items():
            if key == 'type':
                queryset = queryset.filter(**{key: value})
            if key == 'search':
                queryset = queryset.filter(name__icontains=value)
        paginator = self.pagination_class()
        paginator.page = page_number
        paginated_queryset = paginator.paginate_queryset(
            queryset, self.request)
        return paginated_queryset


class RoomRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    def handle_exception(self, exc):
        if isinstance(exc, Http404):
            return self.not_found_response()

        return super().handle_exception(exc)

    def not_found_response(self):
        return Response({"error": "topilmadi"},
                        status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def room_availability_view(request, pk):
    date = request.query_params.get('date', None)
    if date is None:
        date = datetime.datetime.now().strftime('%Y-%m-%d')
    else:
        date = change_date_format(date)
    if not validate_date(date):
        return Response(
            {
                'error':
                'Invalid date format! expected (YYYY-MM-DD) or `date` must be in the future'
            },
            status=400)
    room = get_object_or_404(Room, pk=pk)
    availability = calculate_available_periods(room,
                                               get_datetime_obj_for_date(date))
    return Response(availability, status=200)


@api_view(['POST'])
def create_booking_view(request, pk):
    room = get_object_or_404(Room, pk=pk)
    start_time = request.data.get('start', None)
    end_time = request.data.get('end', None)
    start_time = change_date_format(start_time)
    end_time = change_date_format(end_time)
    resident = request.data.get('resident', None)
    if not validate_datetime(start_time) or not validate_datetime(end_time):
        return Response(
            {
                'error':
                'Invalid date format! expected (YYYY-MM-DD HH:MM:SS) or `start` and `end` must be in the future'
            },
            status=400)
    if not validate_start_end_datetime_same_day(start_time, end_time):
        return Response(
            {
                'error':
                'Invalid date format! `start` and `end` must be in the same day or `start` must be before `end`'
            },
            status=400)
    booking = create_booking(
        get_datetime_obj(start_time),
        get_datetime_obj(end_time),
        room,
        resident,
    )
    if booking is None:
        return Response({'error': 'uzr, siz tanlagan vaqtda xona band'},
                        status=410)
    return Response({'message': 'xona muvaffaqiyatli band qilindi'},
                    status=201)
