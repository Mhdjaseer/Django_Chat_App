from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("<str:room_name>/", views.room, name="room"),
    path('room/exit/<int:room_id>/',views.exit_room, name='exit_room'),
   
]