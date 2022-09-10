import json
import re
import math
import datetime


date_fmt = re.compile(r"\d\d\d\d-\d\d-\d\d")

def get_new_uuid4_string():
    from uuid import uuid4 as U4
    return str(U4())


def exclude_fields(dct, fieldnames=[]):
    # this is used to simplify sending a dict with only desired fields
    new_dict = {}

    for k, v in dct:
        if k not in fieldnames:
            new_dict[k] = v

    return new_dict

class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.date):
            return obj.isoformat
        
        return json.JSONEncoder.default(self, obj)

def DateDecoder(o):
    for k, v in o.items():
        if isinstance(v, str) and re.search(date_fmt, v):
            o[k] = datetime.date.fromisoformat(v)

    return o


def get_longest_word_from_list(list_of_words):
    # this will return the longest word within a list of strings
    longest_word = ""
    for word in list_of_words:
        if len(word) > len(longest_word):
            longest_word = word

    return longest_word


def display_list_in_console(data, align="left", columns=4, width=8):
    # use this to primarily display lists of strings
    # width can be set by the user, but if it is not a larger amount
    # then the longest word in the list, then it would be ignored
    rows = math.ceil(len(data) / columns)
    start = 0
    end = columns + 1

    if align == "left":
        row_format = "{:<{width}}" * (columns - 1) + "{:<}"
    elif align == "center":
        row_format = "{:^{width}}" * (columns - 1) + "{:^}"
    elif align == "right":
        row_format = "{:>{width}}" * (columns - 1) + "{:>}"

    # this is used to determine the longest word in the list
    # and dynamically change the spacing to fit the words neatly, with 
    # enough padding in between the columns
    longest_word_length = len(get_longest_word_from_list(data))

    if longest_word_length > width:
        # the width will always be divisible by 4 (the length of a tab 
        # character, or four spaces)
        # if the modulo operator returns 0, it will add padding anyways
        width = longest_word_length + (4 - (longest_word_length % 4))

    for x in range(rows):
        if len(data[start:]) < columns:
            row = data[start:]
        else:
            row = data[start:end]

        # this will fill in any rows that do not reach the
        # same length as the desired columns
        if len(row) < columns:
            for y in range(columns - len(row)):
                row.append("")
        
        print(row_format.format(*row, width=width))

        start = end - 1
        end += columns


def validate_user_input(user_input, valid_input):
    # for now, this will just be a list of valid options that 
    # a user can type in
    
    if user_input in valid_input:
        return True

    return False


def get_user_input(input_type="SINGLE", message="", validate_input=False, valid_input=[]):
    # this will handle user input, and also validate that input, if any valid input is
    # required. There will be a sepcial format for validation

    if input_type == "SINGLE":
        if message != "":
            message = f"{message}\n>>> "
        else:
            message = ">>> "
        user_input = input(message).strip()

    elif input_type == "MULTI":
        user_input = []
        if message != "":
            print(message)
        while True:
            line = input("(press enter twice to quit)>>> ").strip()

            if line != "":
                user_input.append(line)

            else:
                break

    if validate_input:
        if validate_user_input(user_input, valid_input):
            return (user_input, True)

        else:
            return (user_input, False)           

    return user_input