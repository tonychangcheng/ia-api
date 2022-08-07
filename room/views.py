# Copyright (C) 2022 Zijun Yang <zijun.yang@outlook.com>
#
# This file is part of God of Avalon Backend.
#
# God of Avalon Backend is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# God of Avalon Backend is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with God of Avalon Backend.  If not, see <http://www.gnu.org/licenses/>.


import json
import random
from unittest import result
from django import http
from django.shortcuts import render
from .models import Room, checkRoomExist, createValidRoom
from .models import User, checkUserExist, checkUserValid, createValidUser
from .models import getRoomUser, getRoomStatus, Message
from django.http import HttpResponse, JsonResponse
from django.middleware.csrf import get_token

# Create your views here.


def get_csrf_token(request):
    csrf_token = get_token(request)
    return JsonResponse({'token': csrf_token})


def createroom(request, roomid):
    if(checkRoomExist(roomid)):
        return HttpResponse('Room Exist')
    return createValidRoom(roomid)


def checkString(string):
    res = {
        'number': False,
        'lowLetter': False,
        'upLetter': False,
        'underline': False,
        'otherChar': False,
        'length': 0
    }
    res['length'] = len(string)
    for letter in string:
        if('0' <= letter and letter <= '9'):
            res['number'] = True
        elif('a' <= letter and letter <= 'z'):
            res['lowLetter'] = True
        elif('A' <= letter and letter <= 'Z'):
            res['upLetter'] = True
        elif('-' == letter):
            res['underline'] = True
        else:
            res['otherChar'] = True
    return res


def joinroom(request, roomid, userid, userpsw):
    if(not checkRoomExist(roomid)):
        return HttpResponse('Room Does Not Exist')
    if(checkUserExist(roomid, userid)):
        if(checkUserValid(roomid, userid, userpsw)):
            return HttpResponse('userExistAndValid')
        else:
            return HttpResponse('Wrong Password')
    else:
        if(Room.objects.get(roomid=roomid).roomstatus != 'waiting'):
            return HttpResponse('Room Already Started')
        else:
            return createValidUser(roomid, userid, userpsw)


def roomstatus(request, roomid):
    if(checkRoomExist(roomid)):
        return HttpResponse(getRoomStatus(roomid))
    else:
        return HttpResponse('Room Does Not Exist')


def getWaitingRoomInfo(request, roomid, userid, userpsw):
    if(checkUserValid(roomid, userid, userpsw)):
        return HttpResponse(json.dumps(getRoomUser(roomid)))
    else:
        return HttpResponse('userNotValid')


def testdjango(request):
    data = json.loads(request.body)
    res = data['data1']
    return HttpResponse(res)


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
        return HttpResponse('Room Does Not Exist')
    if(not checkUserValid(roomid, userid, userpsw)):
        return HttpResponse('User Not Valid')
    if(Room.objects.get(roomid=roomid).roomstatus == 'started'):
        return HttpResponse('Room Already Started')

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


def userrole(request, roomid, userid, userpsw):
    if(not checkRoomExist(roomid)):
        return HttpResponse('Room Does Not Exist')
    if(not checkUserValid(roomid, userid, userpsw)):
        return HttpResponse('User Not Valid')
    if(Room.objects.get(roomid=roomid).roomstatus != 'started'):
        return HttpResponse('Room Not Started')

    # return user's role
    return HttpResponse(User.objects.get(roomid=roomid, userid=userid, userpsw=userpsw).role)


def usersusersee(request, roomid, userid, userpsw):
    if(not checkRoomExist(roomid)):
        return HttpResponse('Room Does Not Exist')
    if(not checkUserValid(roomid, userid, userpsw)):
        return HttpResponse('User Not Valid')
    if(Room.objects.get(roomid=roomid).roomstatus != 'started'):
        return HttpResponse('Room Not Started')

    # return users that user can see
    userscount = 0
    response = {}
    thisuser = User.objects.get(roomid=roomid, userid=userid, userpsw=userpsw)
    for user in User.objects.filter(roomid=roomid):
        if(user.userid == thisuser.userid):
            continue
        flag = False
        ul = user.role
        tl = thisuser.role
        flag = flag or (tl == 'Merlin' and (
            ul == 'Morgana' or ul == 'Assassin' or ul == 'Minion of Mordred' or ul == 'Oberon'))
        flag = flag or (tl == 'Percival' and (
            ul == 'Merlin' or ul == 'Morgana'))
        flag = flag or ((tl == 'Assassin' or tl == 'Morgana' or tl ==
                        'Mordred' or tl == 'Minion of Mordred') and (ul == 'Assassin' or ul == 'Morgana' or ul ==
                        'Mordred' or ul == 'Minion of Mordred'))
        if(flag):
            userscount += 1
            response[f'user{userscount}'] = user.userid
    response['userCount'] = userscount
    return HttpResponse(json.dumps(response))


