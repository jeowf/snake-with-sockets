#!/usr/bin/python

import sys
import socket
import curses
from curses import KEY_RIGHT, KEY_LEFT, KEY_UP, KEY_DOWN
from time import sleep

from random import randint


import thread


HOST = '127.0.0.9'     # Endereco IP do Servidor
PORT = 5000            # Porta que o Servidor esta
IA = False

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
win = curses.newwin(30, 70, 0, 0)
win.keypad(1)
curses.noecho()
curses.curs_set(0)
#win.border(0)
#win.nodelay(1)

out_str = ' '

def print_map():
	global tcp
	global win
	global out_str

	while True:

		out_str = tcp.recv(4096)
    	#win.addstr(0, 0, out_str)
    	#x = out_str
    	#win.addstr(0, 0, x)

def send_input():
	global win
	global tcp

	while True:
		if (IA):
			r = randint(258, 261)
			tcp.send(str(r))
		else:
		    event = win.getch()
		    tcp.send(str(event))
		sleep(0.15)




#thread.start_new_thread(send_input, tuple([]))

win.addstr(0,0,'Digite:\n M: Manual\n A: Automatico')
res = win.getch()
if (res == ord('A') or res == ord('a')):
	IA = True

thread.start_new_thread(print_map, tuple([]) )
thread.start_new_thread(send_input, tuple([]) )

#print_map()
while True:
	
	#win.addstr(0, 0, out_str)
	pass
    #a = 1

tcp.close()
