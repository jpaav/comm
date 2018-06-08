from django.shortcuts import render

from rooms.models import Room


def room(request, room_id):
	room = Room.objects.filter(pk=room_id)
	return render(request, 'rooms/room.html')
