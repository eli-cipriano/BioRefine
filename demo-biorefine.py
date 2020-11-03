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
               sg.Button('Apply Change')]
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


def callback_ApplyChange(currentMods, window):


def main(cm, modules, dicts, header=''):
    modValues = {'product': cm['product']['name'],
                 'process': cm['process']['name'],
                 'substrate': cm['substrate']['name'],
                 'material': cm['material']['name'],
                 'side1': cm['side1']['name'],
                 'sub1': cm['sub1']['name'],
                 'proc1': cm['proc1']['name'],
                 'prod1': cm['prod1']['name'],
                 'side2': cm['side2']['name'],
                 'sub2': cm['sub2']['name'],
                 'proc2': cm['proc2']['name'],
                 'prod2': cm['prod2']['name']
                 }
    window = sg.Window('Your Current Bioprocess', make_layout(modValues))

    while True:             # Event Loop
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        elif event == 'Apply Change':
            callback_ApplyChange(cm, window)
        elif event is not None:
            changingMod = event
            avails = brf.get_avails(changingMod, modules, cm, dicts)
            callback_UserChange(changingMod, avails, cm, window)


if __name__ == '__main__':

    # brf.write_json()
    dicts = brf.call_json()
    output = brf.user_build('ethanol',
                            dicts,
                            optimization=None,
                            filter=None
                            )
    currentMods = output[1]
    modules = ['product', 'process', 'substrate', 'material',
               'side1', 'sub1', 'proc1', 'prod1', 'boost1',
               'side2', 'sub2', 'proc2', 'prod2', 'boost2']

    main(currentMods, modules, dicts)
