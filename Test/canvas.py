#from curses import KEY_RIGHT, KEY_LEFT, KEY_UP, KEY_DOWN


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

w, h = 10, 10;
board = [[0 for x in range(w)] for y in range(h)];

board[1][2] = 1;
board[1][3] = 1;
board[2][3] = 1;

for y in range(0, h):
	for x in range(0, w):
		if (board[y][x] == 1):
			#print(bcolors.WARNING + '#' + bcolors.ENDC),;
			print(bcolors.OKBLUE + '#' + bcolors.ENDC),;
		else:
			print(' '),;

	print(" ");