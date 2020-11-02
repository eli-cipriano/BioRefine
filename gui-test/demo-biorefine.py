import sys
import PySimpleGUI as sg

"""
This code can be run in a pysimple trinket.io
See: https://pysimplegui.trinket.io/demo-programs#/demo-programs/the-basic-pysimplegui-program
"""

def button_map(title, names):
    """
    formats a PySimpleGUI window to be input into PySimple's Window method.

    Parameters
    -------------
    title = string
      a string you want as the title of your pop-up window
    
    names = list of list of strings.
      a list of three lists, for three rows in the pop-up.
      each of the three list should contain the button names for that row. 
      FOR NOW, exactly four names necessary per line.

    Returns
    -------------
    produces input for a window of five lines, with four buttons in the 1st, 3rd, and 5th lines.
    """
    # Set up the buttons. 
    # Then add text for the results.  
    layout = [[sg.Text(title)],
          
          [sg.Button(names[0][0]), sg.Text(' --> '),
          sg.Button(names[0][1]), sg.Text(' --> '),
          sg.Button(names[0][2]), sg.Text(' --> '),
          sg.Button(names[0][3])],
          
          [sg.Text('      |  ')],
          
          [sg.Button(names[1][0]), sg.Text(' --> '),
          sg.Button(names[1][1]), sg.Text(' --> '),
          sg.Button(names[1][2]), sg.Text(' --> '),
          sg.Button(names[1][3])],
          
          [sg.Text('      |  ')],
          
          [sg.Button(names[2][0]), sg.Text(' --> '),
          sg.Button(names[2][1]), sg.Text(' --> '),
          sg.Button(names[2][2]), sg.Text(' --> '),
          sg.Button(names[2][3])]
          
          ]
    
    return layout

print_statement = [['1', ' --> ', '2', ' --> ', '3'],
                   ['1', ' --> ', '2', ' --> ', '3'],
                   ['1', ' --> ', '2', ' --> ', '3']]

def callback_function1():
    title = 'Modify side1. Choose from: \ngerm \ncellulose'
    list = 'germ, cellulose'
    entry = sg.popup_get_text(title)
    print_statement[0][0] = entry
    sg.popup('Results', print_statement)
    for i in print_statement:
      print(i)

def callback_function2():
    title = 'Modify sub1. Choose from: \nacetate \nglucose \nmethane'
    entry = sg.popup_get_text(title)
    print_statement[0][1] = entry
    sg.popup('Results', print_statement)
    for i in print_statement:
      print(i)

def callback_function3():
    title = 'Modify proc1. Choose from: \nclostridia \necoli_anaerobic \nmethanogenic \nyeast_anaerobic'
    entry = sg.popup_get_text(title)
    print_statement[0][2] = entry
    sg.popup('Results', print_statement)
    for i in print_statement:
      print(i)

def callback_function4():
    title = 'Modify prod1. Choose from: \nethanol \nisobutanol'
    entry = sg.popup_get_text(title)
    print_statement[0][3] = entry
    sg.popup('Results', print_statement)
    for i in print_statement:
      print(i)

def callback_function5():
    title = 'Modify material. Choose from: \ncorn \nsugar cane \nwheat'
    entry = sg.popup_get_text(title)
    print_statement[1][0] = entry
    sg.popup('Results', print_statement)
    for i in print_statement:
      print(i)

def callback_function6():
    title = 'Modify substrate. Choose from: \n glucose'
    entry = sg.popup_get_text(title)
    print_statement[1][1] = entry
    sg.popup('Results', print_statement)
    for i in print_statement:
      print(i)
    
def callback_function7():
    title = 'Modify process. Choose from: \n'
    entry = sg.popup_get_text(title)
    print_statement[1][2] = entry
    sg.popup('Results', print_statement)
    for i in print_statement:
      print(i)

def callback_function8():
    title = 'Modify product. Choose from: \n'
    entry = sg.popup_get_text(title)
    print_statement[1][3] = entry
    sg.popup('Results', print_statement)
    for i in print_statement:
      print(i)

def callback_function9():
    title = 'Modify side2. Choose from: \n'
    entry = sg.popup_get_text(title)
    print_statement[2][0] = entry
    sg.popup('Results', print_statement)
    for i in print_statement:
      print(i)

def callback_function10():
    title = 'Modify sub2. Choose from: \n'
    entry = sg.popup_get_text(title)
    print_statement[2][1] = entry
    sg.popup('Results', print_statement)
    for i in print_statement:
      print(i)

def callback_function11():
    title = 'Modify proc2. Choose from: \n'
    entry = sg.popup_get_text(title)
    print_statement[2][2] = entry
    sg.popup('Results', print_statement)
    for i in print_statement:
      print(i)

def callback_function12():
    title = 'Modify prod2. Choose from: \n'
    entry = sg.popup_get_text(title)
    print_statement[2][3] = entry
    sg.popup('Results', print_statement)
    for i in print_statement:
      print(i)

names = [['side1', 'sub1', 'proc1', 'prod1'],
         ['material', 'substrate', 'process', 'product'],
         ['side2', 'sub2', 'proc2', 'prod2']]

window = sg.Window('Button Callback Simulation', button_map("Your Processes Map", names))

while True:             # Event Loop
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break
    elif event == names[0][0]:
        callback_function1()        # call the "Callback" function
    elif event == names[0][1]:
        callback_function2()        # call the "Callback" function
    elif event == names[0][2]:
        callback_function3()
    elif event == names[0][3]:
        callback_function4()
    elif event == names[1][0]:
        callback_function5()        # call the "Callback" function
    elif event == names[1][1]:
        callback_function6()        # call the "Callback" function
    elif event == names[1][2]:
        callback_function7()
    elif event == names[1][3]:
        callback_function8()
    elif event == names[2][0]:
        callback_function9()        # call the "Callback" function
    elif event == names[2][1]:
        callback_function10()        # call the "Callback" function
    elif event == names[2][2]:
        callback_function11()
    elif event == names[2][3]:
        callback_function12()

window.close()