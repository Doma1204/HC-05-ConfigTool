import json
from .input_lib import *

def getPreset():
    try:
        with open("preset.json", "r") as file:
            return json.load(file)
    except:
        return {}

def writePreset(preset_json):
    with open("preset.json", "w") as file:
        file.write(json.dumps(preset_json))

def selectPreset(category, preset=None):
    if preset == None:
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
        print("Please select the item you want to change:")
        for i, key in enumerate(keys, start=1):
            print("{}. {}: {}".format(i, key, preset[key]))
        while True:
            selection = input("Please enter 1-{}, or press enter to exit: ".format(i))
            if selection:
                try:
                    selection = int(selection)
                    if selection in range(1, i+1):
                        key = keys[selection-1]
                        func = inputFunc.get(key)
                        if func:
                            user_input = func()
                            if user_input != None:
                                preset[key] = user_input
                        else:
                            preset[key] = input("Please enter a new {}: ".format(key))
                    else:
                        print(INVALID_MESSAGE)
                        continue
                except:
                    print(INVALID_MESSAGE)
                    continue
                print()
                break
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

def viewPreset():
    preset = getPreset()
    if not preset:
        print("There is no preset available")
        return

    print("Please select a Category")
    categories = [c for c in preset.keys()]
    for i, key in enumerate(categories, start=1):
        print("{}. {}".format(i, key))

    selection = get_input(int, "Please select 1-{}: ".format(len(categories)), INVALID_MESSAGE, range(1, i+1))
    print()
    selectedPreset = selectPreset(categories[selection-1], preset=preset)

    print("\n-----------------------------------------\n")
    for key, value in selectedPreset.items():
        print("{}: {}".format(key, value))
    print("\n-----------------------------------------\n")
