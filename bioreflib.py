import biorefbuild as bb
import sys


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

        side1 = MATERIALS.get(material).get('sides')[0]
        side2 = MATERIALS.get(material).get('sides')[1]

        if side1 != 'none':
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

        if side2 != 'none':
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

    if side1 is None and side2 is None:
        changingMod1 = []
        changingMod2 = []
        noSides = True
    else:
        noSides = False

    # begin process of updating network based on user change
    if changingMod == 'product':
        # change product to new newVal
        newDict = PRODUCTS.get(newVal)
        # newDict should now be a dictionary containing product-related keys
        # maybe consider converting this dictionary into an object??
        currentMods['product'] = newDict
        # if new product fits with current process, we're done!
        if process['name'] not in newDict.get('processes'):
            changingMod = 'process'
            # defaults to first, but could be optimized with AI later on
            newVal = newDict.get('processes')[0]

    if changingMod == 'process':
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
            changingMod1 = []
            if side1['name'] not in newDict.get('sides'):
                changingMod1 = 'side1'
                newVal = newDict.get('sides')[0]
        if side2:
            changingMod2 = []
            if side2['name'] not in newDict.get('sides') \
                    and len(newDict.get('sides')) > 1:
                changingMod2 = 'side2'
                newVal = newDict.get('sides')[1]

    else:
        changingMod1 = []
        changingMod2 = []

    if changingMod1 == 'side1':
        pass

    if changingMod2 == 'side2':
        pass

    ar = ' -> '
    product = currentMods.get('product').get('name')
    process = currentMods.get('process').get('name')
    substrate = currentMods.get('substrate').get('name')
    material = currentMods.get('material').get('name')
    side1, sub1, proc1, prod1 = '', '', '', ''
    side2, sub2, proc2, prod2 = '', '', '', ''
    try:
        side1 = currentMods.get('side1').get('name')
        sub1 = currentMods.get('sub1').get('name')
        proc1 = currentMods.get('proc1').get('name')
        prod1 = currentMods.get('prod1').get('name')
    # boost1 = currentMods.get('boost1').get('name')
        side2 = currentMods.get('side2').get('name')
        sub2 = currentMods.get('sub2').get('name')
        proc2 = currentMods.get('proc2').get('name')
        prod2 = currentMods.get('prod2').get('name')
    # boost2 = currentMods.get('boost2').get('name')
    except:
        pass

    mainFlow = material + ar + substrate + ar + process + ar + product
    sideFlow1 = side1 + ar + sub1 + ar + proc1 + ar + prod1
    sideFlow2 = side2 + ar + sub2 + ar + proc2 + ar + prod2
    return [[mainFlow, sideFlow1, sideFlow2], currentMods]
