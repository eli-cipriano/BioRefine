import sys
import PySimpleGUI as sg
import bioreflib as brf
import json

"""
This code can be run in a pysimple trinket.io
See: https://pysimplegui.trinket.io/demo-programs#/demo-programs/the-basic-pysimplegui-program

SAVING YOUR BIOPROCESS:
When saving, your output file will be written as a json, whether you
include a file extension or not.

brf functions used:
 - user_change
     this allows user to input variables and altering the map to
     maintain relationship integrity
 - get_avails
    gets list of compatible options
 - print_bioprocess
    prints the final map to the commandline
 - write_bioprocess
    writes the final map to a file of your choice

"""


def main_layout(modValues, mod_units, header=''):
    """
    formats a PySimpleGUI window to be input into PySimple's Window method.

    Parameters
    -------------
    title = string
      a string you want as the title of your pop-up window

    modValues = list of list of strings.
      a list of three lists, for three rows in the pop-up.
      each of the three list should contain the button modValues for that row.

    Returns
    -------------
    produces input for a window of five lines, with four buttons in the
    1st, 3rd, and 5th lines.
    """
    sg.theme('DarkAmber')
    divider = '---------------------------------------------------------------'\
        '---------------------------------------------------------------'
    spacer = '                                                                '\
        '                                                '

    # Set up the buttons.
    # Then add text for the results.

    tab1_layout = [[sg.Text(header, key='header')],
                   [sg.Button(modValues['side1'], key='side1'), sg.Text(' --> '),
                    sg.Button(modValues['sub1'], key='sub1'), sg.Text(' --> '),
                    sg.Button(modValues['proc1'], key='proc1'), sg.Text(' --> '),
                    sg.Button(modValues['prod1'], key='prod1')
                    ],

                   [sg.Text('  |  ')],

                   [sg.Button(modValues['material'], key='material'), sg.Text(' --> '),
                    sg.Button(modValues['substrate'], key='substrate'), sg.Text(' --> '),
                    sg.Button(modValues['process'], key='process'), sg.Text(' --> '),
                    sg.Button(modValues['product'], key='product')
                    ],

                   [sg.Text('  |  ')],

                   [sg.Button(modValues['side2'], key='side2'), sg.Text(' --> '),
                    sg.Button(modValues['sub2'], key='sub2'), sg.Text(' --> '),
                    sg.Button(modValues['proc2'], key='proc2'), sg.Text(' --> '),
                    sg.Button(modValues['prod2'], key='prod2')
                    ],

                   [sg.Text(divider, key='changeTEXT')],

                   [sg.Text('Change ____:', key='changeMod')],

                   [sg.Combo(values=[''], key='changeOptions', size=(20, 1)),
                    sg.Button('Apply Change')],

                   [sg.Text(spacer),
                    sg.Button('Load Preset', key='load'),
                    sg.Button('Save & Quit', key='exit')]
                   ]

    tab2_layout = [[sg.T('Get Details')],

                   [sg.Text('See details for:')],

                   [sg.Combo(values=mod_units,
                             key='detailOptions', size=(20, 1)),
                    sg.Button('Enter', key='Detail Chosen')], ]

    tab3_layout = [[sg.T('Add Data')],

                   [sg.Text('Add data for:')],

                   [sg.Combo(values=mod_units,
                             key='new_mod', size=(20, 1)),
                    sg.Button('Go', key='Detail Chosen')], ]

    layout = [[sg.TabGroup([[sg.Tab('Bioprocess', tab1_layout),
                             sg.Tab('Details', tab2_layout),
                             sg.Tab('Custom', tab3_layout)]])]]

    return layout


def callback_UserChange(changingMod, avails, currentMods, window):
    """
    This appears to add the values of the dropdown list.

    Parameters
    -------------
    changingMod =

    avails =

    currentMods =

    window=

    Returns
    -------------

    """

    title = 'Change {}:'.format(changingMod)
    window['changeMod'].update(title)
    # add clear option for sideFlows
    if changingMod[0:4] == 'side':
        if 'none' not in avails:
            avails.append('none')
        if 'NA' in avails:
            avails.remove('NA')

    window['changeOptions'].update(values=avails)
    window['changeOptions'].update(value='')


def callback_ApplyChange(window, newVal):
    """
    Updates the window based on output from callback_UserChange

    Parameters
    -------------
    window =

    newVal =

    Returns
    -------------
    """
    # set values and value to empty to get rid of previously specified answers
    window['changeMod'].update('Change ___:')
    window['changeOptions'].update(values=[''])
    window['changeOptions'].update(value='')

    return newVal


