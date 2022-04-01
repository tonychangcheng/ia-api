import json
from django.shortcuts import render
from .models import checkRoomExist, createValidRoom
from .models import checkUserExist, checkUserValid, createValidUser
from .models import getRoomUser
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
        if(checkUserValid(roomid, userid, userpsw)):
            return HttpResponse('userExistAndValid', status=201)
        else:
            return HttpResponse('Wrong Password', status=201)
    else:
        return createValidUser(roomid, userid, userpsw)


def getWaitingRoomInfo(request, roomid, userid, userpsw):
    if(checkUserValid(roomid, userid, userpsw)):
        return HttpResponse(json.dumps(getRoomUser(roomid)), status=201)
    else:
        return HttpResponse('userNotValid', status=201)


def testdjango(request):
    return HttpResponse('It worked', status=201)
