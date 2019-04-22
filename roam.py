#!/usr/bin/env python3

from cursesmenu import SelectionMenu
import random
import time
import subprocess as sp
import csv

directions = {
    'north': 'north', 'n': 'north', 'south': 'south', 's': 'south',
    'east': 'east', 'e': 'east', 'west': 'west', 'w': 'west',
    'northeast': 'northeast', 'ne': 'northeast',
    'southeast': 'southeast', 'se': 'southeast',
    'northwest': 'northwest', 'nw': 'northwest',
    'southwest': 'southwest', 'sw': 'southwest'
}

char_dir = {
    'north': '↑', 'south': '↓', 'east': '→', 'west': '←',
    'northeast': '↗', 'southeast': '↘', 'northwest': '↖', 'southwest': '↙'
}

turns = {
    'right': 'right', 'r': 'right', 'left': 'left', 'l': 'left'
}

char_turn = {
    ('right', 'north'): 'northeast', ('left', 'north'): 'northwest',
    ('right', 'northeast'): 'east', ('left', 'northeast'): 'north',
    ('right', 'east'): 'southeast', ('left', 'east'): 'northeast',
    ('right', 'southeast'): 'south', ('left', 'southeast'): 'east',
    ('right', 'south'): 'southwest', ('left', 'south'): 'southeast',
    ('right', 'southwest'): 'west', ('left', 'southwest'): 'south',
    ('right', 'west'): 'northwest', ('left', 'west'): 'southwest',
    ('right', 'northwest'): 'north', ('left', 'northwest'): 'west'
}

verbs = {
    'wait': 'wait', 'pause': 'wait', 'rest': 'wait', 'sleep': 'sleep',
    'inven': 'inven', 'inventory': 'inven', 'i': 'inven'
}

obj = {
    'spade': 0, 'shovel-like': 0, 'digging': 0,
    'lantern': 1, 'lamp': 1, 'light': 1,
    'mattress': -1, 'bed': -1
}

tk_objs = [
    ("A worn gardener's spade here.","A digging spade"),
    ("There is a shiny brass lamp nearby.", "A brass lantern")
]

tk_obj_desc = [
    "A spade that can be used as a shovel.",
    "A very old, hand-crafted lamp."
]

perm_obj_desc = [
    None,
    "A bed with the perfect mattress for sleep."
]

alignment = {
    'LG': 'lawful good',\
    'NG': 'neutral good',\
    'CG': 'chaotic good',\
    'LN': 'lawful neutral',\
    'N': 'neutral',\
    'CN': 'chaotic neutral',\
    'LE': 'lawful evil',\
    'NE': 'neutral evil',\
    'CE': 'chaotic evil'
}
race_trait = {
    'Dwarf': {
        'min_age': 25,\
        'max_age': 200,\
        'con_adj': 2,\
        'alignment': 'LG',\
        'speed': 25
    },
    'Elf': {
        'min_age': 50,\
        'max_age': 400,\
        'dex_adj': 2,\
        'alignment': 'CG',\
        'speed': 30
    },
    'Human': {
        'min_age': 15,\
        'max_age': 45,\
        'int_adj': 1,\
        'dex_adj': 1,\
        'con_adj': 1,\
        'cha_adj': 1,\
        'wis_adj': 1,\
        'str_adj': 1,\
        'alignment': 'N',\
        'speed': 30
    }
}
class_ability = {
    'Fighter': {
        'Description': 'A fierce warrior of primitive background.',
        'HD': 12,
        'WR': 5,
        'PA': ['str', 'dex'],
        'STP': ['str', 'con']
    },
    'Ranger': {
        'Description': 'A warrior who uses martial prowess and magic.',
        'HD': 10,
        'WR': 5,
        'PA': ['dex', 'wis'],
        'STP': ['str', 'con']
    },
    'Wizard': {
        'Description': 'A scholarly magician capable of manipulating reality.',
        'HD': 6,
        'WR': 4,
        'PA': ['int'],
        'STP': ['int', 'wis']
    }
}

def clear():
    print("\n" * 100)

def add_time(day, game_time, amount):
    game_time = game_time.split(':')
    hour = int(game_time[0])
    minute = int(game_time[1])
    hour = hour + int((amount + minute)/60)
    minute = (minute + amount) % 60
    if hour > 23:
        hour -= 24
        day += 1
    if minute < 10:
        minute = "0" + str(minute)
    else:
        minute = str(minute)
    if hour < 10:
        hour = "0" + str(hour)
    else:
        hour = str(hour)
    game_time = hour + ":" + minute
    #print(day, game_time)
    #input()
    return day, game_time

def print_info_bar(character, map_name):
    line_info = "| LVL: " + str(character['level'])\
                + " | XP: " + str(character['xp'])\
                + " | AC: " + str(character['ac'])\
                + " | HP: " + str(character['hp']) + "/"\
                + str(character['max_hp'])\
                + " | G: " + str(character['gold'])\
                + " | Day: " + str(day)\
                + " | Time: " + game_time + " |"
    line_length = len(line_info)
    line = "-" * line_length
    map_display_name = map_name.replace('_', ' ')
    print(line)
    print(f'|{map_display_name.center(line_length - 2).title()}|')
    print(line)
    print(line_info)
    print(line)

