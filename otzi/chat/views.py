from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User

def index(request):
    return render(request, 'chat/index.html', {})

def room(request, room_name, user_name="Undefined"):
    template = 'chat/room.html'   
    ids = room_name.split("_")
    context = {
        'user_conn' : get_object_or_404(User, id=int(ids[0])) if request.user.id != int(ids[0]) else get_object_or_404(User, id=int(ids[1])),
        'room_name' : room_name,
    }    
    return render(request, template, context)