def message(request, roomid, userid, userpsw, messageid):
    if(not checkRoomExist(roomid)):
        return HttpResponse('Room Does Not Exist')
    if(not checkUserValid(roomid, userid, userpsw)):
        return HttpResponse('User Not Valid')
    if(Room.objects.get(roomid=roomid).roomstatus != 'started'):
        return HttpResponse('Room Not Started')
    if(not Message.objects.filter(roomid=roomid, messageid=messageid).exists()):
        return HttpResponse('Message Does Not Exist', status=404)
    thisroom = Room.objects.get(roomid=roomid)
    if(messageid > thisroom.messagecount):
        return HttpResponse('Message Does Not Exist', status=404)
    thismessage = Message.objects.get(roomid=roomid, messageid=messageid)
    response = {'messageid': thismessage.messageid, 'messagetitle': thismessage.messagetitle, 'messageusers': thismessage.messageusers,
                'message1users': thismessage.message1users, 'message2users': thismessage.message2users}
    return HttpResponse(json.dumps(response))


def messagecount(request, roomid):
    if(not checkRoomExist(roomid)):
        return HttpResponse('Room Does Not Exist')
    return HttpResponse(Room.objects.get(roomid=roomid).messagecount)


def allmessage(request, roomid, userid, userpsw):
    if(not checkRoomExist(roomid)):
        return HttpResponse('Room Does Not Exist')
    if(not checkUserValid(roomid, userid, userpsw)):
        return HttpResponse('User Not Valid')
    thisroom = Room.objects.get(roomid=roomid)
    messagecount = thisroom.messagecount
    messages = Message.objects.filter(roomid=roomid)

    res = {'messagecount': messagecount}
    count = 0
    for message in messages:
        count += 1
        res[f'messagetitle{count}'] = message.messagetitle
        res[f'messageusers{count}'] = message.messageusers
        res[f'message1users{count}'] = message.message1users
        res[f'message2users{count}'] = message.message2users
    return HttpResponse(json.dumps(res))


def buildteam(request, roomid, userid, userpsw, count):

    if(not checkRoomExist(roomid)):
        return HttpResponse('Room Does Not Exist')
    thisroom = Room.objects.get(roomid=roomid)
    if(not checkUserValid(roomid, userid, userpsw)):
        return HttpResponse('User Not Valid')
    if(thisroom.roomstatus != 'started'):
        return HttpResponse('Room Not Started')
    if(thisroom.roomfurtherstatus != 'normal'):
        return HttpResponse('A Vote is on Going')
    #thisroom.votetitle = 'Team Building Proposal'
    #thisroom.roomfurtherstatus = 'build'
    thisroom.teambuilder = userid
    for user in User.objects.filter(roomid=roomid):
        user.onvote = False
        user.save()
    thisroom.teammembercount = count
    thisroom.teammembercountnow = 0
    thisroom.votetitle = 'Team Building Proposal'
    thisroom.votecontent = f'Builder: {userid} | Team Members: '
    thisroom.save()
    return HttpResponse('Start Build Team', status=201)


def newbuildteam(request, roomid, userid, userpsw):
    if(not checkRoomExist(roomid)):
        return HttpResponse('Room Does Not Exist')
    thisroom = Room.objects.get(roomid=roomid)
    if(not checkUserValid(roomid, userid, userpsw)):
        return HttpResponse('User Not Valid')
    if(thisroom.roomstatus != 'started'):
        return HttpResponse('Room Not Started')
    if(thisroom.roomfurtherstatus != 'normal'):
        return HttpResponse('A Vote is on Going')
    da = json.loads(request.body)
    thisroom.teambuilder = userid
    for user in User.objects.filter(roomid=roomid):
        user.onvote = False
        user.save()
    thisroom.teammembercount = da['teammembercount']
    thisroom.teammembercountnow = 0
    thisroom.votetitle = 'Team Building Proposal'
    thisroom.votecontent = f'Builder: {userid} | Team Members: '
    for i in range(1, da['teammembercount']+1):
        memberid = da[f'teammember{i}']
        if(not checkUserExist(roomid, memberid)):
            return HttpResponse('Member Not Exists')
        thismember = User.objects.get(roomid=roomid, userid=memberid)
        thismember.onvote = True
        thisroom.teammembercountnow += 1
        thisroom.votecontent += memberid
        if(thisroom.teammembercount != thisroom.teammembercountnow):
            thisroom.votecontent += ', '
        thismember.save()
    thisroom.roomfurtherstatus = 'build'
    thisroom.save()
    startvote(roomid)
    return HttpResponse('Start Build Team', status=201)