def load_map_index():
    map_index = {}
    linecount = 0
    with open('map_index.txt') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            map_index[row[0]] = {
                row[1]: [row[2], int(row[3]), int(row[4])],
                row[5]: [row[6], int(row[7]), int(row[8])],
                row[9]: [row[10], int(row[11]), int(row[12])],
                row[13]: [row[14], int(row[15]), int(row[16])]
            }
            #print(f'Map length {len(map)}')
            #input()
            #print(map[linecount])
            #print(type(linecount), linecount)
            linecount += 1
    return map_index

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
    global traveler
    #print(type(x),x, type(y), y)
    height = len(map_name)
    for line in range(height):
        #print(x)
        #print(type(x))
        #input()
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
    traveler = "↑"
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

def calc_initial_abilities(character):
    clear()
    max_hp = class_ability[character['class']]['HD']
    print(f"As a {character['class']}, {character['char_name']} ", end='')
    print(f"starts with {max_hp} Max Hit Points (HP)")
    print(f" and Armor Class (AC) of {character['ac']}.")
    print()
    time.sleep(two)
    if 'con_adj' in race_trait[character['race']]:
        hp_adj = int(race_trait[character['race']]['con_adj'])
        max_hp += hp_adj
        print(f"As a {character['race']}, {character['char_name']} gets a +", end='')
        print(f"{hp_adj} HP bonus for Constitution.")
        print(f"Max HP increased to {max_hp}.")
        time.sleep(four)
        print()
    if 'dex_adj' in race_trait[character['race']]:
        dex_adj = int(race_trait[character['race']]['dex_adj'])
        character['ac'] += dex_adj
        print(f"As a {character['race']}, {character['char_name']} gets a +", end='')
        print(f"{dex_adj} AC bonus for Dexterity.")
        print(f"AC increased to {character['ac']}.")
        time.sleep(four)
        print()
    return max_hp

def make_character():
    race = list(race_trait.keys())
    Class = list(class_ability.keys())

    #Pick Race
    menu = SelectionMenu(race,'Select a Race:',show_exit_option=False)
    menu.show()
    menu.join()
    selection = menu.selected_option
    character['race'] = race[selection]

    #Pick Class
    menu = SelectionMenu(Class,'Select a Class:',show_exit_option=False)
    menu.show()
    menu.join()
    selection = menu.selected_option
    character['class'] = Class[selection]

    #Assign initial abilities and characteristics
    character['age'] = random.randint(int(race_trait[character['race']]['min_age']),\
                                int(race_trait[character['race']]['max_age']))
    character['str'] = random.randint(3,18)
    character['int'] = random.randint(3,18)
    character['dex'] = random.randint(3,18)
    character['con'] = random.randint(3,18)
    character['wis'] = random.randint(3,18)
    character['cha'] = random.randint(3,18)
    character['numHD'] = 1
    character['level'] = 1
    character['xp'] = 0
    character['ac'] = 10

    #Determine starting Gold
    character['gold'] = 0
    rolls = 0
    wealth_rolls = int(class_ability[character['class']]['WR'])
    while rolls < wealth_rolls:
        rolls += 1
        character['gold'] += random.randint(1,4) * 10
        #print(f"{character['gold']} after roll {rolls}.")
        #input()
    character['max_hp'] = calc_initial_abilities(character)
    character['hp'] = character['max_hp']
    #Reduce initial max_hp to test healing
    #if character['max_hp'] < 6:
    #    character['hp'] = character['max_hp']
    #else:
    #    character['hp'] = character['max_hp'] - 5

    return race, Class

def intro():
    clear()
    #Print initial greeting and abilities
    print(f"Hi {character['name']}, welcome to Roam!\n")
    print(f"Your {character['age']} year old ", end='')
    print(f"{character['class']} character will hopefully be prosperous.")
    time.sleep(four)
    clear()
    print(f"Your {character['class']}, ", end='')
    print(f"{character['char_name']} has the following abilities:")
    time.sleep(one)
    print(f"     Strength: {character['str']}")
    time.sleep(one)
    print(f" Intelligence: {character['int']}")
    time.sleep(one)
    print(f"    Dexterity: {character['dex']}")
    time.sleep(one)
    print(f" Constitution: {character['con']}")
    time.sleep(one)
    print(f"       Wisdom: {character['wis']}")
    time.sleep(one)
    print(f"     Charisma: {character['cha']}")
    time.sleep(one)
    print()
    return character

