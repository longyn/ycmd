# Copyright (C) 2016 ycmd contributors
#
# This file is part of ycmd.
#
# ycmd is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# ycmd is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with ycmd.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from future import standard_library
standard_library.install_aliases()
from builtins import *  # noqa

from hamcrest import assert_that, matches_regexp

from ycmd.tests.python import IsolatedYcmd, SharedYcmd
from ycmd.tests.test_utils import BuildRequest, StopCompleterServer, UserOption


@SharedYcmd
def DebugInfo_ServerIsRunning_test( app ):
  request_data = BuildRequest( filetype = 'python' )
  assert_that(
    app.post_json( '/debug_info', request_data ).json,
    matches_regexp( 'Python completer debug information:\n'
                    '  JediHTTP running at: http://127.0.0.1:\d+\n'
                    '  JediHTTP process ID: \d+\n'
                    '  JediHTTP executable: .+\n'
                    '  JediHTTP logfiles:\n'
                    '    .+\n'
                    '    .+\n'
                    '  Python interpreter: .+' ) )


@IsolatedYcmd
def DebugInfo_ServerIsNotRunning_LogfilesExist_test( app ):
  with UserOption( 'server_keep_logfiles', True ):
    StopCompleterServer( app, 'python' )
    request_data = BuildRequest( filetype = 'python' )
    assert_that(
      app.post_json( '/debug_info', request_data ).json,
      matches_regexp( 'Python completer debug information:\n'
                      '  JediHTTP no longer running\n'
                      '  JediHTTP executable: .+\n'
                      '  JediHTTP logfiles:\n'
                      '    .+\n'
                      '    .+\n'
                      '  Python interpreter: .+' ) )


@IsolatedYcmd
def DebugInfo_ServerIsNotRunning_LogfilesDoNotExist_test( app ):
  with UserOption( 'server_keep_logfiles', False ):
    StopCompleterServer( app, 'python' )
    request_data = BuildRequest( filetype = 'python' )
    assert_that(
      app.post_json( '/debug_info', request_data ).json,
      matches_regexp( 'Python completer debug information:\n'
                      '  JediHTTP is not running\n'
                      '  JediHTTP executable: .+\n'
                      '  Python interpreter: .+' ) )
