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

c_player = 0

snake1 = [[randint(1, 9), randint(1, 29)]]
snake2 = [[randint(10, 18), randint(30, 58)]]

def process(clients):
    global commands
    global outstr
    global food
    global snake1
    global snake2
    global c_player

    w, h = 60, 20;
    board = [[0 for x in range(w)] for y in range(h)];

    score = 0

    #snake = [[4,10], [4,9], [4,8]]                                     # Initial snake co-ordinates
    #snake = [[4,10], [4,9], [4,8]]                                     
    
    food = [10,20]                                                     # First food co-ordinates

    # win.addch(food[0], food[1], '*')                                   # Prints the food

    key = KEY_RIGHT

    # while c_player == 0:
    #     pass

    for y in range(0, h):
        for x in range(0, w):
            board[y][x] = ' '

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

    while key != 27:                                                   # While Esc key is not pressed

        if (c_player == 0):
            continue

        key = commands[0]
        #snake = snake1
        # Calculates the new coordinates of the head of the snake. NOTE: len(snake) increases.
        # This is taken care of later at [1].
        snake1.insert(0, [snake1[0][0] + (key == KEY_DOWN and 1) + (key == KEY_UP and -1), snake1[0][1] + (key == KEY_LEFT and -1) + (key == KEY_RIGHT and 1)])

        # If snake1 crosses the boundaries, make it enter from the other side
        #if snake1[0][0] == 0: snake1[0][0] = 18
        if snake1[0][1] == 0: snake1[0][1] = 58
        #if snake1[0][0] == 19: snake1[0][0] = 1
        if snake1[0][1] == 59: snake1[0][1] = 1

        # Exit if snake1 crosses the boundaries (Uncomment to enable)
        if snake1[0][0] == 0 or snake1[0][0] == 19: break
        #if snake1[0][0] == 0 or snake1[0][0] == 19 or snake1[0][1] == 0 or snake1[0][1] == 59: break
        #print 'opa'

        # If snake1 runs over itself
        if snake1[0] in snake1[1:]: break
        
        if snake1[0] == food:                                            # When snake1 eats the food
            food = []
            score += 1
            while food == []:
                food = [randint(1, 18), randint(1, 58)]                 # Calculating next food's coordinates
                if food in snake1: food = []
            #win.addch(food[0], food[1], '*')
        else:    
            last = snake1.pop()                                          # [1] If it does not eat the food, length decreases
            #win.addch(last[0], last[1], ' ')
        #win.addch(snake[0][0], snake[0][1], '#')

        if c_player > 1:
            key2 = commands[1]

            #snake2.insert(0, [snake2[0][0] + (key2 == KEY_DOWN and 1) + (key2 == KEY_UP and -1), snake2[0][1] + (key2 == KEY_LEFT and -1) + (key2 == KEY_RIGHT and 1)])

            #snake2 = snake22

            snake2.insert(0, [snake2[0][0] + (key2 == KEY_DOWN and 1) + (key2 == KEY_UP and -1), snake2[0][1] + (key2 == KEY_LEFT and -1) + (key2 == KEY_RIGHT and 1)])

            if snake2[0][1] == 0: snake2[0][1] = 58
            if snake2[0][1] == 59: snake2[0][1] = 1
            if snake2[0][0] == 0 or snake2[0][0] == 19: break
            if snake2[0] in snake2[1:]: break
            if snake2[0] == food:                                            # When snake2 eats the food
                food = []
                score += 1
                while food == []:
                    food = [randint(1, 18), randint(1, 58)]                 # Calculating next food's coordinates
                    if food in snake2: food = []
            else:    
                last = snake2.pop()

            if snake2[0] in snake1[1:]: break
            if snake1[0] in snake2[1:]: break

        for y in range(0, h):
            for x in range(0, w):
                board[y][x] = ' '

        for s in snake1:
            board[s[0]][s[1]] = '#'

        if (c_player > 1):
            for s in snake2:
                board[s[0]][s[1]] = '@'

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
    global c_player
    # global snake1
    # global snake2
    # global food

    

    # if (c_player == 0):
    #     while snake1 == []:
    #         snake1 = [[randint(1, 18), randint(1, 58)]]
    #         if food in snake1: snake1 = []
        

    # else:
    #     pass

    this_p = c_player
    c_player += 1

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

        commands[this_p] = key


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