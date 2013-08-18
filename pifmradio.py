"""
PiFMRadio, a FM radio stream for Raspberry pi.
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
from subprocess import Popen, PIPE
from multiprocessing import Process
import json

freq = "107.4"

PIFMPORT = 8000
CONTROLPORT = 8080


def pifm(freq):
    s = socket()
    s.bind(('0.0.0.0', PIFMPORT))
    s.listen(0)
    while 1:
        conn, addr = s.accept()
        p = Popen(["./pifm", "-", freq], bufsize=2048, stdin=PIPE)
        while 1:
            data = conn.recv(16)
            if not data:
                break
            p.stdin.write(data)
            p.stdin.flush()
        conn.close()
        p.terminate()


class Radio(object):
    def __init__(self, freq):
        self.freq = freq
        self.proc = Process(target=pifm, args=(self.freq,))
        self.running = False

    def start(self):
        if self.proc.is_alive():
            retval = 'ERROR'
        else:
            self.proc.start()
            retval = 'OK'
        return retval

    def stop(self):
        if not self.proc.is_alive():
            retval = 'ERROR'
        else:
            self.proc.terminate()
            self.proc = Process(target=pifm, args=(self.freq,))
            retval = 'OK'
        return retval

    def main(self):
        self.control_socket = socket()
        self.control_socket.bind(('0.0.0.0', CONTROLPORT))
        self.control_socket.listen(0)
        self.running = True
        while self.running:
            conn, addr = self.control_socket.accept()
            self.conn_open = True
            while self.conn_open:
                data = conn.recv(512)
                if not data:
                    break
                data_dict = json.loads(data)
                if 'command' in data_dict:
                    response = {}
                    if data_dict['command'] == 'info':
                        retval = 'OK'
                        response['status'] = self.proc.is_alive()
                        response['freq'] = self.freq
                    elif data_dict['command'] == 'stop':
                        retval = self.stop()
                    elif data_dict['command'] == 'start':
                        retval = self.start()
                    elif data_dict['command'] == 'sintonize':
                        self.freq = data_dict['freq']
                        self.stop()
                        retval = self.start()
                    elif data_dict['command'] == 'exit':
                        self.conn_open = False
                        retval = 'OK'
                    elif data_dict['command'] == 'quit':
                        self.conn_open = False
                        self.quit()
                        retval = 'OK'
                    response['retval'] = retval
                    conn.send(json.dumps(response))
            conn.close()
        self.control_socket.close()

    def quit(self):
        self.running = False

if __name__ == '__main__':
    ra = Radio(freq)
    ra.main()
