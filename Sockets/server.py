#!/usr/bin/python

import sys
import socket
import thread

import time

import curses
from curses import KEY_RIGHT, KEY_LEFT, KEY_UP, KEY_DOWN
from random import randint


commands = [KEY_RIGHT, KEY_RIGHT]
outstr = ''

snake1 = []
snake2 = []

def process(clients):
    global commands
    global outstr

    w, h = 60, 20;
    board = [[0 for x in range(w)] for y in range(h)];
    # curses.initscr()
    # win = curses.newwin(20, 60, 0, 0)
    # win.keypad(1)
    # curses.noecho()
    # curses.curs_set(0)
    # win.border(0)
    # win.nodelay(1)

    score = 0

    snake = [[4,10], [4,9], [4,8]]                                     # Initial snake co-ordinates
    snake = [[4,10], [4,9], [4,8]]                                     
    
    food = [10,20]                                                     # First food co-ordinates

    # win.addch(food[0], food[1], '*')                                   # Prints the food

    key = KEY_RIGHT

    while key != 27:                                                   # While Esc key is not pressed

        key = commands[0]

        # Calculates the new coordinates of the head of the snake. NOTE: len(snake) increases.
        # This is taken care of later at [1].
        snake.insert(0, [snake[0][0] + (key == KEY_DOWN and 1) + (key == KEY_UP and -1), snake[0][1] + (key == KEY_LEFT and -1) + (key == KEY_RIGHT and 1)])

        # If snake crosses the boundaries, make it enter from the other side
        #if snake[0][0] == 0: snake[0][0] = 18
        if snake[0][1] == 0: snake[0][1] = 58
        #if snake[0][0] == 19: snake[0][0] = 1
        if snake[0][1] == 59: snake[0][1] = 1

        # Exit if snake crosses the boundaries (Uncomment to enable)
        if snake[0][0] == 0 or snake[0][0] == 19: break
        #if snake[0][0] == 0 or snake[0][0] == 19 or snake[0][1] == 0 or snake[0][1] == 59: break
        #print 'opa'

        # If snake runs over itself
        if snake[0] in snake[1:]: break
        
        if snake[0] == food:                                            # When snake eats the food
            food = []
            score += 1
            while food == []:
                food = [randint(1, 18), randint(1, 58)]                 # Calculating next food's coordinates
                if food in snake: food = []
            #win.addch(food[0], food[1], '*')
        else:    
            last = snake.pop()                                          # [1] If it does not eat the food, length decreases
            #win.addch(last[0], last[1], ' ')
        #win.addch(snake[0][0], snake[0][1], '#')

        for y in range(0, h):
            for x in range(0, w):
                board[y][x] = ' '

        for s in snake:
            board[s[0]][s[1]] = '#'

        board[food[0]][food[1]] = '*'

        outstr = ''
        for x in range(0, w):
            outstr += '/'
        for y in range(0, h):
            for x in range(0, w):
                outstr += board[y][x]
            outstr += '\n'
        for x in range(0, w):
            outstr += '/'

        print outstr

        time.sleep(0.15)

    
    #snake = []

    #curses.endwin()


def get_input(con, cliente):
    global commands

    key = KEY_RIGHT

    while True:

        prevKey = key                                                  # Previous key pressed

        event = int( con.recv(1024) )

        key = key if event == -1 else event 
        if ((key == KEY_RIGHT and prevKey == KEY_LEFT) or 
            (prevKey == KEY_RIGHT and key == KEY_LEFT) or
            (prevKey == KEY_DOWN and key == KEY_UP) or
            (key == KEY_DOWN and prevKey == KEY_UP)):
            key = prevKey

        if key not in [KEY_LEFT, KEY_RIGHT, KEY_UP, KEY_DOWN, 27, 0]:     # If an invalid key is pressed
            key = prevKey

        commands[0] = key


    con.close()
    thread.exit()

def send_info(clients):
    global outstr

    while True:
        for c in clients:
            x = outstr
            x += str(randint(1,999))
            c[0].sendall(x)
            time.sleep(0.05)


HOST = '127.0.0.9'     # Endereco IP do Servidor
PORT = 5000            # Porta que o Servidor esta

if (len(sys.argv) == 2):
    HOST = sys.argv[1]
if (len(sys.argv) == 3):
    PORT = sys.argv[2]

tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
orig = (HOST, PORT)
tcp.bind(orig)
tcp.listen(1)

clients = []

thread.start_new_thread(process, tuple([clients]))
thread.start_new_thread(send_info, tuple([clients]))

while True:
    con, cliente = tcp.accept()
    c_info = [con, cliente]
    clients.append(c_info)
    thread.start_new_thread(get_input, tuple([con, cliente]))
    #thread.start_new_thread(send_info, tuple([con, cliente]))

tcp.close()

#curses.endwin()