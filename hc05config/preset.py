import json
from .input_lib import get_input, INVALID_MESSAGE, BLUETOOTH_CONFIG_VALIDATE

def getPreset():
    try:
        with open("preset.json", "r") as file:
            return json.load(file)
    except:
        return {}

def writePreset(preset_json):
    with open("preset.json", "w") as file:
        file.write(json.dumps(preset_json))

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

def viewPreset():
    _, _, selectedPreset = _selectPreset()

    print("\n-----------------------------------------\n")
    for key, value in selectedPreset.items():
        print("{}: {}".format(key, value))
    print("\n-----------------------------------------\n")

def editPreset():
    preset = getPreset()
    category, title, selectedPreset = _selectPreset(preset)

    adjustPreset(selectedPreset, inputFunc=BLUETOOTH_CONFIG_VALIDATE)
    preset[category][title] = selectedPreset
    writePreset(preset)

def renamePreset():
    preset = getPreset()
    category, title, selectedPreset = _selectPreset(preset)

    new_title = input("Please enter a new title: ")
    del preset[category][title]
    preset[category][new_title] = selectedPreset
    writePreset(preset)

def copyPreset():
    preset = getPreset()
    category, title, selectedPreset = _selectPreset(preset)

    new_title = input("Please enter a new title: ")
    print("Preset has been copied (Title: \"{}\")".format(new_title))
    preset[category][new_title] = selectedPreset
    writePreset(preset)

def deletePreset():
    preset = getPreset()
    category, title, _ = _selectPreset(preset)

    print("Preset \"{}\" has been deleted".format(title))
    del preset[category][title]
    writePreset(preset)

# TODO: Export preset feature
def exportPreset():
    print("Work on Progress!")
    return

# TODO: Import preset feature
def importPreset():
    print("Work on Progress!")
    return