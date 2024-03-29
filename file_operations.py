import os
import json
from csv import DictReader, DictWriter

# Loading Files
def load_json_file(filename, encoding='utf-8', object_hook=None, object_pairs_hook=None):
    data = None

    with open(filename, 'r', encoding=encoding) as open_file:
        if object_hook != None and object_pairs_hook == None:
            data = json.load(open_file, object_hook=object_hook)
        elif object_pairs_hook != None:
            data = json.load(open_file, object_pairs_hook=object_pairs_hook)
        else:
            data = json.load(open_file)

    return data


def load_csv_file(filename, encoding='utf-8'):
    data = []

    with open(filename, 'r', encoding=encoding) as open_file:
        csvReader = DictReader(open_file)

        for row in csvReader:
            data.append(row)

    return data


def load_txt_file(filename, encoding='utf-8'):
    data = []

    with open(filename, 'r', encoding=encoding) as open_file:
        for line in open_file.readlines():
            data.append(line.strip())

    return data


def load_file(filename, encoding='utf-8', object_hook=None, object_pairs_hook=None):
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
        return load_json_file(filename, encoding=encoding, object_hook=object_hook, object_pairs_hook=object_pairs_hook)

    elif file_ext == 'csv':
        return load_csv_file(filename, encoding=encoding)

    elif file_ext == 'txt':
        return load_txt_file(filename, encoding=encoding)

    else:
        return None


# Saving Files
def save_json_file(filename, data, encoding='utf-8', custom_encoder=None):
    with open(filename, 'w', encoding=encoding) as open_file:
        if custom_encoder != None:
            json.dump(data, open_file, indent=4, cls=custom_encoder)
        else:
            json.dump(data, open_file, indent=4)


def save_csv_file(filename, data, fieldnames, encoding='utf-8'):
    with open(filename, 'w', newline='', encoding=encoding) as open_file:
        csvWriter = DictWriter(open_file, fieldnames=fieldnames)
        csvWriter.writeheader()
        for row in data:
            csvWriter.writerow(row)


def save_txt_file(filename, data, encoding='utf-8'):
    with open(filename, 'w', encoding=encoding) as open_file:
        for line in data:
            open_file.write(f"{line}\n")


def save_file(filename, data, encoding='utf-8', fieldnames=[], custom_encoder=None):
    filename = os.path.normpath(filename)

    file_ext = os.path.basename(filename).split('.')[1]

    if file_ext == 'json':
        if custom_encoder != None:
            save_json_file(filename, data, encoding=encoding, custom_encoder=custom_encoder)
        else:
            save_json_file(filename, data, custom_encoder, encoding=encoding)

    elif file_ext == 'csv':
        if fieldnames == []:
            if type(data) == list:
                fieldnames = data[0].keys()
            save_csv_file(filename, data, fieldnames, encoding=encoding)
        else:
            save_csv_file(filename, data, fieldnames, encoding=encoding)

    elif file_ext == 'txt':
        save_txt_file(filename, data, encoding=encoding)
