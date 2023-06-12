from django.shortcuts import render,redirect
from .forms import NewUserForm,MessageForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate,login,logout
from .models import Room,Message
from django.contrib.auth.decorators import login_required

# Create your views here.
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages
from .models import Room
from django.http import JsonResponse
from datetime import timedelta
from django.utils import timezone

@login_required
def index(request):
    if request.method == 'POST':
        room_name = request.POST['room_name']
        try:
            room = Room.objects.get(name=room_name)
            messages.error(request, f"A room with the name '{room_name}' already exists.")
            return redirect('index')
        except Room.DoesNotExist:
            # Create the room
            room = Room.objects.create(name=room_name)
            room.users.add(request.user)  # Add the room creator as a user
            messages.success(request, f"You have created and joined the room '{room.name}'.")
            # Redirect to the created room
            return redirect('room', room_name=room.name)

    joined_rooms = Room.objects.filter(users=request.user)
    available_rooms = Room.objects.exclude(users=request.user)

   
    if request.method == 'GET' and 'join_room' in request.GET:
        room_id = request.GET.get('join_room')
        room = get_object_or_404(Room, id=room_id)
        if request.user not in room.users.all():
            room.users.add(request.user)
            messages.success(request, f"You have joined the room '{room.name}'.")

    context = {
        'joined_rooms': joined_rooms,
        'available_rooms': available_rooms,
        
    }
    return render(request, "chat/index.html", context)

@login_required
def room(request, room_name):
    room = get_object_or_404(Room, name=room_name)
    username=request.user.username
    messages = room.messages.all()
    joined_rooms = Room.objects.filter(users=request.user)
    available_rooms = Room.objects.exclude(users=request.user)
    creator = room.users.first() 
    
    context={
        "room_name": room_name,
        "messages": messages,
        "username":username,
        'joined_rooms': joined_rooms,
        'available_rooms': available_rooms,
        "creator": creator,
    }
    return render(request, "chat/room.html",context)



def register(request):
    if request.method == 'POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            form.save()
            
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.capitalize()}: {error}")
    else:
        form = NewUserForm()
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                # Redirect to a success page or do something else
                return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})


@login_required
def exit_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    if request.user.is_authenticated:
        room.users.remove(request.user)
    return redirect('index')




def delete_message(request, message_id):
    message = get_object_or_404(Message, id=message_id)
    if message.sender == request.user and message.is_deletable():
        message.delete()
    return redirect('room', room_name=message.room.name)


def update_message(request, message_id):
    message = get_object_or_404(Message, id=message_id)
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message.content = form.cleaned_data['content']
            message.save()
            return redirect('room', room_name=message.room.name)
    else:
        form = MessageForm(initial={'content': message.content})
    return render(request, 'chat/update_message.html', {'form': form, 'message': message})


def logout_view(request):
    logout(request)
    return redirect('login_') 


def Reported(request, id):
    message = get_object_or_404(Message, id=id)
    if not message.reported:
        message.reported = True
        message.content = 'Content is removed because it has been reported.'
        message.save()
    return redirect('room', room_name=message.room.name)



