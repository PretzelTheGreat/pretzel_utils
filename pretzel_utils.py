import os
import json
from csv import DictReader, DictWriter


def import_json_file(filename, custom_loader=None):
    data = None

    with open(filename, 'r') as open_file:
        data = json.load(filename, object_hook=custom_loader)

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


def import_file(filename, custom_loader=None):
    # generic function for importing files
    # file will be imported based on it's extention, with non-extention files being ignored
    # filename 
    #   can be an absolute or relative path, with the relative path starting in the directory this is called from
    # custom_loader
    #   this is used to pass a custom object_hook to the json.loads function, in the event a custom class/object
    #   needs to be loaded

    filename = os.path.normpath(filename)
    if not os.path.lexists(filename):
        print(f"{filename} does not exist!")
        return None

    file_ext = os.path.basename.split('.')[1]

    if file_ext == 'json':
        return import_json_file(filename, custom_loader=custom_loader)

    elif file_ext == 'csv':
        return import_csv_file(filename)

    elif file_ext == 'txt':
        return import_txt_file(filename)

    else:
        return None