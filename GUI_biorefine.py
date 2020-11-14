import sys
import PySimpleGUI as sg
import bioreflib as brf

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


def make_layout(modValues, modules, header=''):
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
        '                                                       '

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
                    sg.Button('Save & Quit', key='exit')]
                   ]

    tab2_layout = [[sg.T('Get Details')],

                   [sg.Text('See details for:')],

                   [sg.Combo(values=modules,
                             key='detailOptions', size=(20, 1)),
                    sg.Button('Enter', key='Detail Chosen')], ]

    layout = [[sg.TabGroup([[sg.Tab('Bioprocess', tab1_layout),
                             sg.Tab('Details', tab2_layout)]])]]

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
    # Why is there are values and value? Why are both empty? #
    window['changeMod'].update('Change ___:')
    window['changeOptions'].update(values=[''])
    window['changeOptions'].update(value='')
    # clearwindow['header'].update('Changed to {}...'.format(newVal))
    return newVal  # where does newVal go?


def callback_UpdateMap(cm, modules, window):
    for mod in modules:
      # Boost is not implemented yet, just a potential way to link different
      # bioprocesses together via sideFlows
        if mod[0:5] != 'boost':
            # Updates a mod of the window . . .
            window[mod].update(cm[mod]['name'])


def callback_Save():
    fileName = sg.popup_get_text('Save Bioprocess As:', 'File Saver')
    print(fileName)
    if fileName:
        fileName = fileName.strip(' ')
        if 'json' not in fileName.split('.'):
            fileName = ''.join([fileName, '.json'])
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
    detailText = print_Details(detailMod, mod, currentMods)
    detailPopup = sg.popup(detailText)


def print_Details(detailMod, mod, currentMods):
    detailText = ''
    for key, val in detailMod.items():
        if key == 'subprods':
            # list strain options line by line
            if mod == 'process':
                prod = currentMods['product']['name']
                sub = currentMods['substrate']['name']
            elif mod == 'proc1':
                prod = currentMods['prod1']['name']
                sub = currentMods['sub1']['name']
            elif mod == 'proc2':
                prod = currentMods['prod2']['name']
                sub = currentMods['sub2']['name']
            key = '2'.join([sub, prod])
            strains = val[key]['strains']
            detailText += '\n{}: '.format(key)
            for strain in strains:
                detailText += '\n       {}'.format(strain)

        elif key == 'treatments':
            # list treatment options line by line
            pass

        else:
            # print field of detailMod
            detailText += '{}: {}\n'.format(key, val)

    return detailText


def main():
    # initialize the bioprocess with default values
    output = brf.user_build('ethanol',
                            optimization=None,
                            filter=None
                            )
    cm = output[1]
    # make a list of all the module names
    modules = ['product', 'process', 'substrate', 'material',
               'side1', 'sub1', 'proc1', 'prod1', 'boost1',
               'side2', 'sub2', 'proc2', 'prod2', 'boost2']
    # store current module values for updating button names
    modValues = {}
    # to begin, no module is specified for change
    changingMod = None

    for mod in modules:
        if mod[0:5] != 'boost':
            # Here's this line again. What does it do?
            modValues[mod] = cm[mod]['name']

    window = sg.Window('Your Current Bioprocess', make_layout(modValues, modules))

    while True:  # Event Loop
        event, values = window.read()
        try:
            # check that conditions are met for input actions
            canApply = changingMod is not None and values['changeOptions'] != ''
            canDetail = values['detailOptions'] != ''
        except:
            pass

        if event == sg.WIN_CLOSED:
            break

        #
        elif event == 'Apply Change' and canApply:
            newVal = callback_ApplyChange(window, values['changeOptions'])
            output = brf.user_change(changingMod, newVal, cm)
            cm = output[1]
            callback_UpdateMap(cm, modules, window)
            changingMod = None

        elif event in modules:
            if cm[event]['name'] != '':
                changingMod = event
                avails = brf.get_avails(changingMod, modules, cm)
                callback_UserChange(changingMod, avails, cm, window)

        elif event == 'Detail Chosen' and canDetail:
            mod = values['detailOptions']
            detailMod = cm[mod]
            callback_Details(detailMod, mod, cm)

        elif event == 'exit':
            fileName = callback_Save()
            if fileName == 'cancel':
                pass
            elif fileName == 'exit':
                window.close()
                break
            else:
                window.close()
                brf.print_bioprocess(output[0][0], output[0][1], output[0][2])
                brf.write_bioprocess(cm, fileName)
                break


if __name__ == '__main__':

    # brf.write_json()
    main()
