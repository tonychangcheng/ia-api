from statistics import mode
from telnetlib import STATUS
from django.db import models
from django.http import HttpResponse

# Create your models here.


class Room(models.Model):
    roomid = models.CharField(max_length=6)


class User(models.Model):
    roomid = models.CharField(max_length=6)
    userid = models.CharField(max_length=6)
    userpsw = models.CharField(max_length=6)


def checkRoomExist(Roomid):
    return Room.objects.filter(roomid=Roomid).exists()


def createValidRoom(Roomid):
    Room.objects.create(roomid=Roomid)
    return HttpResponse('createdRoom', status=201)


def checkUserExist(Roomid, Userid):
    return User.objects.filter(roomid=Roomid, userid=Userid).exists()


def checkUserValid(Roomid, Userid, Userpsw):
    return User.objects.filter(roomid=Roomid, userid=Userid, userpsw=Userpsw).exists()


def createValidUser(Roomid, Userid, Userpsw):
    return HttpResponse('createdUser', status=201)
