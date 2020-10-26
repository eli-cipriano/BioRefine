import sys
import json
import biorefbuild as bb


def user_build(product, dicts, optimization=None, filter=None):
    currentMods = {}
    PRODUCTS = dicts.get('PRODUCTS')
    PROCESSES = dicts.get('PROCESSES')
    SUBSTRATES = dicts.get('SUBSTRATES')
    MATERIALS = dicts.get('MATERIALS')
    SIDES = dicts.get('SIDES')

    ar = ' -> '
    currentMods['product'] = PRODUCTS.get(product)
    if optimization is None and filter is None:
        process = PRODUCTS.get(product).get('processes')[0]
        for key, val in PROCESSES.get(process).get('subprods').items():
            sub, prod = key.split('2')
            if prod == product:
                substrate = sub
                break
        material = SUBSTRATES.get(substrate).get('materials')[0]

        mainFlow = material + ar + substrate + ar + process + ar + product
        currentMods['process'] = PROCESSES.get(process)
        currentMods['substrate'] = SUBSTRATES.get(substrate)
        currentMods['material'] = MATERIALS.get(material)

        currentMods = replace_sideFlow('side1', currentMods)
        currentMods = replace_sideFlow('side2', currentMods)

        side1 = MATERIALS.get(material).get('sides')[0]
        side2 = MATERIALS.get(material).get('sides')[1]
        sideFlow1, sideFlow2 = '', ''

        if side1 != 'NA':
            sub1 = SIDES.get(side1).get('substrates')[0]
            proc1 = SUBSTRATES.get(sub1).get('processes')[0]
            for key, val in PROCESSES.get(proc1).get('subprods').items():
                sub, prod = key.split('2')
                if sub == sub1:
                    prod1 = prod
                    break

            sideFlow1 = side1 + ar + sub1 + ar + proc1 + ar + prod1
            currentMods['side1'] = SIDES.get(side1)
            currentMods['sub1'] = SUBSTRATES.get(sub1)
            currentMods['proc1'] = PROCESSES.get(proc1)
            currentMods['prod1'] = PRODUCTS.get(prod1)

        if side2 != 'NA':
            sub2 = SIDES.get(side2).get('substrates')[0]
            proc2 = SUBSTRATES.get(sub2).get('processes')[0]
            for key, val in PROCESSES.get(proc2).get('subprods').items():
                sub, prod = key.split('2')
                if sub == sub2:
                    prod2 = prod
                    break

            sideFlow2 = side2 + ar + sub2 + ar + proc2 + ar + prod2
            currentMods['side2'] = SIDES.get(side2)
            currentMods['sub2'] = SUBSTRATES.get(sub2)
            currentMods['proc2'] = PROCESSES.get(proc2)
            currentMods['prod2'] = PRODUCTS.get(prod2)

    else:
        print('Optimization and Filtering options coming soon!')
        sys.exit(0)

    return [[mainFlow, sideFlow1, sideFlow2], currentMods]