def addteammember(request, roomid, userid, userpsw, memberid):

    if(not checkRoomExist(roomid)):
        return HttpResponse('Room Does Not Exist')
    thisroom = Room.objects.get(roomid=roomid)
    if(not checkUserValid(roomid, userid, userpsw)):
        return HttpResponse('User Not Valid')
    if(thisroom.roomstatus != 'started'):
        return HttpResponse('Room Not Started')
    if(thisroom.roomfurtherstatus != 'normal'):
        return HttpResponse('A Vote is on Going')
    if(userid != thisroom.teambuilder):
        return HttpResponse('You are not team builder')

    thismember = User.objects.get(roomid=roomid, userid=memberid)
    if(thismember.onvote == False):
        thismember.onvote = True
        thisroom.teammembercountnow += 1
        thisroom.votecontent += memberid
        if(thisroom.teammembercount != thisroom.teammembercountnow):
            thisroom.votecontent += ', '
        else:
            thisroom.roomfurtherstatus = 'build'
            startvote(roomid)
    thisroom.save()
    thismember.save()
    return HttpResponse(thisroom.teammembercountnow, status=201)


def startvote(roomid):
    for user in User.objects.filter(roomid=roomid):
        user.voted = False
        user.save()


def allroominfo(request, roomid, userid, userpsw):
    if(not checkRoomExist(roomid)):
        return HttpResponse('Room Does Not Exist')
    thisroom = Room.objects.get(roomid=roomid)
    if(not checkUserValid(roomid, userid, userpsw)):
        return HttpResponse('User Not Valid')
    thisuser = User.objects.get(roomid=roomid, userid=userid, userpsw=userpsw)
    if(thisroom.roomstatus != 'started'):
        return HttpResponse('Room Not Started')
    res = {'roomfurtherstatus': thisroom.roomfurtherstatus}
    # normal
    if(res['roomfurtherstatus'] == 'normal'):
        return HttpResponse(json.dumps(res))
    # build
    if(res['roomfurtherstatus'] == 'build'):
        res['votetitle'] = thisroom.votetitle
        res['votecontent'] = thisroom.votecontent
        res['voted'] = thisuser.voted
        return HttpResponse(json.dumps(res))
    # quest
    if(res['roomfurtherstatus'] == 'quest'):
        res['votetitle'] = thisroom.votetitle
        res['votecontent'] = thisroom.votecontent
        res['onvote'] = thisuser.onvote
        res['voted'] = thisuser.voted
        return HttpResponse(json.dumps(res))


def anybuild(request, roomid, userid, userpsw):
    if(not checkRoomExist(roomid)):
        return HttpResponse('Room Does Not Exist')
    thisroom = Room.objects.get(roomid=roomid)
    if(not checkUserValid(roomid, userid, userpsw)):
        return HttpResponse('User Not Valid')
    if(thisroom.roomstatus != 'started'):
        return HttpResponse('Room Not Started')
    return HttpResponse(thisroom.roomfurtherstatus == 'build')


def votecontent(request, roomid, userid, userpsw):
    if(not checkRoomExist(roomid)):
        return HttpResponse('Room Does Not Exist')
    thisroom = Room.objects.get(roomid=roomid)
    if(not checkUserValid(roomid, userid, userpsw)):
        return HttpResponse('User Not Valid')
    if(thisroom.roomstatus != 'started'):
        return HttpResponse('Room Not Started')
    if(thisroom.roomfurtherstatus == 'normal'):
        return HttpResponse('No Vote is on Going')
    return HttpResponse(thisroom.votecontent)


def anyquest(request, roomid, userid, userpsw):
    if(not checkRoomExist(roomid)):
        return HttpResponse('Room Does Not Exist')
    thisroom = Room.objects.get(roomid=roomid)
    if(not checkUserValid(roomid, userid, userpsw)):
        return HttpResponse('User Not Valid')
    if(thisroom.roomstatus != 'started'):
        return HttpResponse('Room Not Started')
    # return HttpResponse(thisroom.roomfurtherstatus == 'quest' and User.objects.get(roomid=roomid, userid=userid, userpsw=userpsw).onvote, status=201)
    return HttpResponse(thisroom.roomfurtherstatus == 'quest')


