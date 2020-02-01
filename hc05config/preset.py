import json
from .input_lib import get_input, INVALID_MESSAGE, BLUETOOTH_CONFIG_VALIDATE
from copy import deepcopy
import os

DEFAULT_PRESET_PATH = "~/.hc05config_preset"

def getPreset(json_file=DEFAULT_PRESET_PATH):
    try:
        with open(os.path.abspath(os.path.expanduser(json_file)), "r") as file:
            preset = json.load(file)

        # support for older version
        replace_flag = False
        if "BT_Config" in preset.keys():
            preset["Bluetooth Config"] = deepcopy(preset["BT_Config"])
            del preset["BT_Config"]
            replace_flag = True
        if "Master_and_Slave" in preset.keys():
            preset["Master and Slave"] = deepcopy(preset["Master_and_Slave"])
            del preset["Master_and_Slave"]
            replace_flag = True
        if replace_flag:
            writePreset(preset)
        
        return preset
    except:
        return {}

def writePreset(preset_json, json_file=DEFAULT_PRESET_PATH, *arg, **kwarg):
    with open(os.path.abspath(os.path.expanduser(json_file)), "w") as file:
        file.write(json.dumps(preset_json, *arg, **kwarg))

def selectPreset(category):
    preset = getPreset()
    if category in preset.keys():
        print("Please select the following preset:")
        title = [t for t in preset[category].keys()]
        for i, key in enumerate(title, start=1):
            print("{}. {}".format(i, key))
        selection = get_input(int, "Please select 1-{}: ".format(len(title)), INVALID_MESSAGE, range(1, i+1))
        return preset[category][title[selection-1]]
    else:
        print("There is no preset available")
        return None

def adjustPreset(preset, inputFunc={}):
    keys = [key for key in preset.keys()]
    
    while True:
        print("\nPlease select the item you want to change:")
        for i, key in enumerate(keys, start=1):
            print("{}. {}: {}".format(i, key, preset[key]))

        selection = get_input(int, "Please enter 1-{}, or press enter to exit: ".format(i), wrong_msg=INVALID_MESSAGE, correct=range(1, i+1), allow_empty=True)
        if selection:
            key = keys[selection - 1]
            func = inputFunc.get(key)
            if func:
                user_input = func()
                preset[key] = user_input
            else:
                preset[key] = input("Please enter a new {}: ".format(key))
        else:
            return preset

def savePreset(category, preset):
    if get_input(str, "Do you want to save the configuration as a preset? (Y/N) ", INVALID_MESSAGE, ["Y", "N", "y", "n"]).upper() == "Y":
        preset_json = getPreset()
        if preset_json.get(category) == None:
            preset_json[category] = {}
        
        category_json = preset_json[category]
        while True:
            title = input("Please enter the preset title: ")
            if category_json.get(title) != None:
                option = get_input(str, "\"{}\" already exist, Do you want to Replace(r), Keep Both(k), or Stop(s)? ".format(title), INVALID_MESSAGE, ["R", "K", "S", "r", "k", "s"]).upper()
                if option == "K":
                    title += "_2"
                elif option == "S":
                    continue

            category_json[title] = preset
            writePreset(preset_json)
            print("Preset is saved")
            break

def managePreset():
    print("\n-----------------------------------------\n")
    while True:
        print("Please select the following job:")
        print("1. View preset")
        print("2. Edit preset")
        print("3. Rename preset")
        print("4. Copy preset")
        print("5. Delete preset")
        print("6. Export preset")
        print("7. Import preset")

        selection = get_input(int, "Please enter 1-7, or press enter to exit: ", correct=range(1, 8), allow_empty=True)

        print()

        if selection == 1:
            viewPreset()
        elif selection == 2:
            editPreset()
        elif selection == 3:
            renamePreset()
        elif selection == 4:
            copyPreset()
        elif selection == 5:
            deletePreset()
        elif selection == 6:
            exportPreset()
        elif selection == 7:
            importPreset()
        else:
            break

        input("Press enter to exit")
        print()

