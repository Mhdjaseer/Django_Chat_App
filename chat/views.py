from django.shortcuts import render,redirect
from .forms import NewUserForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate,login
from .models import Room


# Create your views here.
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages
from .models import Room


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
        'available_rooms': available_rooms
    }
    return render(request, "chat/index.html", context)

def room(request, room_name):
    room = get_object_or_404(Room, name=room_name)
    username=request.user.username
    messages = room.messages.all()
    
    context={
        "room_name": room_name,
        "messages": messages,
        "username":username,
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



def exit_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    if request.user.is_authenticated:
        room.users.remove(request.user)
    return redirect('index')