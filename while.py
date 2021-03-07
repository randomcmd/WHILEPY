# Made by @randomcmd in March 2021
# Python Compiler for while language
# Copyright 2021
# hello world

# Valid Syntax:
# x = x + 1
# x = x - 1
#
# while x != 0
#       x = x + 1
# while
#
# print x

# This simple language is meant to be a turing complete language with as little commands as possible

import sys
import re

# Dictionary for all user generated variables
variables = {}
while_stack = []
while_frame_stack = []

# Regex for different commands

regex_addition = "[a-zA-Z]+([a-zA-Z]*[0-9]*)+ = [a-zA-Z]+([a-zA-Z]*[0-9]*)+ \+ [0-9]+"
regex_subtraction = "[a-zA-Z]+([a-zA-Z]*[0-9]*)+ = [a-zA-Z]+([a-zA-Z]*[0-9]*)+ \- [0-9]+"
regex_while_condition = "while [a-zA-Z]+([a-zA-Z]*[0-9]*)+ \!\= 0"  # Comparisons like < > are not allowed in while 8
regex_while_frame = "while"
regex_print = "print [a-zA-Z]+([a-zA-Z]*[0-9]*)+"
regex_comment = "\A#"


def execute(filename):
    f = open(filename, "r")
    code = f.read().split('\n')
    evaluate(code)
    run(code)
    f.close()


def get_var(var):
    try:
        return variables[var]
    except:
        variables[var] = 0
        return 0


def printvar(line):
    varname = line.split(" ")[1]
    print(varname + " -> " + str(get_var(varname)))


def assignement(line, plus):
    # example x = x + 1696969606060069
    linearray = line.split(" ")

    if plus:
        result = get_var(linearray[2]) + int(linearray[3 + 1])
    else:
        result = get_var(linearray[2]) - int(linearray[3 + 1])
    result = max(result, 0)
    variables[linearray[0]] = result;
    # print(result) #debug


def evaluate(code):
    for i, line in enumerate(code):
        line = line.lstrip()
        # print(line, end=" ")
        if re.match(regex_comment, line) is not None:
            # print("Matches comment regex")
            continue
        elif re.match(regex_while_condition, line) is not None:
            #
            print(f"Matches while condition regex {i}")
            while_stack.append((i, line.split(" ")[1]))
            print(">>" + str(while_stack))
        elif re.match(regex_while_frame, line) is not None:
            #
            print(f"Matches while frame regex {i}")
            while_frame_stack.append((i, while_stack.pop()))
            print(">>" + str(while_frame_stack))

    if len(while_stack) != 0: raise Exception("Reached end of file while parsing") 


def run(code):
    i = -1
    while i < len(code) - 1: 
        # .
        i += 1
        line = code[i]
        line = line.lstrip()

        if re.match(regex_addition, line) is not None:
            assignement(line, 1)
        elif re.match(regex_subtraction, line) is not None:
            assignement(line, 0)
        elif re.match(regex_print, line) is not None:
            printvar(line)
        elif re.match(regex_while_condition, line) is not None:
            if (get_var(line.split(" ")[1]) == 0):
                for u in while_frame_stack:
                    if u[1][1] == line.split(" ")[1] and u[1][0] == i:
                        i = u[0]
                        continue

        elif re.match(regex_while_frame, line) is not None:
            for u in while_frame_stack:
                if u[0] == i and get_var(u[1][1]) != 0:
                    f = i
                    i = u[1][0]  # setting i to jump


def main():
    if len(sys.argv) == 2:
        execute(sys.argv[1])
    else:
        print("Usage:", sys.argv[0], "filename [.while]")


if __name__ == "__main__": main()
