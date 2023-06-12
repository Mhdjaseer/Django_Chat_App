from django.urls import path

from . import views


urlpatterns = [
    path("home", views.index, name="index"),
    path("<str:room_name>/", views.room, name="room"),
    path('room/exit/<int:room_id>/',views.exit_room, name='exit_room'),
    path('report/<int:id>/',views.Reported,name='report'),

    path('message/<int:message_id>/update/', views.update_message, name='update_message'),
    path('delete/<int:message_id>/', views.delete_message, name='delete_message'),

    
   
]