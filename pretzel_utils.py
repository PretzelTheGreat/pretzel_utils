import os
import json
import re
import math
from csv import DictReader, DictWriter
import datetime


date_fmt = re.compile(r"\d\d\d\d-\d\d-\d\d")

# Loading Files
def import_json_file(filename, object_hook=None, object_pairs_hook=None):
    data = None

    with open(filename, 'r') as open_file:
        data = json.load(open_file, object_hook=object_hook, object_pairs_hook=object_pairs_hook)

    return data


def import_csv_file(filename):
    data = []

    with open(filename, 'r') as open_file:
        csvReader = DictReader(open_file)

        for row in csvReader:
            data.append(row)

    return data


def import_txt_file(filename):
    data = []

    with open(filename, 'r') as open_file:
        for line in open_file.readlines():
            data.append(line.strip())

    return data


def import_file(filename, object_hook=None, object_pairs_hook=None):
    # generic function for importing files
    # file will be imported based on it's extention, with non-extention files being ignored
    # filename 
    #   can be an absolute or relative path, with the relative path starting in the directory this is called from
    # object_hook
    #   this is used to pass a custom object_hook to the json.loads function, in the event a custom class/object
    #   needs to be loaded

    filename = os.path.normpath(filename)
    if not os.path.lexists(filename):
        print(f"{filename} does not exist!")
        return None

    file_ext = os.path.basename(filename).split('.')[1]

    if file_ext == 'json':
        return import_json_file(filename, object_hook=object_hook, object_pairs_hook=object_pairs_hook)

    elif file_ext == 'csv':
        return import_csv_file(filename)

    elif file_ext == 'txt':
        return import_txt_file(filename)

    else:
        return None


# Saving Files
def save_json_file(filename, data, custom_encoder=None):
    with open(filename, 'w') as open_file:
        if custom_encoder != None:
            json.dump(data, open_file, indent=4, cls=custom_encoder)
        else:
            json.dump(data, open_file, indent=4)


def save_csv_file(filename, data, fieldnames):
    with open(filename, 'w', newline='') as open_file:
        csvWriter = DictWriter(open_file, fieldnames=fieldnames)
        csvWriter.writeheader()
        for row in data:
            csvWriter.writerow(row)


def save_txt_file(filename, data):
    with open(filename, 'w') as open_file:
        for line in data:
            open_file.write(f"{line}\n")


def save_file(filename, data, fieldnames=[], custom_encoder=None):
    filename = os.path.normpath(filename)

    file_ext = os.path.basename(filename).split('.')[1]

    if file_ext == 'json':
        if custom_encoder != None:
            save_json_file(filename, data, custom_encoder=custom_encoder)
        else:
            save_json_file(filename, data, custom_encoder)

    elif file_ext == 'csv':
        if fieldnames == []:
            if type(data) == list:
                fieldnames = data[0].keys()
            save_csv_file(filename, data, fieldnames)
        else:
            save_csv_file(filename, data, fieldnames)

    elif file_ext == 'txt':
        save_txt_file(filename, data)


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

def save_date_as_string(o):
    if isinstance(o, datetime.date):
        return o.isoformat()

    return o

def load_date_as_obj(o):
    if isinstance(o, str) and re.search(date_fmt, o):
        return datetime.date.fromisoformat(o)

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