from statistics import mode
from django.db import models

# Create your models here.


class Room(models.Model):
    roomid = models.CharField(max_length=6)
    roompsw = models.CharField(max_length=6)


def checkRoomExist(Roomid):
    if(Room.objects.filter(roomid=Roomid).exists):
        return True
    return False


def checkRoomInfo(roomid, roompsw):
    pass


def createValidRoom(Roomid, Roompsw):
    Room.objects.create(roomid=Roomid, roompsw=Roompsw)
