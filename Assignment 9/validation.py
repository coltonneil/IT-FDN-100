#!/usr/bin/env python3
"""
requires Python3

Script provides float and string input validation and a funcional way to display and select menu options
"""
import re
#menu = ["New report", "Load report", "Delete Report", "Edit tax and fees", "Quit"]


# builds a menu from an array or dictionary and presents the user with a numeric choice, returns that selection
def display_options(options, prompt):
    lookup_dict = {}
    for index, item in enumerate(options):
        print("[{}] - {}".format(str(index + 1), item))
        if type(options) == dict:
            lookup_dict[index + 1] = item
    while True:
        try:
            selection = int(input(prompt))
        except ValueError:
            print("Selection must be a number")
            continue
        if selection < 1 or selection > len(options):
            print("Choose a number from the list")
            continue
        else:
            break
    if type(options) == dict:
        return lookup_dict[selection-1]
    else:
        return selection


# gets and validates floats
def validate_float(data_name, allow_zero=False):
    while True:
        try:
            tmp_float = float(input("Input {}: ".format(data_name)))
        except ValueError:
            print("{} must be a number".format(data_name))
            continue
        if tmp_float < 1 and not allow_zero:
            print("{} must be greater than 0".format(data_name))
            continue
        else:
            break
    return round(tmp_float, 2)


# gets a string from the user and insures it meets set specifications
def required_string(prompt, max_length=25, required_length=0, regex_pattern=""):
    while True:
        tmp = input(prompt)
        if required_length != 0 and len(tmp) != required_length:
            print("Must be {} characters".format(required_length))
            continue
        if len(tmp) == 0:
            print("Must not be blank")
            continue
        if len(tmp) > max_length:
            print("Cannot be longer than {} characters".format(max_length))
            continue
        if len(regex_pattern) > 0:
            if not re.match(regex_pattern, tmp):
                print("Input format invalid")
                continue
        break
    return tmp

