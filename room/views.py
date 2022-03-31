from django.shortcuts import render
from .models import checkRoomExist, checkRoomInfo, createValidRoom
from .models import checkUserExist, checkUserValid, createValidUser
from django.http import HttpResponse

# Create your views here.


def createroom(request, roomid):
    if(checkRoomExist(roomid)):
        return HttpResponse('Room Exist', status=201)
    return createValidRoom(roomid)


def joinroom(request, roomid, userid, userpsw):
    if(not checkRoomExist(roomid)):
        return HttpResponse('Room Does Not Exist', status=201)
    if(checkUserExist(roomid, userid)):
        if(not checkUserValid(roomid, userid, userpsw)):
            return HttpResponse('Wrong Password', status=201)
        else:
            pass
    else:
        return createValidUser(roomid, userid, userpsw)


def testdjango(request):
    return HttpResponse('It worked', status=201)
