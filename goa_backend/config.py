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

config = {
    # whether show debug info or not
    'DEBUG': True,
    # a django secret key, can be generated from  https://djecrety.ir/
    'SECRET_KEY': '&el+tpq6nk9=z^ux5jqlrxc!xwn5y#lycodv-(y3_l%9$v&5nr',
    # url where the backend is deployed
    'BACKEND_URLs': [
        # '127.0.0.1',
        'ia-api-qmw9.onrender.com'
    ],
    # url where the frontend is deployed
    'FRONTEND_URLs': [
        # 'http://localhost:8080',
        'https://ia-mcsc8090.onrender.com'
    ]
}