def user_change(changingMod, currentMods, newVal, dicts):
    # extract main dicts:
    PRODUCTS = dicts.get('PRODUCTS')
    PROCESSES = dicts.get('PROCESSES')
    SUBSTRATES = dicts.get('SUBSTRATES')
    MATERIALS = dicts.get('MATERIALS')
    SIDES = dicts.get('SIDES')

    # extract current state of network
    # maybe these can be objects with properties? Or just dicts?
    product = currentMods.get('product')
    process = currentMods.get('process')
    substrate = currentMods.get('substrate')
    material = currentMods.get('material')
    side1 = currentMods.get('side1')
    sub1 = currentMods.get('sub1')
    proc1 = currentMods.get('proc1')
    prod1 = currentMods.get('prod1')
    boost1 = currentMods.get('boost1')
    side2 = currentMods.get('side2')
    sub2 = currentMods.get('sub2')
    proc2 = currentMods.get('proc2')
    prod2 = currentMods.get('prod2')
    boost2 = currentMods.get('boost2')

    # begin process of updating network based on user change
    if changingMod == 'product':
        # mod, nextMod = 'product', 'process'
        # field, dictName = 'PRODUCTS', 'processes'
        # output = match_mods(currentMods, changingMod, mod, newVal,
        #                     nextMod, field, dictName)
        # currentMods = output[0]
        # changingMod = output[1]
        # newVal = output[2]

        # change product to new newVal
        newDict = PRODUCTS.get(newVal)
        # newDict should now be a dictionary containing product-related keys
        currentMods['product'] = newDict
        # if new product fits with current process, we're done!
        if process['name'] not in newDict.get('processes'):
            changingMod = 'process'
            # defaults to first, but could be optimized with AI later on
            newVal = newDict.get('processes')[0]

    if changingMod == 'process':
        # mod, nextMod = 'product', 'process'
        # field, dictName = 'PRODUCTS', 'processes'
        # currentMods = match_mods(currentMods, changingMod, mod, newVal,
        #                          nextMod, field, dictName)
        # change process to new newVal
        newDict = PROCESSES.get(newVal)
        currentMods['process'] = newDict
        # if new process fits with current substrate, we're done!
        if substrate['name'] not in newDict.get('substrates'):
            changingMod = 'substrate'
            newVal = newDict.get('substrates')[0]

    if changingMod == 'substrate':
        # change substrate to new newVal
        newDict = SUBSTRATES.get(newVal)
        currentMods['substrate'] = newDict
        # if new substrate fits with current material, we're done!
        if material['name'] not in newDict.get('materials'):
            changingMod = 'material'
            newVal = newDict.get('materials')[0]

    if changingMod == 'material':
        # change material to new newVal
        newDict = MATERIALS.get(newVal)
        currentMods['material'] = newDict
        # check both possible branches for side products
        if side1:
            if side1['name'] not in newDict.get('sides'):
                newVal = newDict.get('sides')[0]
                if newVal != 'NA':
                    changingMod = 'side1'
                else:
                    currentMods = replace_sideFlow('side1', currentMods)

    if changingMod == 'side1':
        # change side1 to new newVal
        newDict = SIDES.get(newVal)
        currentMods['side1'] = newDict
        # if new substrate fits with current side1, we're done!
        if sub1['name'] not in newDict.get('substrates'):
            changingMod = 'sub1'
            newVal = newDict.get('substrates')[0]

    if changingMod == 'sub1':
        # change side1 to new newVal
        newDict = SUBSTRATES.get(newVal)
        currentMods['sub1'] = newDict
        # if new substrate fits with current material, we're done!
        if proc1['name'] not in newDict.get('processes'):
            changingMod = 'proc1'
            newVal = newDict.get('processes')[0]

    if changingMod == 'proc1':
        # change side1 to new newVal
        newDict = PROCESSES.get(newVal)
        currentMods['proc1'] = newDict
        # if new substrate fits with current material, we're done!
        for key, val in newDict.get('subprods').items():
            sub, prod = key.split('2')
            sub1 = currentMods['sub1']
            if prod == prod1['name'] and sub == sub1['name']:
                changingMod = 'side2'
                break
            else:
                changingMod = 'prod1'
            if sub == sub1['name']:
                newVal = prod

    if changingMod == 'prod1':
        #
        newDict = PRODUCTS.get(newVal)
        currentMods['prod1'] = newDict
        materialDict = MATERIALS.get(currentMods['material']['name'])
        #
        if side2:
            if side2['name'] not in materialDict.get('sides'):
                newVal = materialDict.get('sides')[0]
                if newVal != 'NA':
                    changingMod = 'side2'
                else:
                    currentMods = replace_sideFlow('side2')

    ar = ' -> '
    product = currentMods.get('product').get('name')
    process = currentMods.get('process').get('name')
    substrate = currentMods.get('substrate').get('name')
    material = currentMods.get('material').get('name')

    sideFlow1, sideFlow2 = '', ''
    if currentMods['side1'] is not None:
        side1 = currentMods.get('side1').get('name')
        sub1 = currentMods.get('sub1').get('name')
        proc1 = currentMods.get('proc1').get('name')
        prod1 = currentMods.get('prod1').get('name')
        # boost1 = currentMods.get('boost1').get('name')
        sideFlow1 = side1 + ar + sub1 + ar + proc1 + ar + prod1
    if currentMods['side2'] is not None:
        side2 = currentMods.get('side2').get('name')
        sub2 = currentMods.get('sub2').get('name')
        proc2 = currentMods.get('proc2').get('name')
        prod2 = currentMods.get('prod2').get('name')
        # boost2 = currentMods.get('boost2').get('name')
        sideFlow2 = side2 + ar + sub2 + ar + proc2 + ar + prod2

    mainFlow = material + ar + substrate + ar + process + ar + product

    return [[mainFlow, sideFlow1, sideFlow2], currentMods]


def match_mods(currentMods, changingMod, mod, newVal, nextMod, field, dictName):
    if changingMod == mod:
        # change mod to new newVal
        newDict = eval('{}.get(newVal)'.format(dictName.upper()))
        currentMods[mod] = newDict
        # if nextMod is compatible with mod.field, we're done
        eval("if {}['name'] not in newDict.get({}):".format(nextMod, field))
        changingMod = nextMod
        newVal = newDict.get(field)[0]

    return [currentMods, changingMod, newVal]


def replace_sideFlow(side, currentMods):
    if side == 'side1':
        currentMods['side1'] = None
        currentMods['sub1'] = None
        currentMods['proc1'] = None
        currentMods['prod1'] = None
        currentMods['boost1'] = None
    elif side == 'side2':
        currentMods['side2'] = None
        currentMods['sub2'] = None
        currentMods['proc2'] = None
        currentMods['prod2'] = None
        currentMods['boost2'] = None
    return currentMods


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


def get_avails(module, modules, currentMods, dicts):
    avails = []
    if module in modules[0:4]:
        if module == 'product':
            avails = list(dicts.get('PRODUCTS').keys())
        elif module == 'process':
            avails = currentMods['product']['processes']
        elif module == 'substrate':
            subprods = currentMods['process']['subprods']
            product = currentMods['product']['name']
            for key, val in subprods.items():
                sub, prod = key.split('2')
                if prod == product:
                    avails.append(sub)
        elif module == 'material':
            avails = currentMods['substrate']['materials']
        return avails

    elif module in modules[4:14]:
        if module in ['prod1', 'prod2']:
            if module == 'prod1':
                subprods = currentMods['proc1']['subprods']
                substrate = currentMods['sub1']['name']
            elif module == 'prod2':
                subprods = currentMods['proc2']['subprods']
                substrate = currentMods['sub2']['name']
            for key, val in subprods.items():
                sub, prod = key.split('2')
                if sub == substrate:
                    avails.append(prod)
        elif module in ['proc1', 'proc2']:
            if module == 'proc1':
                avails = currentMods['prod1']['processes']
            elif module == 'proc2':
                avails = currentMods['prod2']['processes']
        elif module in ['sub1', 'sub2']:
            if module == 'sub1':
                avails = currentMods['proc1']['substrates']
            elif module == 'sub2':
                avails = currentMods['proc2']['substrates']
        elif module in ['side1', 'side2']:
            avails = currentMods['material']['sides']
        return avails
