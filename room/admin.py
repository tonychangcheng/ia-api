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

from django.contrib import admin

# Register your models here.

from .models import Message, Room, User


# Admin view for Room model
@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ("roomid", "messagecount", "createdate")


# Admin view for User model
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("roomid", "userid", "role", "userpsw")


# Register Message model if you need to manage it in the admin as well
@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("roomid", "messageid", "messagetitle")  # You can customize fields here