def _selectPreset(preset=None):
    if preset == None:
        preset = getPreset()
    if not preset:
        print("There is no preset available")
        return

    print("Please select a Category")
    categories = [c for c in preset.keys()]
    for i, key in enumerate(categories, start=1):
        print("{}. {}".format(i, key))

    selection = get_input(int, "Please select 1-{}: ".format(len(categories)), INVALID_MESSAGE, range(1, i+1))
    category = categories[selection-1]
    print()
    
    print("Please select the following preset:")
    titles = [t for t in preset[category].keys()]
    for i, key in enumerate(titles, start=1):
        print("{}. {}".format(i, key))
    selection = get_input(int, "Please select 1-{}: ".format(len(titles)), INVALID_MESSAGE, range(1, i+1))
    title = titles[selection-1]
    return category, title, preset[category][title]

def _savePreset(preset_json, category, title, preset):
    if preset_json.get(category) == None:
        preset_json[category] = {}
    
    category_json = preset_json[category]

    option = ""
    while True:
        if category_json.get(title) != None:
            option = get_input(str, "\"{}\" already exist, Do you want to Replace(r), Keep Both(k), or Stop(s)? ".format(title), INVALID_MESSAGE, ["R", "K", "S", "r", "k", "s"]).upper()
            if option == "K":
                title += "_2"
            elif option == "S":
                return False
        break

    category_json[title] = preset
    return option != "R"

def viewPreset():
    try:
        _, _, selectedPreset = _selectPreset()
    except:
        return

    print("\n-----------------------------------------\n")
    for key, value in selectedPreset.items():
        print("{}: {}".format(key, value))
    print("\n-----------------------------------------\n")

def editPreset():
    preset = getPreset()
    if not preset:
        print("There is no preset available")
        return
    category, title, selectedPreset = _selectPreset(preset)

    adjustPreset(selectedPreset, inputFunc=BLUETOOTH_CONFIG_VALIDATE)
    preset[category][title] = selectedPreset
    writePreset(preset)

def renamePreset():
    preset = getPreset()
    if not preset:
        print("There is no preset available")
        return
    category, title, selectedPreset = _selectPreset(preset)

    new_title = input("Please enter a new title: ")
    _savePreset(preset, category, new_title, selectedPreset)
    del preset[category][title]
    preset[category][new_title] = selectedPreset
    writePreset(preset)
    print("Preset \"{}\" is renamed".format(title))

def copyPreset():
    preset = getPreset()
    if not preset:
        print("There is no preset available")
        return
    category, title, selectedPreset = _selectPreset(preset)

    new_title = input("Please enter a new title: ")
    print("Preset has been copied (Title: \"{}\")".format(new_title))
    preset[category][new_title] = selectedPreset
    writePreset(preset)

def deletePreset():
    preset = getPreset()
    if not preset:
        print("There is no preset available")
        return
    category, title, _ = _selectPreset(preset)

    print("Preset \"{}\" has been deleted".format(title))
    del preset[category][title]
    if not preset[category]:
        del preset[category]
    writePreset(preset)

# TODO: Export preset feature
def exportPreset():
    preset = getPreset()
    if not preset:
        print("There is no preset available")
        return

    while True:
        print("Please enter the directory and file name (e.g. ~/Desktop/bluetooth_preset):")
        file = input()
        absPath = os.path.abspath(os.path.expanduser(file))
        if os.path.isfile(absPath):
            option = get_input(str, "\"{}\" already exist, Do you want to Replace(r), Keep Both(k), or Stop(s)? ".format(absPath), INVALID_MESSAGE, ["R", "K", "S", "r", "k", "s"]).upper()
            if option == "K":
                absPath += "_2"
            elif option == "S":
                continue
        break

    dir, _ = os.path.split(absPath)
    if not os.path.isdir(dir):
        os.makedirs(dir)
    writePreset(preset, json_file=absPath, indent=4)

    print("Presets have been exported to \"{}\"".format(absPath))

# TODO: Import preset feature
def importPreset():
    file = get_input(str, "Please enter the directory and file name (e.g. ~/Desktop/bluetooth_preset):\n", "File not exist, please enter again", correct=lambda x: os.path.isfile(os.path.abspath(os.path.expanduser(x))))
    absPath = os.path.abspath(os.path.expanduser(file))
    
    preset_import = getPreset(absPath)
    preset = getPreset()

    for category, new_presets in preset_import.items():
        print("Importing \"{}\" preset".format(category))
        for title, new_preset in new_presets.items():
            _savePreset(preset, category, title, new_preset)

    writePreset(preset)
    print("Presets have been imported")