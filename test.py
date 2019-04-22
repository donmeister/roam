#!/usr/bin/env python3

directions = {'0': ['left', 'l', 'west', 'w'],\
                '1' : ['right', 'r', 'east', 'e'],\
                '2' : ['up', 'u', 'north', 'n'],\
                '3' : ['down', 'd', 'south', 's']
            }
action = 'left'
for i in range(4):
    print(i)
    print(directions[str(i)])
    if action in directions[str(i)]:
        action = directions[str(i)][0]
        print(action)
