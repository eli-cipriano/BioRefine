import sys
import PySimpleGUI as sg
import bioreflib as brf

"""
This code can be run in a pysimple trinket.io
See: https://pysimplegui.trinket.io/demo-programs#/demo-programs/the-basic-pysimplegui-program

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


def make_layout(modValues, header=''):
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

                   [sg.Text('See details for:', key='changeDetails')],

                   [sg.Combo(values=['Coming Soon :)'],
                             key='changeOptionsDetail', size=(20, 1)),
                    sg.Button('Enter')], ]

    layout = [[sg.TabGroup([[sg.Tab('Tab 1', tab1_layout),
                             sg.Tab('Tab 2', tab2_layout)]])]]

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
    #clearwindow['header'].update('Changed to {}...'.format(newVal))
    return newVal  # where does newVal go?


def callback_UpdateMap(cm, modules, window):
    for mod in modules:
      # What does boost do? #
        if mod[0:5] != 'boost':
            # Updates a mod of the window . . .
            window[mod].update(cm[mod]['name'])


def callback_Save():
    fileName = sg.popup_get_text('Save Bioprocess As:', 'File Saver')
    if fileName:
        fileName = fileName.strip(' ')
        if 'json' not in fileName.split('.'):
            fileName = ''.join([fileName, '.json'])
    else:
        fileName = 'exit'
    return fileName


def main(cm, modules, output, changingMod=None):
    modValues = {}
    for mod in modules:
        if mod[0:5] != 'boost':
          # Here's this line again. What does it do? #
            modValues[mod] = cm[mod]['name']

    window = sg.Window('Your Current Bioprocess', make_layout(modValues))

    while True:             # Event Loop
        event, values = window.read()

        # check that conditions are met for applying changes
        canApply = changingMod is not None and values['changeOptions'] != ''

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

        elif event == 'exit':
            fileName = callback_Save()
            window.close()
            if fileName != 'exit':
                brf.print_bioprocess(output[0][0], output[0][1], output[0][2])
                brf.write_bioprocess(cm, fileName)
            break


if __name__ == '__main__':

    # brf.write_json()
    output = brf.user_build('ethanol',
                            optimization=None,
                            filter=None
                            )
    currentMods = output[1]
    modules = ['product', 'process', 'substrate', 'material',
               'side1', 'sub1', 'proc1', 'prod1', 'boost1',
               'side2', 'sub2', 'proc2', 'prod2', 'boost2']

    main(currentMods, modules, output)