def callback_LoadMap(fileName=None):
    """
    Allows user to load in a previously saved bioprocess
    """
    loading_msg = 'Load Bioprocess:'\
        '\n(will check processes/ by default)'

    # get fileName from user
    if not fileName:
        fileName = sg.popup_get_text(loading_msg, 'File Loader')
    # add default path and .json ext
    fileName = default_path(fileName)
    jName, fileName = brf.get_file_ext('.json', fileName)
    # attempt to load in specified json
    try:
        with open(jName) as j:
            currentMods = json.load(j)
    except(FileNotFoundError):
        sg.popup('Error: File could not be opened')
        currentMods = None
    return currentMods


def callback_UpdateMap(cm, mod_units, window):
    for mod in mod_units:
      # Boost is not implemented yet, just a potential way to link different
      # bioprocesses together via sideFlows
        if mod[0:5] != 'boost':
            # Updates a mod of the window . . .
            window[mod].update(cm[mod]['name'])


def callback_Save():
    saving_msg = 'Save Bioprocess As:'\
        '\n(will save in processes/ by default)'
    fileName = sg.popup_get_text(saving_msg, 'File Saver')

    if fileName:
        # read filename and add default path
        fileName = fileName.strip(' ')
        fileName = default_path(fileName)

    # if user does not input a fileName
    elif fileName is None:
        fileName = 'cancel'
    elif fileName == '':
        fileName = 'exit'
    return fileName


def callback_Details(detailMod, mod, currentMods):
    """
    sub function for receiving input from user on which module they would like
    to view detailed properties of.
    """
    detailText = brf.print_Details(detailMod, mod, currentMods)
    detailPopup = sg.popup(detailText)


def default_path(fileName):
    """
    sub function for reading file paths, determining whether a path was
    specified or just the file name (in default "processes" path)
    """
    noPath = '/' not in fileName or '\\' not in fileName
    if noPath:
        fileName = ''.join(['processes/', fileName])
    return fileName


def main():
    # initialize the bioprocess with default values
    cm = callback_LoadMap(fileName='example_ethanol')

    # make a list of all the module names
    mod_units = ['product', 'process', 'substrate', 'material',
                 'side1', 'sub1', 'proc1', 'prod1', 'boost1',
                 'side2', 'sub2', 'proc2', 'prod2', 'boost2']
    # store current module values for updating button names
    modValues = {}
    # to begin, no module is specified for change
    changingMod = None

    for mod in mod_units:
        if mod[0:5] != 'boost':
            # Here's this line again. What does it do?
            modValues[mod] = cm[mod]['name']

    window = sg.Window('Your Current Bioprocess', main_layout(modValues, mod_units))

    ###########################################################################
    # Event Loop
    ###########################################################################

    while True:
        event, values = window.read()
        try:
            # check that conditions are met for input actions
            canApply = changingMod is not None and values['changeOptions'] != ''
            canDetail = values['detailOptions'] != ''
        except:
            pass

        if event == sg.WIN_CLOSED:
            break

        elif event == 'Apply Change' and canApply:
            newVal = callback_ApplyChange(window, values['changeOptions'])
            output = brf.user_change(changingMod, newVal, cm)
            cm = output[1]
            callback_UpdateMap(cm, mod_units, window)
            changingMod = None

        elif event in mod_units:
            if cm[event]['name'] != '':
                changingMod = event
                avails = brf.get_avails(changingMod, mod_units, cm)
                callback_UserChange(changingMod, avails, cm, window)

        elif event == 'Detail Chosen' and canDetail:
            mod = values['detailOptions']
            callback_Details(mod, cm)

        elif event == 'load':
            new_cm = callback_LoadMap()
            if new_cm is not None:
                cm = new_cm
                callback_UpdateMap(cm, mod_units, window)

        elif event == 'exit':
            fileName = callback_Save()
            if fileName == 'cancel':
                pass
            elif fileName == 'exit':
                window.close()
                break
            else:
                window.close()
                biomap = brf.print_bioprocess(output[0][0], output[0][1], output[0][2])
                brf.write_bioprocess(cm,
                                     mod_units,
                                     fileName,
                                     biomap)
                break


if __name__ == '__main__':

    # brf.write_json()
    main()
