from telnetlib import STATUS
from django.shortcuts import render
from .models import checkRoomExist, checkRoomInfo, createValidRoom
from django.http import HttpResponse

# Create your views here.


def createroom(request, roomid, roompsw):
    if(checkRoomExist(roomid)):
        return HttpResponse('Room Exist', status=403)
    if(checkRoomInfo(roomid, roompsw) == False):
        return HttpResponse('Invalid RoomID or RoomPassword', status=403)
    return createValidRoom(roomid, roompsw)


def testdjango(request):
    return HttpResponse('It worked', status=201)
