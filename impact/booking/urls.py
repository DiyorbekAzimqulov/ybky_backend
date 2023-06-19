from django.urls import path
from . import views

urlpatterns = [
    path('rooms/', views.RoomListCreateAPIView.as_view()),
    path('rooms/<int:pk>', views.RoomRetrieveUpdateDestroyAPIView.as_view()),
    path('rooms/<int:pk>/availability', views.room_availability_view),
    path('rooms/<int:pk>/book', views.create_booking_view),
]
