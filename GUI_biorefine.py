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
        '                                                                     '

    tab1_layout = [[sg.Text(spacer+'                         '),
                    sg.Button('Help', key='bioprocess_help')],

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

                   # add spaces to prevent disappearing-text bug
                   [sg.Text('Change ____:                  ', key='changeMod')],

                   [sg.Combo(values=[''], key='changeOptions', size=(20, 1)),
                    sg.Button('Apply Change')],

                   [sg.Text('\n\n\n')],

                   [sg.Text(spacer),
                    sg.Button('Load Preset', key='load'),
                    sg.Button('Save & Quit', key='exit')]

                   ]

    tab2_layout = [[sg.T(spacer+'                         '),
                    sg.Button('Help', key='details_help')],

                   [sg.Text('See details for:')],

                   [sg.Combo(values=mod_units,
                             key='detailOptions', size=(20, 1)),
                    sg.Button('Enter', key='Detail Chosen')]]

    # TODO:
    # TRY TO UPDATE TAB2 TEXT INSTEAD OF USING A POPUP
    # [sg.Text('Details for _______:       \n\n\n\n\n\n\n\n\n\n\n',
    #          key='detailText')]]

    tab3_layout = [[sg.T(spacer+'                         '),
                    sg.Button('Help', key='custom_help')],

                   [sg.Text('Select conversion type:')],

                   [sg.Combo(values=['material', 'side', 'substrate'],
                             key='new_mod', size=(20, 1)),
                    sg.Button('Launch', key='Detail Chosen')], ]

    layout = [[sg.TabGroup([[sg.Tab('Bioprocess', tab1_layout),
                             sg.Tab('Details', tab2_layout),
                             sg.Tab('Custom', tab3_layout)]])]]

    return layout


def data_addition_layout(entry_type):
    """
    Allow users to add their own data entries
    """

    if entry_type == 'material':
        sg.popup('material')
    elif entry_type == 'side':
        sg.popup('side')
    elif entry_type == 'substrate':
        sg.popup('substrate')
    return None


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

    if fileName:
        # add default path and .json ext
        fileName = brf.default_path(fileName)
        jName, fileName = brf.get_file_ext('.json', fileName)
        # attempt to load in specified json
        try:
            with open(jName) as j:
                currentMods = json.load(j)
        except(FileNotFoundError):
            sg.popup('Error: File could not be opened')
            currentMods = None

    else:
        currentMods = 'cancel'

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

    # if user does not input a fileName
    elif fileName is None:
        fileName = 'cancel'
    elif fileName == '':
        fileName = 'exit'
    return fileName


def callback_Details(mod, currentMods, window):
    """
    sub function for receiving input from user on which module they would like
    to view detailed properties of.
    """
    detailMod = currentMods[mod]
    detailText = brf.print_Details(mod, currentMods)
    sg.popup(detailText)
    # window['detailText'].update('Details for {}:\n{}'.format(mod, detailText))


def callback_PrintHelp(help_type):
    """
    sub function for printing help documentation
    """
    if help_type == 'bioprocess':
        help_msg = 'Click a button to set which Modular Unit you would like to'\
            + ' change. Then select an option from the drop-down menu. Options will'\
            + ' only be available if they are compatible with neighboring Modular'\
            + ' Units. You can only change one Modular Unit at a time.\n'\
            + ' ------------------------------------------------------\n'\
            + ' Use the "Load" button to change the current map to a previously saved'\
            + ' Bioprocess. Use the "Save & Quit" button to save your current map.\n\n'\
            + ' * Files will automatically be saved/loaded to/from the processes/'\
            + ' directory, unless otherwise stated in the file path name.\n\n'\
            + ' *The file will save and load JSON files automatically, so do not'\
            + ' your own file extension.\n\n'\
            + ' *When quitting, press OK with no file name to exit without saving.'\
            + ' You can also close the window at any point to exit without saving.'\

    elif help_type == 'details':
        help_msg = 'Click which Modular Unit you want to see more detailed'\
            + ' information about. This information will also be written to a text'\
            + ' file upon saving.'

    elif help_type == 'custom':
        help_msg = 'Click which data type you would like to add to.\n\n'\
            + ' *Materials refer to information on converting raw biomass into'\
            + ' substrate compounds.\n\n'\
            + ' *Sides refer to information on converting by-products of materials'\
            + ' into useful substrates as well.\n\n'\
            + ' *Substrates refer to information on converting basic compounds into'\
            + ' more valuable and refined products.'

    help_window = sg.popup(help_msg)

    return None


def main():
    # initialize the bioprocess with default values
    try:
        cm = callback_LoadMap(fileName='.startup_DO-NOT-DELETE')

        if cm is None:
            raise FileNotFoundError

        # "change" cm so that the flows can also be initialized
        flows, cm = brf.user_change('prod2', cm['prod2']['name'], cm)

    except(FileNotFoundError):
        sg.popup('WARNING: No startup process detected.\nMaking new default.')
        flows, cm = brf.create_default()

    # After initializing:
    # make a list of all the module names
    mod_units = brf.get_mod_units()
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
            flows, cm = brf.user_change(changingMod, newVal, cm)
            callback_UpdateMap(cm, mod_units, window)
            changingMod = None

        elif event in mod_units:
            if cm[event]['name'] != '':
                changingMod = event
                avails = brf.get_avails(changingMod, mod_units, cm)
                callback_UserChange(changingMod, avails, cm, window)

        elif event == 'Detail Chosen' and canDetail:
            mod = values['detailOptions']
            callback_Details(mod, cm, window)

        elif event == 'load':
            new_cm = callback_LoadMap()
            if new_cm == 'cancel':
                pass
            elif new_cm is not None:
                cm = new_cm
                callback_UpdateMap(cm, mod_units, window)

        elif 'help' in event:
            help_type = event.split('_')
            callback_PrintHelp(help_type[0])

        elif event == 'exit':
            fileName = callback_Save()
            if fileName == 'cancel':
                pass
            elif fileName == 'exit':
                window.close()
                break
            else:
                window.close()
                biomap = brf.print_bioprocess(flows[0], flows[1], flows[2])
                brf.write_bioprocess(cm,
                                     fileName,
                                     mod_units=mod_units,
                                     biomap=biomap)
                break


if __name__ == '__main__':

    # brf.write_json()
    main()
