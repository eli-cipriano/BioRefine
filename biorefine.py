"""
This is the main UI file for running/using BioRefine, bioreflib
"""

import os
import sys
import json
import argparse
import bioreflib as bl
import biorefbuild as bb


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
                        help='Name of writing file',
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
    try:
        if fileName[-5:len(fileName)] != '.json':
            fileName += '.json'
    except:
        fileName += '.json'

# use user_build to initialize the bioprocess
    dicts = bb.call_json()
    output = bl.user_build(product,
                           dicts,
                           optimization=opt,
                           filter=filt
                           )

    currentMods = output[1]
    mainFlow = output[0][0]
    sideFlow1 = output[0][1]
    sideFlow2 = output[0][2]

    modules = ['product', 'process', 'substrate', 'material',
               'side1', 'sub1', 'proc1', 'prod1', 'boost1',
               'side2', 'sub2', 'proc2', 'prod2', 'boost2']
# plot the output and enter the decision loop
    os.system('clear')
    print_bioprocess(mainFlow, sideFlow1, sideFlow2)

    while True:

        instruct = input('\nType "help" for a list of commands.\n\ncmd: ')
        os.system('clear')
        print_bioprocess(mainFlow, sideFlow1, sideFlow2)

        if instruct.lower() == 'help':
            print('-------------------------------------------------------'
                  '------------------------')
            print('EXIT:            EXIT quits with the currently presented'
                  ' bioprocess.')

            print('\nVIEW [MODULE]:   VIEW shows all the available'
                  ' options for a specified module. Modules are the types'
                  ' of steps in the bioprocess. Type "view help"'
                  ' for more details.')

            print('\nCHANGE [MODULE]: CHANGE shows all available options for a'
                  ' specified modules, which you can then select from and'
                  ' apply the change to the currentbioprocess.'
                  ' Type "change help" for more details.\n'
                  '                 WARNING: This change could impact'
                  ' other modules in the process.')

            print('\nDETAIL[MODULE]: DETAIL shows values associated with the
                  ' characterization of that module. This allows you to view'
                  ' things like process efficiency, crop density, product'
                  ' value, etc. for each module in the current process.'
                  ' Type "detail help" for more details.'
                  ' other modules in the process.')

            print('\nOPTIM [TYPE]:    OPTIM allows you to change the type of'
                  ' optimization used for determining the initial bioprocess.'
                  ' Type "optim help" for more details.')

            print('\nFILT [TYPE]:     FILT allows you to change the type of'
                  ' filter used for determining the initial bioprocess.'
                  ' Type "filt help" for more details.')

            print('-------------------------------------------------------'
                  '------------------------')

        elif instruct.lower() == 'exit':
            write_bioprocess(currentMods, fileName)
            break

        elif instruct.lower()[0:4] == 'view':
            cmd = instruct.split(' ')

            if len(cmd) <= 1:
                cmd.append('help')
            mod = cmd[1]

            if mod == 'help':
                print('-------------------------------------------------------'
                      '------------------------')
                print('view help...')
                print('-------------------------------------------------------'
                      '------------------------')
            elif mod in modules:
                print('-------------------------------------------------------'
                      '------------------------')
                avails = get_avails(mod, modules, currentMods)
                if avails is not None:
                    for a in avails:
                        print(a)

        elif instruct.lower()[0:6] == 'detail':
            cmd = instruct.split(' ')
            if len(cmd) <= 1:
                cmd.append('help')
            mod = cmd[1]

        elif instruct.lower()[0:6] == 'change':
            cmd = instruct.split(' ')
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

            if len(cmd) <= 1:
                cmd.append('help')
            mod = cmd[1]

            if mod == 'help':
                print('-------------------------------------------------------'
                      '------------------------')
                print('change help...')
                print('-------------------------------------------------------'
                      '------------------------')

            elif mod in modules:
                print('-------------------------------------------------------'
                      '------------------------')
                avails = get_avails(mod, modules, currentMods)
                for a in avails:
                    print(a)
                newVal = input('\nEnter new value from above:\n\ncmd: ')
                print('\nCHANGED: {} from {} to {}'
                      .format(mod.upper(),
                              currentMods[mod]['name'].upper(),
                              newVal.upper()))

                output = bl.user_change(mod, currentMods, newVal, dicts)
                currentMods = output[1]
                mainFlow = output[0][0]
                sideFlow1 = output[0][1]
                sideFlow2 = output[0][2]
                os.system('clear')
                print_bioprocess(mainFlow, sideFlow1, sideFlow2)


def print_bioprocess(mainFlow, sideFlow1, sideFlow2):
    print('-------------------------------------------------------'
          '------------------------')
    print(sideFlow1)
    print('  |  ')
    print(mainFlow)
    print('  |  ')
    print(sideFlow2)
    print('-------------------------------------------------------'
          '------------------------')
    return None


def write_bioprocess(currentMods, fileName):
    with open(fileName, 'w') as f:
        json.dump(currentMods, f)
    return None


def get_avails(module, modules, currentMods):
    avails = []
    if module in modules[0:4]:
        if module == 'product':
            avails = get_availProducts()
        elif module == 'process':
            avails = currentMods['product']['processes']
        elif module == 'substrate':
            subprods = currentMods['process']['subprods']
            product = currentMods['product']['name']
            avails = []
            for key, val in subprods.items():
                sub, prod = key.split('2')
                if prod == product:
                    avails.append(sub)
        elif module == 'material':
            avails = currentMods['substrate']['materials']
        return avails

    else:
        print('sideFlows coming soon!')
        return None

    return None


if __name__ == '__main__':
    main()
