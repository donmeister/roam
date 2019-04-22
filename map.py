#!/usr/bin/env python3

import time
import curses
import csv

def load_map(map_name):
    map = {}
    #print(type(x),x, type(y), y)
    linecount = 0
    with open(map_name + '.txt') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            map[linecount] = row
            #print(f'Map length {len(map)}')
            #input()
            #print(map[linecount])
            #print(type(linecount), linecount)
            linecount += 1
    return map

def print_map(map_name,x,y):
    traveler = '*'
    #print(type(x),x, type(y), y)
    height = len(map_name)
    for line in range(height):
        left = map_name[int(line)][:x]
        right = map_name[line][x:]
        #print(f'Line: {line}, {type(line)}')
        #print(f'x: {x}, {type(x)}')
        if line == y:
            #traveler = row[0:y-1]
            print(f"{map_name[line][0][:x]}{traveler}{map_name[line][0][x+1:]}")
        else:
            print(map_name[line][0])

def print_map_file(x,y):
    #print(type(x),x, type(y), y)
    linecount = 0
    traveler = "*"
    with open('rune.txt') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            #print(type(linecount), linecount)
            if linecount == y:
                #traveler = row[0:y-1]
                print(f"{row[0][:x]}{traveler}{row[0][x+1:]}")
            else:
                print(f"{row[0]}")
            linecount += 1

'''
def run(win, timeout=3): # timeout in seconds
    x = y = 10
    curses.echo()
    win.timeout(0) # Non-block read.

    line = 0
    while True:
        win.addstr(line, 0, "Enter something: ")
        s = []
        start = time.time()
        run = True
        while run:
            c = win.getch()
            time_taken = time.time() - start

            if c < 0:
                pass
            elif c in ENTER_KEY:
                break
            else:
                s.append(chr(c))

            if time_taken >= timeout:
                # Out of time.
                s.append(-1)
                run = False

        if len(s) == 0:
            break
        if s[-1] == -1:
            s.pop()
        answer = ''.join(s)
        #win.addstr(line + 1, 0, "Your input was: %s" % answer)
        print_map(x,y)
        line += 2

ENTER_KEY = (curses.KEY_ENTER, ord('\n'), ord('\r'))
'''
x = y = 10
#print_map(x,y)
z = 'print_map(x,y)'
map = load_map('rune')
print(len(map))
input()
while True:
#    eval(z)
    print_map(map,x,y)
    direction = input('>')
    print("\n" * 100)
    if direction == 'w':
        y -= 1
    elif direction == 's':
        y += 1
    elif direction == 'd':
        x += 1
    elif direction == 'a':
        x -= 1
    else:
        pass
#curses.wrapper(run)
