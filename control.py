"""
PiFMRadio control command.
Copyright 2009 Labkaxita

This file is part of pifmradio.

pifmradio is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.

pifmradio is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE.  See the GNU Affero General Public License for
more details.

You should have received a copy of the GNU General Public License along with
pifmradio. If not, see <http://www.gnu.org/licenses/>.
"""
from socket import socket
import json
from cmd import Cmd
import sys


class Controller(Cmd):
    """
    PiFMRadio controller.

    This command controls the PiFMRadio daemon.
    """

    intro = 'PiFMRadio controller'
    prompt = 'command: '

    def send_command_to_controller(self, **kwargs):
        sock = socket()
        sock.send(json.dumps(kwargs))
        response = ''
        while self.recv(512):
            response += response
        json.loads(response)

    def do_start(self, arg):
        "Starts the emission"
        self.send_command_to_controller(command='start')

    def do_stop(self, arg):
        "Stops the emission"
        self.send_command_to_controller(command='stop')

    def do_info(self, arg):
        "Gather server information"
        self.send_command_to_controller(command='info')

    def do_sintonize(self, freq):
        "Change the emitting frequency, pass the new frequency as argument"
        if not freq:
            freq = raw_input('Which frequency? ')
        self.send_command_to_controller(command='sintonize', freq=freq)

    def do_exit(self, arg):
        "Exit session"
        self.send_command_to_controller(command='exit')
        sys.exit()

    def do_quit(self, arg):
        "Terminate the emission and the control daemon"
        self.send_command_to_controller(command='quit')
        sys.exit()

c = Controller()
c.cmdloop()
