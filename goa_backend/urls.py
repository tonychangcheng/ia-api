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

"""goa_backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from room.views import createroom, joinroom, getWaitingRoomInfo, roomstatus, testdjango
from room.views import startGame, userrole, usersusersee, message, messagecount, buildteam
from room.views import addteammember, anybuild, votecontent, anyquest, vote, voted
from room.views import get_csrf_token, allmessage, allroominfo, newbuildteam

urlpatterns = [
    path('admin/', admin.site.urls),
    path('test/', testdjango),
    path('create/<str:roomid>/', createroom),
    path('join/<str:roomid>/<str:userid>/<str:userpsw>/', joinroom),
    path('wait/<str:roomid>/<str:userid>/<str:userpsw>/', getWaitingRoomInfo),
    path('status/<str:roomid>/', roomstatus),
    path('start/<str:roomid>/<str:userid>/<str:userpsw>/', startGame),
    path('userrole/<str:roomid>/<str:userid>/<str:userpsw>/', userrole),
    path('usersusersee/<str:roomid>/<str:userid>/<str:userpsw>/', usersusersee),
    #path('messagecount/<str:roomid>/', messagecount),
    #path('message/<str:roomid>/<str:userid>/<str:userpsw>/<int:messageid>/', message),
    path('allmessage/<str:roomid>/<str:userid>/<str:userpsw>/', allmessage),
    #path('buildteam/<str:roomid>/<str:userid>/<str:userpsw>/<int:count>/', buildteam),
    #path('addteammember/<str:roomid>/<str:userid>/<str:userpsw>/<str:memberid>/', addteammember),
    path('newbuildteam/<str:roomid>/<str:userid>/<str:userpsw>/', newbuildteam),
    #path('anybuild/<str:roomid>/<str:userid>/<str:userpsw>/', anybuild),
    #path('votecontent/<str:roomid>/<str:userid>/<str:userpsw>/', votecontent),
    #path('anyquest/<str:roomid>/<str:userid>/<str:userpsw>/', anyquest),
    path('vote/<str:roomid>/<str:userid>/<str:userpsw>/<str:choice>/', vote),
    #path('voted/<str:roomid>/<str:userid>/<str:userpsw>/', voted),
    path('get_csrf_token/', get_csrf_token),
    path('allroominfo/<str:roomid>/<str:userid>/<str:userpsw>/', allroominfo)
]
