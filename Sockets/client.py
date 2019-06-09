#!/usr/bin/python

import sys
import socket
import curses
from curses import KEY_RIGHT, KEY_LEFT, KEY_UP, KEY_DOWN
from time import sleep


HOST = '127.0.0.9'     # Endereco IP do Servidor
PORT = 5000            # Porta que o Servidor esta

if (len(sys.argv) == 2):
	HOST = sys.argv[1]
if (len(sys.argv) == 3):
	PORT = sys.argv[2]

tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
dest = (HOST, PORT)
tcp.connect(dest)


#print 'Para sair use CTRL+X\n'
#msg = raw_input()
# while msg <> '\x18':
#     tcp.send (msg)
#     msg = raw_input()
#     x = tcp.recv(1024)
#     print x

curses.initscr()
win = curses.newwin(20, 60, 0, 0)
win.keypad(1)
curses.noecho()
#curses.curs_set(0)
#win.border(0)
#win.nodelay(1)

while True:
    event = win.getch()
    print event


    tcp.send(str(event))



tcp.close()