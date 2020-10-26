"""
This is the main UI file for running/using BioRefine, bioreflib.
It allows the user to view and change the Modules of the bioprocess, which are
the discrete units of the bioprocess. For instance, the Module 'material' might
have the value, 'corn', or the Module 'process' might have the value
'anaerobic_yeast'. The following diagram shows the label of each Module, which
can be used by the user to specify which Module they wish to act on.

-------------------------------------------------------------------------------
side1  -> sub1  -> proc1  -> prod1
  |
material -> substrate -> process -> product
  |
side2  -> sub2  -> proc2  -> prod2
-------------------------------------------------------------------------------
Use the built-in help function for more detail on how to manipulate and view
aspects of the Modules.
"""

import os
import sys
import json
import argparse
import bioreflib as br

# TODO: fix get_avails function
# TODO: fix user_change to eliminate extra sideFLows (germ from sugar cane, etc)


def main():
    # use argparse to define inputs
    parser = argparse.ArgumentParser(
        description='Prints cases/deaths for a given county/state',
        prog='print_cases'
    )

    parser.add_argument('--product',
                        dest='product',
                        type=str,
                        help='Name of desired product',
                        required=True)

    parser.add_argument('--file',
                        dest='file',
                        type=str,
                        help='Name of output json file',
                        required=True)

    parser.add_argument('--opt',
                        dest='optimization',
                        type=str,
                        help='Basis of optimization:'
                        ' edges, product, material',
                        required=False)

    parser.add_argument('--filter',
                        dest='filter',
                        type=str,
                        nargs='+',
                        help='List of filters to apply to options:'
                        ' perrenials, cropYield, sugarless, anaerobic, co-prod',
                        required=False)

# parse arguments and check for formatting
    args = parser.parse_args()
    product = args.product.lower()
    opt = args.optimization
    filt = args.filter
    fileName = args.file

    if opt is not None:
        opt = opt.lower()
    if filt is not None:
        filt = filt.lower()
# check that if an extension was included, that it is a json
    try:
        if fileName[-5:len(fileName)] != '.json':
            fileName += '.json'
    except:
        fileName += '.json'


# use write_json to update dictionaries with new values.
# currently, this will shuffle the order due to the "set" function
# only use when dictionaries need to be updated.
    # br.write_json()
# use call_json to load in the dictionaries containing our modules
    dicts = br.call_json()
# use user_build to make an initial bioprocess for a given product
    output = br.user_build(product,
                           dicts,
                           optimization=opt,
                           filter=filt
                           )

    currentMods = output[1]  # dict with current module values
    mainFlow = output[0][0]  # string for main process
    sideFlow1 = output[0][1]  # string for side process 1
    sideFlow2 = output[0][2]  # string for side process 2

    modules = ['product', 'process', 'substrate', 'material',
               'side1', 'sub1', 'proc1', 'prod1', 'boost1',
               'side2', 'sub2', 'proc2', 'prod2', 'boost2']