def move(direction):
    global x, y, map, map_index, map_name
    x_step = y_step = 0
    #print(x,y)
    #print(map_index[map_name]['west'][0])
    #print(len(map_index[map_name]['west'][0]))
    #print(type(map_index[map_name]['west'][0]))
    if direction == 'north':
        y_step = -1
    elif direction == 'south':
        y_step = 1
    elif direction == 'east':
        x_step = 1
    elif direction == 'west':
        x_step = -1
    elif direction == 'northeast':
        y_step = -1
        x_step = 1
    elif direction == 'southeast':
        y_step = 1
        x_step = 1
    elif direction == 'southwest':
        y_step = 1
        x_step = -1
    elif direction == 'northwest':
        y_step = -1
        x_step = -1
    else:
        pass
    if x == 0 and x_step == -1:
        x = map_index[map_name]['west'][1]
        y = map_index[map_name]['west'][2]
        map_name = map_index[map_name]['west'][0]
        map_display_name = map_name.replace('_', ' ')
        #print(map_name)
        #input()
        map = load_map(map_name)
        print(f'Entering...{map_display_name.title()}')
        x_step = 0
    elif x == len(str(map[y]))-5 and x_step == 1:
        x = map_index[map_name]['east'][1]
        y = map_index[map_name]['east'][2]
        map_name = map_index[map_name]['east'][0]
        map_display_name = map_name.replace('_', ' ')
        #print(map_name)
        #input()
        map = load_map(map_name)
        print(f'Entering...{map_display_name.title()}')
        x_step = 0
    elif y == 0 and y_step == -1:
        x = map_index[map_name]['north'][1]
        y = map_index[map_name]['north'][2]
        map_name = map_index[map_name]['north'][0]
        map_display_name = map_name.replace('_', ' ')
        #print(map_name)
        #input()
        map = load_map(map_name)
        print(f'Entering...{map_display_name.title()}')
        y_step = 0
    elif y == len(map)-1 and y_step == 1:
        x = map_index[map_name]['south'][1]
        y = map_index[map_name]['south'][2]
        map_name = map_index[map_name]['south'][0]
        map_display_name = map_name.replace('_', ' ')
        #print(map_name)
        #input()
        map = load_map(map_name)
        print(f'Entering...{map_display_name.title()}')
        y_step = 0
    elif (y+y_step in map) and (map[y+y_step][0][x+x_step] == " "):
        x += x_step
        y += y_step
    else:
        print('Way is blocked...')

def sleep():
    print("You nod off...")
    if character['hp'] < character['max_hp']:
        starting_hp = character['hp']
        if command[0] in ['sleep']:
            healing = random.randint(1,2)
        character['hp'] += healing
        if character['hp'] < character['max_hp'] and healing > 0:
            print("...and awake feeling better.")
        elif character['hp'] >= character['max_hp']:
            character['hp'] = character['max_hp']
            print("...and awake feeling fully restored.")
        else:
            print("...and awake feeling no better than before.")
        time.sleep(one)
        print()
        if character['hp'] > starting_hp:
            print(f"{character['name']}'s health has improved by ", end='')
            print(f"{character['hp'] - starting_hp} HP.")
            print()
    else:
        print("...and awake feeling exactly the same.")
        print()

def run_command(command):
    if command[0] in verbs:
        verb = command[0]+'()'
        eval(verb)

#Main routine
clear()
one = 1
two = 2
three = 3
four = 4
one = two = three = four = 0
global x, y, traveler
traveler = '↑'
x = 38
y = 24
character = {}
character['name'] = ''
character['char_name'] = ''
while character['name'] == '':
    character['name'] = input('Your Name: ')
while character['char_name'] == '':
    character['char_name'] = input('Your Character Name: ')
race = Class = list()
#alignment = race_trait = class_ability = {}
#Debug dictionary values
#print(race_trait)
#input('Debug...<Enter> to continue...')
race, Class = make_character()
intro()
inventory = {}
char_alive = True
day = 1
game_time = '10:00'
map_name = 'rune'
map_index = load_map_index()
#print(map_index)
#input()
map = load_map(map_name)
direction = 'north'
while char_alive:
    #print(f"{character['char_name']} is still alive...after {char_days} days.")
    #char_alive = random.randint(0,10)

    #Actual width of map
    #print(len(str(map[y])))

    #print(map_name.capitalize())
    print_map(map, x, y)
    print_info_bar(character, map_name)
    command = input("> ").lower().split()
    clear()
    if len(command) > 0:
        if command[0] in directions:
            direction = directions[command[0]]
            move(direction)
            traveler = char_dir[direction]
            day, game_time = add_time(day, game_time, 5)
        elif command[0] in turns:
            traveler = char_dir[char_turn[(turns[command[0]], direction)]]
            direction = char_turn[(turns[command[0]], direction)]
        elif command[0] in verbs:
            run_command(command)
            day, game_time = add_time(day, game_time, 5)
        elif command[0] != '':
            print(f'You do not know how to "{command[0]}."')
            print()
print(f"{character['name']} died at the age of ", end='')
print(f"{int(character['age'] + char_days/365)}.")
print()
print_info_bar(character)
print("The end...")
