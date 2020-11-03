import sys
import PySimpleGUI as sg
import bioreflib as brf

"""
This code can be run in a pysimple trinket.io
See: https://pysimplegui.trinket.io/demo-programs#/demo-programs/the-basic-pysimplegui-program
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
      FOR NOW, exactly four modValues necessary per line.

    Returns
    -------------
    produces input for a window of five lines, with four buttons in the 1st, 3rd, and 5th lines.
    """
    sg.theme('DarkAmber')
    divider = '---------------------------------------------------------------'\
        '---------------------------------------------------------------'
    spacer = '                                                                '\
        '                                                       '

    # Set up the buttons.
    # Then add text for the results.

    layout = [[sg.Text(header)],
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

    return layout


def callback_UserChange(changingMod, avails, currentMods, window):
    print(changingMod)
    title = 'Change {}:'.format(changingMod)
    window['changeMod'].update(title)
    # add clear option for sideFlows
    if changingMod[0:4] == 'side':
        avails.append('none')
    window['changeOptions'].update(values=avails)
    window['changeOptions'].update(' ')


def callback_ApplyChange(window, newVal):
    window['changeMod'].update('Change ___:')
    window['changeOptions'].update(values=[''])

    return newVal


def callback_UpdateMap(cm, modules, window):
    for mod in modules:
        if mod[0:5] != 'boost':
            window[mod].update(cm[mod]['name'])


def main(cm, modules, header='', changingMod=None):
    modValues = {}
    for mod in modules:
        if mod[0:5] != 'boost':
            modValues[mod] = cm[mod]['name']

    window = sg.Window('Your Current Bioprocess', make_layout(modValues))

    while True:             # Event Loop
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break

        elif event == 'Apply Change' and changingMod is not None:
            newVal = callback_ApplyChange(window, values['changeOptions'])
            output = brf.user_change(changingMod, newVal, cm)
            cm = output[1]
            brf.print_bioprocess(output[0][0], output[0][1], output[0][2])
            for key, vals in cm.items():
                print(key, ':', vals)
            callback_UpdateMap(cm, modules, window)
            changingMod = None

        elif event in modules:
            changingMod = event
            avails = brf.get_avails(changingMod, modules, cm)
            callback_UserChange(changingMod, avails, cm, window)


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

    main(currentMods, modules)