# plot the output and enter the decision loop
    os.system('clear')
    br.print_bioprocess(mainFlow, sideFlow1, sideFlow2)

    while True:
        instruct = input('\nType "help" for a list of commands.\n\ncmd: ')
        print('User:', instruct)
        os.system('clear')
        br.print_bioprocess(mainFlow, sideFlow1, sideFlow2)

        if instruct.lower() == 'help':
            print('-------------------------------------------------------'
                  '------------------------')
            print('EXIT:            EXIT quits with the currently presented'
                  ' bioprocess.')

            print('\nVIEW [MODULE]:   VIEW shows all the available'
                  ' options for a specified module.\n'
                  '                 Modules are the types  of '
                  ' steps in the bioprocess. \n'
                  '                 Type "view help" for more details.')

            print('\nCHANGE [MODULE]: CHANGE shows all available options for a'
                  ' specified module,\n'
                  '                 which you can then select from and'
                  ' apply the change to the \n'
                  '                 current bioprocess.\n'
                  '                 Type "change help" for more details.\n'
                  '                 WARNING: This change could impact'
                  ' other modules in the process.')

            print('\nDETAIL[MODULE]:  DETAIL shows values associated with the'
                  ' characterization of \n'
                  '                 that module. This allows you to view'
                  ' things like process \n'
                  '                 efficiency, crop density, product value,'
                  ' etc. for each module \n'
                  '                 in the current process.\n'
                  '                 Type "detail help" for more details.')

            print('\nOPTIM [TYPE]:    OPTIM allows you to change the type of'
                  ' optimization used for \n'
                  '                 determining the initial bioprocess.\n'
                  '                 Type "optim help" for more details.')

            print('\nFILT [TYPE]:     FILT allows you to change the type of'
                  ' filter used for \n'
                  '                 determining the initial bioprocess.\n'
                  '                 Type "filt help" for more details.')

            print('-------------------------------------------------------'
                  '------------------------')

        elif instruct.lower().strip() == 'exit':
            # quit the UI loop and create output file
            br.write_bioprocess(currentMods, fileName)
            break

        elif instruct.lower()[0:4] == 'view':
            # show list of available options
            mod = read_input(instruct, modules)  # extract command from user

            if mod == 'help':
                print('-------------------------------------------------------'
                      '------------------------')
                print('VIEW HELP: \n\nType "view [MODULE]" to see a list of'
                      ' available options.\n\nList of Module labels:')
                for module in modules:
                    print(module)
                print('-------------------------------------------------------'
                      '------------------------')
            elif mod in modules:
                # use get_avails to generate list of available options
                print('-------------------------------------------------------'
                      '------------------------')
                avails = br.get_avails(mod, modules, currentMods, dicts)  # list
                if avails is not None:
                    for a in avails:
                        print(a)
                print('-------------------------------------------------------'
                      '------------------------')

        elif instruct.lower()[0:6] == 'change':
            # show list of available options and ask user for input
            mod = read_input(instruct, modules)  # extract command from user

            if mod == 'help':
                print('-------------------------------------------------------'
                      '------------------------')
                print('CHANGE HELP: \n\nType "change [MODULE]" to change the'
                      ' value of a specific module to a new value\nfrom a list'
                      ' of available options.\n\nList of Module labels:')
                for module in modules:
                    print(module)
                print('-------------------------------------------------------'
                      '------------------------')

            elif mod in modules:
                # use get_avails to generate list of available options
                # use user_change to update the current bioproecess
                print('-------------------------------------------------------'
                      '------------------------')
                avails = br.get_avails(mod, modules, currentMods, dicts)  # list
                while True:
                    # keep user in input mode until valid input received
                    for a in avails:
                        print(a)
                    print('----------------------------------------------------'
                          '---------------------------')
                    newVal = input('\nEnter new value from above:\n\ncmd: ')
                    if newVal in avails:
                        # valid input, proceed with user_change
                        print('\nCHANGED: {} to {}'
                              .format(mod.upper(),
                                      newVal.upper()))

                        output = br.user_change(mod, currentMods, newVal, dicts)
                        currentMods = output[1]
                        mainFlow = output[0][0]
                        sideFlow1 = output[0][1]
                        sideFlow2 = output[0][2]
                        os.system('clear')
                        br.print_bioprocess(mainFlow, sideFlow1, sideFlow2)
                        break

                    elif newVal == '':
                        # empy input, return to home
                        os.system('clear')
                        br.print_bioprocess(mainFlow, sideFlow1, sideFlow2)
                        break
                    else:
                        # invalid entry, try again
                        os.system('clear')
                        print('Invalid entry: Please try again.')
                        br.print_bioprocess(mainFlow, sideFlow1, sideFlow2)

        elif instruct.lower()[0:6] == 'detail':
            # display properties of the specified Module
            mod = read_input(instruct, modules)  # extract command from user

            if mod == 'help':
                print('-------------------------------------------------------'
                      '------------------------')
                print('detail help...')
                print('-------------------------------------------------------'
                      '------------------------')

            elif mod in modules:
                print('-------------------------------------------------------'
                      '------------------------')
                detailMod = currentMods[mod]
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
                        val = val[key]['strains']
                        print('\n', key+': ')
                        for strain in val:
                            print('\n       ', strain)

                    elif key == 'treatments':
                        # list treatment options line by line
                        pass

                    else:
                        # print field of detailMod
                        print(key+': {}'.format(val))


def read_input(instruct, modules):
    # cmd = input, modules = list of Module labels (12)
    cmd = instruct.lower().split(' ')  # list of terms entered by user

    # handle mis-inputs
    if len(cmd) <= 1:
        cmd.append('help')
    elif len(cmd) > 1 and cmd[1] not in modules:
        cmd[1] = 'help'
    mod = cmd[1]
    return mod


if __name__ == '__main__':
    main()
