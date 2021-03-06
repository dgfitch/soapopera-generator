#!/usr/bin/env python3

import os
import random
import sys
from contextlib import suppress
from termcolor import colored, cprint

class Getch:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

getch = Getch()

def load_file(path):
    with open(path, 'r') as f:
        stuff = f.read().splitlines()
    return set(stuff)

def clear():
    os.system('clear')

party_people = {}

used = load_file("names-used.txt")
weird = load_file("names.txt") - used
male = load_file("names-male.txt") - used
female = load_file("names-female.txt") - used

occupations = load_file("occupations.txt")
occupations_weird = load_file("occupations-weird.txt")
strengths = load_file("strength.txt")
weaknesses = load_file("weakness.txt")

def ok(thing):
    print("Is this okay? (Y/n) ", end='', flush=True)
    answer = getch()
    print()
    if answer.lower() == "n":
        return None
    else:
        return thing

def pick_name():
    print("Would you like a non-gendered name? (y/N) ", end='', flush=True)
    answer = getch()
    print()

    if answer.lower() == "y":
        name = random.sample(weird, 1)[0]
    else:
        answer = ""
        while answer == "":
            print("Would you like to have a male or female name? (enter m or f) ", end='', flush=True)
            answer = getch()
            print()
            if answer.lower() == "m":
                name = random.sample(male, 1)[0]
            elif answer.lower() == "f":
                name = random.sample(female, 1)[0]
            else: 
                answer = ""

    cprint("Your name is:", 'blue')
    cprint(name, 'red', attrs=['bold'])
    print()
    return ok(name)

def pick_occupation():
    print("Would you like a normal job? (Y/n) ", end='', flush=True)
    answer = getch()
    print()

    if answer.lower() == "y":
        occupation = random.sample(occupations, 1)[0]
    else:
        occupation = random.sample(occupations_weird, 1)[0]
    cprint("Your occupation is:", 'blue')
    cprint(occupation, 'red', attrs=['bold'])
    print()
    return ok(occupation)

def pick_strength():
    strength = random.sample(strengths, 1)[0]
    cprint("Your strength is:", 'blue')
    cprint(strength, 'green', attrs=['bold'])
    print()
    return ok(strength)

def pick_weakness():
    weakness = random.sample(weaknesses, 1)[0]
    cprint("Your weakness is:", 'blue')
    cprint(weakness, 'yellow', attrs=['bold'])
    print()
    return ok(weakness)

while True:
    clear()
    print(colored('WELCOME', 'yellow', attrs=["bold"]),
          colored('to the', 'white', attrs=["dark"]),
          colored('DAYS', 'red', attrs=["bold"]),
          colored('of', 'white', attrs=["dark"]),
          colored('OUR LIVES', 'red', attrs=["bold"]))
    print()

    real_name = input("Please enter your (actual) name and then hit ENTER: ")

    name = None
    while not name:
        name = pick_name()

    occupation = None
    while not occupation:
        occupation = pick_occupation()

    strength = None
    while not strength:
        strength = pick_strength()

    weakness = None
    while not weakness:
        weakness = pick_weakness()

    clear()
    print("Okay", colored(name, 'red', attrs=["bold"]) + ",",
            "please take an index card and a pen,\nand write this down before the amnesia sets in:\n")

    print(colored('      Name:', 'blue'),
          colored(name, 'red', attrs=["bold"]))

    print(colored('Occupation:', 'blue'),
          colored(occupation, 'red', attrs=["bold"]))

    print(colored('  Strength:', 'blue'),
          colored(strength, 'green', attrs=["bold"]))

    print(colored('  Weakness:', 'blue'),
          colored(weakness, 'yellow', attrs=["bold"]))

    # Nemesis, every 4th person gets one!
    number_of_partiers = len(party_people.keys())
    nemesis = None
    their_name = None
    if number_of_partiers > 1 and number_of_partiers % 4 == 0:
        nemesis = random.sample(party_people.keys(), 1)[0]
        their_name = party_people[nemesis]

        print(colored('   Nemesis:', 'blue'),
            colored(nemesis, 'yellow', attrs=["bold"]),
            f"(played by {their_name})")

        print()
        print("            You can let them know you're here for revenge.")
        print("            Or you can surprise them later!")
        print("            If you don't know them, TOO BAD!")

    print()
    print("Be honest. Did you write all that down, or do you just want to start over? (hit o to start over and return the name to the pool, any other key to party!)")
    answer = getch()

    if answer.lower() != "o":
        party_people[name] = real_name

        # Write name to names-used.txt so it only gets used once
        with open('character-dump.txt', 'a') as f:
            f.write(f"{real_name}: {name}, {occupation}. Strength: {strength}. Weakness: {weakness}. Nemesis: {nemesis}, {their_name}")
            f.write("\n")
        with open('names-used.txt', 'a') as f:
            f.write(name)
            f.write("\n")
        with suppress(KeyError):
            weird.remove(name)
            male.remove(name)
            female.remove(name)
