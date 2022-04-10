from pyexpat import model
from unittest import result
from django.db import models
from django.http import HttpResponse

# Create your models here.


class Room(models.Model):
    roomid = models.CharField(max_length=6)
    roomstatus = models.CharField(max_length=7)  # waiting / started
    messagecount = models.IntegerField()
    roomfurtherstatus = models.CharField(
        max_length=7)  # normal / build / quest
    questcount = models.IntegerField()
    # Team Building Proposal / Quest#n Proposal
    votetitle = models.CharField(max_length=22)
    votecontent = models.CharField(max_length=200)
    teammembercount = models.IntegerField()
    teammembercountnow = models.IntegerField()
    teambuilder = models.CharField(max_length=7)


class User(models.Model):
    roomid = models.CharField(max_length=6)
    userid = models.CharField(max_length=7)
    userpsw = models.CharField(max_length=6)
    role = models.CharField(max_length=23)
    onvote = models.BooleanField()
    voted = models.BooleanField()
    result = models.BooleanField()


class Message(models.Model):
    roomid = models.CharField(max_length=6)
    messageid = models.IntegerField()
    messagetitle = models.CharField(max_length=25)  # Title
    messageusers = models.CharField(max_length=200)  # users
    message1users = models.CharField(max_length=200)  # Agree
    message2users = models.CharField(max_length=200)  # Disagree


def checkRoomExist(Roomid):
    return Room.objects.filter(roomid=Roomid).exists()


def createValidRoom(Roomid):
    Room.objects.create(roomid=Roomid, roomstatus='waiting',
                        messagecount=0, roomfurtherstatus='normal', questcount=0, votetitle='', votecontent='', teammembercount=0, teammembercountnow=0, teambuilder='')
    return HttpResponse('createdRoom', status=201)


def checkUserExist(Roomid, Userid):
    return User.objects.filter(roomid=Roomid, userid=Userid).exists()


def checkUserValid(Roomid, Userid, Userpsw):
    return User.objects.filter(roomid=Roomid, userid=Userid, userpsw=Userpsw).exists()


def createValidUser(Roomid, Userid, Userpsw):
    User.objects.create(roomid=Roomid, userid=Userid,
                        userpsw=Userpsw, role='not distrubuted', onvote=False, voted=False, result=False)
    return HttpResponse('createdUser', status=201)


def getRoomUser(Roomid):
    Users = User.objects.filter(roomid=Roomid)
    response = {'userCount': len(Users)}
    useri = 0
    for user in Users:
        useri += 1
        response[f'user{useri}'] = user.userid
    return response


def getRoomStatus(Roomid):
    return Room.objects.get(roomid=Roomid).roomstatus
