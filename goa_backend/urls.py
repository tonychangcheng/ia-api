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
from room.views import addteammember, anybuild, votecontent, anyquest

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
    path('messagecount/<str:roomid>/', messagecount),
    path('message/<str:roomid>/<str:userid>/<str:userpsw>/<int:messageid>/', message),
    path('buildteam/<str:roomid>/<str:userid>/<str:userpsw>/<int:count>/', buildteam),
    path('addteammember/<str:roomid>/<str:userid>/<str:userpsw>/<str:memberid>/', addteammember),
    path('anybuild/<str:roomid>/<str:userid>/<str:userpsw>/', anybuild),
    path('votecontent/<str:roomid>/<str:userid>/<str:userpsw>/', votecontent),
    path('anyquest/<str:roomid>/<str:userid>/<str:userpsw>/', anyquest)
]
