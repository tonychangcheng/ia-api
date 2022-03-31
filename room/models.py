from statistics import mode
from telnetlib import STATUS
from django.db import models
from django.http import HttpResponse

# Create your models here.


class Room(models.Model):
    roomid = models.CharField(max_length=6)
    roompsw = models.CharField(max_length=6)


def checkRoomExist(Roomid):
    if(Room.objects.filter(roomid=Roomid).exists):
        return True
    return False


def checkRoomInfo(Roomid, Roompsw):
    pass
    return True


def createValidRoom(Roomid, Roompsw):
    Room.objects.create(roomid=Roomid, roompsw=Roompsw)
    return HttpResponse('created', status=201)
