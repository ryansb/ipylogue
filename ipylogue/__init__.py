#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2014 Ryan Brown <sb@ryansb.com>
#
# This file is part of pitted.
#
# pitted is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

'''Pitted

Backs the IPython notebook system with git.
'''

__title__ = 'pitted'
__version__ = '0.1.0'
__ref__ = 0x000000
__author__ = 'Ryan Brown'
__license__ = 'AGPLv3'
__copyright__ = 'Copyright 2014 Ryan Brown'

from .gitmanager import GitNotebookManager