def vote(request, roomid, userid, userpsw, choice):
    if(not checkRoomExist(roomid)):
        return HttpResponse('Room Does Not Exist')
    thisroom = Room.objects.get(roomid=roomid)
    if(not checkUserValid(roomid, userid, userpsw)):
        return HttpResponse('User Not Valid')
    if(thisroom.roomstatus != 'started'):
        return HttpResponse('Room Not Started')
    if(thisroom.roomfurtherstatus == 'normal'):
        return HttpResponse('No Vote is on Going')
    thisuser = User.objects.get(roomid=roomid, userid=userid, userpsw=userpsw)
    if(thisuser.voted == True):
        return HttpResponse('Already Voted')
    thisuser.voted = True
    thisuser.result = choice == 'yes'
    thisuser.save()

    #
    if(thisroom.roomfurtherstatus == 'build'):
        votedusercount = len(User.objects.filter(roomid=roomid, voted=True))
    else:
        votedusercount = len(User.objects.filter(
            roomid=roomid, voted=True, onvote=True))
    # build->quest?
    if(thisroom.roomfurtherstatus == 'build' and votedusercount == len(User.objects.filter(roomid=roomid))):

        # message.messageusers
        totalcount = len(User.objects.filter(roomid=roomid, onvote=True))
        messageusers = ''
        count = 0
        for user in User.objects.filter(roomid=roomid, onvote=True):
            count += 1
            messageusers += user.userid
            if(count < totalcount):
                messageusers += ', '

        # message.message1users
        agree = len(User.objects.filter(
            roomid=roomid, voted=True, result=True))
        agreeuser = f'{agree} Yes: '
        count = 0
        for user in User.objects.filter(roomid=roomid, voted=True, result=True):
            count += 1
            agreeuser += user.userid
            if(count < agree):
                agreeuser += ', '

        # message.message2users
        disagree = len(User.objects.filter(
            roomid=roomid, voted=True, result=False))
        disagreeuser = f'{disagree} No: '
        count = 0
        for user in User.objects.filter(roomid=roomid, voted=True, result=False):
            count += 1
            disagreeuser += user.userid
            if(count < disagree):
                disagreeuser += ', '
        Message.objects.create(roomid=roomid, messageid=thisroom.messagecount+1,
                               messagetitle=f'Team Building Proposal#{thisroom.messagecount-thisroom.questcount+1}', messageusers=messageusers, message1users=agreeuser, message2users=disagreeuser)
        thisroom.messagecount += 1
        if(agree > disagree):
            thisroom.questcount += 1
            thisroom.roomfurtherstatus = 'quest'
            thisroom.votetitle = f'Quest#{thisroom.questcount}'
            startvote(roomid)
        else:
            thisroom.roomfurtherstatus = 'normal'
        thisroom.save()
    # quest->over?
    if(thisroom.roomfurtherstatus == 'quest' and votedusercount == len(User.objects.filter(roomid=roomid, onvote=True))):

        # message.messageusers
        totalcount = len(User.objects.filter(
            roomid=roomid, voted=True, onvote=True))
        messageusers = ''
        count = 0
        for user in User.objects.filter(roomid=roomid, voted=True, onvote=True):
            count += 1
            messageusers += user.userid
            if(count < totalcount):
                messageusers += ', '

        agree = len(User.objects.filter(roomid=roomid,
                    voted=True, onvote=True, result=True))
        disagree = len(User.objects.filter(
            roomid=roomid, voted=True, onvote=True, result=False))
        Message.objects.create(roomid=roomid, messageid=thisroom.messagecount+1,
                               messagetitle=f'Quest#{thisroom.questcount}', messageusers=messageusers, message1users=f'{agree} Yes', message2users=f'{disagree} No')
        thisroom.messagecount += 1
        thisroom.roomfurtherstatus = 'normal'
        thisroom.save()
    return HttpResponse('Successfully Vote', status=201)


def voted(request, roomid, userid, userpsw):
    if(not checkRoomExist(roomid)):
        return HttpResponse('Room Does Not Exist')
    thisroom = Room.objects.get(roomid=roomid)
    if(not checkUserValid(roomid, userid, userpsw)):
        return HttpResponse('User Not Valid')
    if(thisroom.roomstatus != 'started'):
        return HttpResponse('Room Not Started')
    if(thisroom.roomfurtherstatus == 'normal'):
        return HttpResponse('No Vote is on Going')
    thisuser = User.objects.get(roomid=roomid, userid=userid, userpsw=userpsw)

    return HttpResponse(thisuser.voted or (thisroom.roomfurtherstatus == 'quest' and thisuser.onvote == False))
