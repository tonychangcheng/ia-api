import json
import random
from tabnanny import check
from django import http
from django.shortcuts import render
from .models import Room, checkRoomExist, createValidRoom
from .models import User, checkUserExist, checkUserValid, createValidUser
from .models import getRoomUser, getRoomStatus
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


def roomstatus(request, roomid):
    if(checkRoomExist(roomid)):
        return HttpResponse(getRoomStatus(roomid), status=201)
    else:
        return HttpResponse('Room Does Not Exist', status=201)


def getWaitingRoomInfo(request, roomid, userid, userpsw):
    if(checkUserValid(roomid, userid, userpsw)):
        return HttpResponse(json.dumps(getRoomUser(roomid)), status=201)
    else:
        return HttpResponse('userNotValid', status=201)


def testdjango(request):
    return HttpResponse('It worked', status=201)


character = ['Merlin', 'Percival', 'Morgana',
             'Assassin', 'Loyal Servant of Arther', 'Oberon', 'Mordred', 'Minion of Mordred']
'''
                                                    0 Merlin
                                                    1 Percival
                                                    2 Morgana
                                                    3 Assassin
                                                    4 Loyal Servant of Arther
                                                    5 Oberon
                                                    6 Mordred
                                                    7 Minion of Mordred
'''

template = ['', '', '', '', '', [5, 0, 1, 2, 3, 4],
            [6, 0, 1, 2, 3, 4, 4], [7, 0, 1, 2, 3, 4, 4, 5], [8, 0, 1, 2, 3, 4, 4, 4, 6], [9, 0, 1, 2, 3, 6, 4, 4, 4, 4], [10, 0, 1, 2, 3, 6, 4, 4, 4, 4, 7]]


def startGame(request, roomid, userid, userpsw):
    if(not checkRoomExist(roomid)):
        return HttpResponse('Room Does Not Exist', status=201)
    if(not checkUserValid(roomid, userid, userpsw)):
        return HttpResponse('User Not Valid', status=201)
    if(Room.objects.get(roomid=roomid).roomstatus == 'started'):
        return HttpResponse('Room Already Started', status=201)

    # generate role
    userNumInRomm = len(User.objects.filter(roomid=roomid))
    distrubuter = template[userNumInRomm]
    for i in range(5000):
        t1, t2 = random.randint(
            1, userNumInRomm), random.randint(1, userNumInRomm)
        t3 = distrubuter[t1]
        distrubuter[t1] = distrubuter[t2]
        distrubuter[t2] = t3
    i = 0
    for user in User.objects.filter(roomid=roomid):
        i += 1
        user.role = character[distrubuter[i]]
        user.save()
    thisRoom = Room.objects.get(roomid=roomid)
    thisRoom.roomstatus = 'started'
    thisRoom.save()
    return HttpResponse('Game Started', status=201)
