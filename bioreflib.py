"""
This library aids the development of an integrated bioprocess for a specified
product. It is used primarily by biorefine.py to allow the user to create a
bioprocess and then manipulate the steps within that process.
"""

import sys
import json


def user_build(product, dicts, optimization=None, filter=None):
    # initialize the bioprocess Modules for a specified product

    currentMods = {}  # dictionary of current Module values
    PRODUCTS = dicts['PRODUCTS']  # dictionary of all known products
    PROCESSES = dicts['PROCESSES']  # dictionary of all known processes
    SUBSTRATES = dicts['SUBSTRATES']  # dictionary of all known substrates
    MATERIALS = dicts['MATERIALS']  # dictionary of all known materials
    SIDES = dicts['SIDES']  # dictionary of all known side materials

    ts = ' -> '  # transition string
    currentMods['product'] = PRODUCTS.get(product)  # update product
    if optimization is None and filter is None:
        # no opt or filt specified, choose first available module value
        process = PRODUCTS.get(product)['processes'][0]
        for key, val in PROCESSES.get(process)['subprods'].items():
            sub, prod = key.split('2')
            if prod == product:
                substrate = sub
                break
        material = SUBSTRATES.get(substrate)['materials'][0]

        #  write output string and update Module values
        mainFlow = material + ts + substrate + ts + process + ts + product
        currentMods['process'] = PROCESSES.get(process)
        currentMods['substrate'] = SUBSTRATES.get(substrate)
        currentMods['material'] = MATERIALS.get(material)

        # initialize and update sideFlow Module values, output strings
        currentMods = replace_sideFlow('side1', currentMods)
        currentMods = replace_sideFlow('side2', currentMods)

        side1 = MATERIALS.get(material)['sides'][0]
        side2 = MATERIALS.get(material)['sides'][1]
        sideFlow1, sideFlow2 = '', ''

        if side1 != 'NA':
            sub1 = SIDES.get(side1)['substrates'][0]
            proc1 = SUBSTRATES.get(sub1)['processes'][0]
            for key, val in PROCESSES.get(proc1)['subprods'].items():
                sub, prod = key.split('2')
                if sub == sub1:
                    prod1 = prod
                    break

            sideFlow1 = side1 + ts + sub1 + ts + proc1 + ts + prod1
            currentMods['side1'] = SIDES.get(side1)
            currentMods['sub1'] = SUBSTRATES.get(sub1)
            currentMods['proc1'] = PROCESSES.get(proc1)
            currentMods['prod1'] = PRODUCTS.get(prod1)

        if side2 != 'NA':
            sub2 = SIDES.get(side2)['substrates'][0]
            proc2 = SUBSTRATES.get(sub2)['processes'][0]
            for key, val in PROCESSES.get(proc2)['subprods'].items():
                sub, prod = key.split('2')
                if sub == sub2:
                    prod2 = prod
                    break

            sideFlow2 = side2 + ts + sub2 + ts + proc2 + ts + prod2
            currentMods['side2'] = SIDES.get(side2)
            currentMods['sub2'] = SUBSTRATES.get(sub2)
            currentMods['proc2'] = PROCESSES.get(proc2)
            currentMods['prod2'] = PRODUCTS.get(prod2)

    else:
        # filter available Module values and optimize decision making
        print('Optimization and Filtering options coming soon!')
        sys.exit(0)

    return [[mainFlow, sideFlow1, sideFlow2], currentMods]


def user_change(changingMod, currentMods, newVal, dicts):
    # extract main dicts:
    PRODUCTS = dicts['PRODUCTS']
    PROCESSES = dicts['PROCESSES']
    SUBSTRATES = dicts['SUBSTRATES']
    MATERIALS = dicts['MATERIALS']
    SIDES = dicts['SIDES']

    # extract current state of network
    # these could eventually be made as objects in a Module class
    product = currentMods['product']
    process = currentMods['process']
    substrate = currentMods['substrate']
    material = currentMods['material']
    # testing for presence of sideFlows
    if currentMods.get('side1') is not None:
        side1 = currentMods['side1']
        sub1 = currentMods['sub1']
        proc1 = currentMods['proc1']
        prod1 = currentMods['prod1']
        boost1 = currentMods['boost1']
    else:
        side1 = {'name': 'NA'}
        sub1 = {'name': 'NA'}
        proc1 = {'name': 'NA'}
        prod1 = {'name': 'NA'}
        boost1 = {'name': 'NA'}

    if currentMods.get('side2') is not None:
        side2 = currentMods['side2']
        sub2 = currentMods['sub2']
        proc2 = currentMods['proc2']
        prod2 = currentMods['prod2']
        boost2 = currentMods['boost2']
    else:
        side2 = {'name': 'NA'}
        sub2 = {'name': 'NA'}
        proc2 = {'name': 'NA'}
        prod2 = {'name': 'NA'}
        boost2 = {'name': 'NA'}

    # begin process of updating Module values based on initial input
    if changingMod == 'product':
        # change process to new newVal
        product = PRODUCTS.get(newVal)
        currentMods['product'] = product
        # if new substrate fits with current material, we're done!
        key = '2'.join([substrate['name'], product['name']])
        process = PROCESSES.get(process['name'])
        subprod = process['subprods'].get(key)
        # if new product fits with current process & substrate, we're done!
        if subprod is None:
            for key, val in process['subprods'].items():
                sub, prod = key.split('2')
                if prod == product['name']:
                    changingMod = 'substrate'
                    newVal = sub

            if changingMod == 'product':
                changingMod = 'process'
                newVal = product['processes'][0]

    if changingMod == 'process':
        # change process to new newVal
        process = PROCESSES.get(newVal)
        currentMods['process'] = process
        # if new process fits with current substrate, we're done!
        key = '2'.join([substrate['name'], product['name']])
        subprod = process['subprods'].get(key)
        if subprod is None:
            for key, val in process['subprods'].items():
                sub, prod = key.split('2')
                if prod == product['name']:
                    changingMod = 'substrate'
                    newVal = sub

    if changingMod == 'substrate':
        # change substrate to new newVal
        substrate = SUBSTRATES.get(newVal)
        currentMods['substrate'] = substrate
        # if new substrate fits with current material, we're done!
        if material['name'] not in substrate['materials']:
            changingMod = 'material'
            newVal = substrate['materials'][0]

    if changingMod == 'material':
        # change material to new newVal
        material = MATERIALS.get(newVal)
        currentMods['material'] = material
        # if new material fits with current side1, we're done!
        if side1['name'] not in material['sides']:
            sides = material['sides']
            substrate = currentMods['substrate']['name']
            for side in sides:
                if side not in ['NA', substrate]:
                    changingMod = 'side1'
                    newVal = side
            if changingMod != 'side1':
                currentMods = replace_sideFlow('side1', currentMods)

    if changingMod == 'side1':
        # change side1 to new newVal
        side1 = SIDES.get(newVal)
        currentMods['side1'] = side1
        # if new side1 fits with current sub1, we're done!
        if sub1['name'] not in side1['substrates']:
            changingMod = 'sub1'
            newVal = side1['substrates'][0]

    if changingMod == 'sub1':
        # change sub1 to new newVal
        sub1 = SUBSTRATES.get(newVal)
        currentMods['sub1'] = sub1
        # if new sub1 fits with current proc1 and prod1, we're done!
        if proc1['name'] != 'NA':
            key = '2'.join([sub1['name'], prod1['name']])
            proc1 = PROCESSES.get(proc1['name'])
            subprod = proc1['subprods'].get(key)
            if subprod is None:
                for key, val in proc1['subprods'].items():
                    sub, prod = key.split('2')
                    prod1 = currentMods['prod1']
                    if sub == sub1['name']:
                        changingMod = 'prod1'
                        newVal = prod

                if changingMod == 'sub1':
                    changingMod = 'proc1'
                    newVal = sub1['processes'][0]
        else:
            changingMod = 'proc1'
            newVal = sub1['processes'][0]

    if changingMod == 'proc1':
        # change proc1 to new newVal
        proc1 = PROCESSES.get(newVal)
        currentMods['proc1'] = proc1
        # if new proc1 fits with current product, we're done!
        key = '2'.join([sub1['name'], prod1['name']])
        subprod = proc1['subprods'].get(key)
        if subprod is None:
            for key, val in proc1['subprods'].items():
                sub, prod = key.split('2')
                if sub == sub1['name']:
                    changingMod = 'prod1'
                    newVal = prod

    if changingMod == 'prod1':
        #
        prod1 = PRODUCTS.get(newVal)
        currentMods['prod1'] = prod1
        materialDict = MATERIALS.get(currentMods['material']['name'])
        #
        if side2:
            if side2['name'] not in materialDict['sides']:
                sides = materialDict['sides']
                substrate = currentMods['substrate']['name']
                for side in sides:
                    if side not in ['NA', substrate, side1['name']]:
                        changingMod = 'side2'
                        newVal = side

                if changingMod != 'side2':
                    currentMods = replace_sideFlow('side2', currentMods)

    if changingMod == 'side2':
        # # change side1 to new newVal
        side2 = SIDES.get(newVal)
        currentMods['side2'] = side2
        # if new substrate fits with current side1, we're done!
        if sub2:
            if sub2['name'] not in side2['substrates']:
                changingMod = 'sub2'
                newVal = side2['substrates'][0]
        else:
            changingMod = 'sub2'
            newVal = side2['substrates'][0]

    if changingMod == 'sub2':
        # change sub2 to new newVal
        sub2 = SUBSTRATES.get(newVal)
        currentMods['sub2'] = sub2
        # if new sub2 fits with current proc2 and prod2, we're done!
        if proc2['name'] != 'NA':
            key = '2'.join([sub2['name'], prod2['name']])
            proc2 = PROCESSES.get(proc2['name'])
            subprod = proc2['subprods'].get(key)
            if subprod is None:
                for key, val in proc2['subprods'].items():
                    sub, prod = key.split('2')
                    if sub == sub2['name']:
                        changingMod = 'prod2'
                        newVal = prod

                if changingMod == 'sub2':
                    changingMod = 'proc2'
                    newVal = sub2['processes'][0]
        else:
            changingMod = 'proc2'
            newVal = sub2['processes'][0]

    if changingMod == 'proc2':
        # change proc2 to new newVal
        proc2 = PROCESSES.get(newVal)
        currentMods['proc2'] = proc2
        # if new proc2 fits with current product, we're done!
        key = '2'.join([sub2['name'], prod2['name']])
        subprod = proc2['subprods'].get(key)
        if subprod is None:
            for key, val in proc2['subprods'].items():
                sub, prod = key.split('2')
                if sub == sub2['name']:
                    changingMod = 'prod2'
                    newVal = prod

    if changingMod == 'prod2':
        # change proc2 to new newVal
        prod2 = PRODUCTS.get(newVal)
        currentMods['prod2'] = prod2
        # end of updates, add  "boost" Modules to
        # increase amount of side material,
        # i.e switchgrass, algae, food waste, etc.

    # reassemble bioprocess

    ts = ' -> '  # transition string
    product = currentMods['product']['name']
    process = currentMods['process']['name']
    substrate = currentMods['substrate']['name']
    material = currentMods['material']['name']

    sideFlow1, sideFlow2 = '', ''
    if currentMods['side1'] is not None:
        side1 = currentMods['side1']['name']
        sub1 = currentMods['sub1']['name']
        proc1 = currentMods['proc1']['name']
        prod1 = currentMods['prod1']['name']
        # boost1 = currentMods.get('boost1').get('name')
        sideFlow1 = side1 + ts + sub1 + ts + proc1 + ts + prod1
    if currentMods['side2'] is not None:
        side2 = currentMods['side2']['name']
        sub2 = currentMods['sub2']['name']
        proc2 = currentMods['proc2']['name']
        prod2 = currentMods['prod2']['name']
        # boost2 = currentMods.get('boost2').get('name')
        sideFlow2 = side2 + ts + sub2 + ts + proc2 + ts + prod2

    mainFlow = material + ts + substrate + ts + process + ts + product

    return [[mainFlow, sideFlow1, sideFlow2], currentMods]


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
            avails = list(dicts['PRODUCTS'].keys())
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


###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################

"""This is a one-time use library for us to develop dictionaries and write
json files"""

# develop master csv of all strains and their subprods, then use
# grep and command line filtering, my_utils.py, to get lists
# of relevant values for each dict.


def write_json():
    dicts = build_dicts()
    PRODUCTS = dicts['PRODUCTS']
    PROCESSES = dicts['PROCESSES']
    SUBSTRATES = dicts['SUBSTRATES']
    MATERIALS = dicts['MATERIALS']
    SIDES = dicts['SIDES']
    with open('Jproducts.json', 'w') as f:
        json.dump(PRODUCTS, f)
    with open('Jprocesses.json', 'w') as f:
        json.dump(PROCESSES, f)
    with open('Jsubstrates.json', 'w') as f:
        json.dump(SUBSTRATES, f)
    with open('Jmaterials.json', 'w') as f:
        json.dump(MATERIALS, f)
    with open('Jsides.json', 'w') as f:
        json.dump(SIDES, f)

    return None


def call_json():
    dicts = {}
    with open('Jproducts.json') as j:
        PRODUCTS = json.load(j)
    with open('Jprocesses.json') as j:
        PROCESSES = json.load(j)
    with open('Jsubstrates.json') as j:
        SUBSTRATES = json.load(j)
    with open('Jmaterials.json') as j:
        MATERIALS = json.load(j)
    with open('Jsides.json') as j:
        SIDES = json.load(j)

    tags = ['PRODUCTS', 'PROCESSES', 'SUBSTRATES', 'MATERIALS', 'SIDES']
    for tag in tags:
        dicts[tag] = eval(tag)

    return dicts


def build_dicts():
    dicts = {}
    PRODUCTS = build_products()
    PROCESSES = build_processes()
    SUBSTRATES = build_substrates()
    MATERIALS = build_materials()
    SIDES = build_sides()
    tags = ['PRODUCTS', 'PROCESSES', 'SUBSTRATES', 'MATERIALS', 'SIDES']
    for tag in tags:
        dicts[tag] = eval(tag)

    return dicts


def build_products():
    products = {}
    prodList = get_column('data_sub2prod.csv', result_column=3)
    prodList = list(set(prodList))
    for prod in prodList:
        processes = []
        results = get_column('data_sub2prod.csv', result_column=0,
                             query_column=3, query_value=prod)
        for r in list(set(results)):
            processes.append(r)

        products[prod] = {'name': prod,
                          'processes': processes
                          }
    return products


def build_processes():
    processes = {}
    processList = get_column('data_sub2prod.csv', result_column=0)
    processList = list(set(processList))

    for proc in processList:
        results = get_column('data_sub2prod.csv',
                             result_column=[2, 3],
                             query_column=0,
                             query_value=proc)

        subprods = build_subprods(results)
        substrates = []
        products = []
        for r in results:
            substrates.append(r[0])
            products.append(r[1])

        processes[proc] = {'name': proc,
                           'substrates': substrates,
                           'products': products,
                           'subprods': subprods
                           }
    return processes


def build_subprods(results):
    subprods = {}
    pairs = []
    for r in results:
        pairs.append('2'.join([r[0], r[1]]))

    for pair in list(set(pairs)):
        substrate, product = pair.split('2')

        strains = get_column('data_sub2prod.csv', result_column=[1, 4, 5, 6],
                             query_column=[2, 3], query_value=pair.split('2'))
        subprods[pair] = {'substrate': substrate,
                          'product': product,
                          'strains': strains}
    return subprods


def build_substrates():
    substrates = {}
    subList = get_column('data_sub2prod.csv', result_column=2)
    subList = list(set(subList))
    for sub in subList:
        processes = []
        results = get_column('data_sub2prod.csv', result_column=0,
                             query_column=2, query_value=sub)
        for r in list(set(results)):
            processes.append(r)

        materials = []
        results = get_column('data_mat2sub.csv', result_column=0,
                             query_column=[1, 2, 3],
                             query_value=[sub, sub, sub],
                             searchOr=True)
        for r in list(set(results)):
            materials.append(r)

        substrates[sub] = {'name': sub,
                           'processes': processes,
                           'materials': materials
                           }
    return substrates


def build_materials():
    materials = {}
    with open('data_mat2sub.csv', 'r') as f:
        header = f.readline()
        for line in f:
            a = line.rstrip().split(',')
            material = a[0]
            substrate = a[1]
            sides = ['NA']
            comp = ['NA']
            if a[2] != 'NA':
                side1 = a[2]
                side2 = a[3]
                sides = [side1, side2]
                c1, c2, c3 = a[4].split('/')
                comp = [float(c1), float(c2), float(c3)]
                comp_source = a[5]
            cropYield, cropSource = a[6], a[7]

            materials[material] = {'name': material,
                                   'substrate': substrate,
                                   'sides': sides,
                                   'comp': [comp, comp_source],
                                   'yield': [cropYield, cropSource]
                                   }
    return materials


def build_sides():
    sides = {}
    sidesList = get_column('data_side2sub.csv', result_column=0)
    sidesList = list(set(sidesList))

    for side in sidesList:
        results = get_column('data_side2sub.csv', result_column=[1, 2, 3, 4],
                             query_column=0, query_value=side)
        substrates = []
        treatments = []
        for r in results:
            substrates.append(r[0])
            treatments.append(r[1:4])
        substrates = list(set(substrates))

        sides[side] = {'name': side,
                       'substrates': substrates,
                       'treatments': treatments}
    return sides


def get_column(file_name,
               query_column=None,
               query_value=None,
               searchOr=False,
               result_column=1,
               date_column=None,
               header=True):
    """Return a list of filtered values from a specific column.

    Parameters:
    -----------
    file_name: string, name of csv file containing data of interest.
    query_column: int, column location contatining query of interest.
    query_value: string, query of interest.
    result_column: int, column location of desired results.
    data_column: int, column location of dates.

    Returns:
    --------
    results: a list of data-val paired items.
    """
    # convert list to int if only single column requested
    if type(result_column) == list and len(result_column) <= 1:
        result_column = result_column[0]

    try:
        with open(file_name, 'r', encoding="ISO-8859-1") as f:
            # assumes header on data
            if header:
                header = f.readline()
            results = []
            yesterday = []

            for line in f:
                a = line.rstrip().split(',')

                # no query, get entire column
                if query_value is None:
                    results = append_results(a,
                                             results,
                                             result_column)

                # multiple query, check all true before appending
                elif type(query_value) == list:
                    if len(query_value) != len(query_column):
                        print('Please enter a column for each query.')
                        sys.exit(3)

                    if searchOr:  # do an OR search in query columns
                        matches = False
                        for i, query in enumerate(query_value):
                            if a[query_column[i]] == query:
                                matches = True
                                break
                    else:
                        matches = True  # do an AND search in query columns
                        for i, query in enumerate(query_value):
                            # print(query, a[query_column[i]])
                            if a[query_column[i]] != query:
                                matches = False
                                break

                    if matches:
                        if date_column is not None:
                            results = track_dates(a,
                                                  date_column,
                                                  results,
                                                  result_column)

                        results = append_results(a,
                                                 results,
                                                 result_column)

                # single query, check query_column
                elif a[query_column] == query_value:
                    if date_column is not None:
                        results = track_dates(a,
                                              date_column,
                                              results,
                                              result_column)

                    results = append_results(a,
                                             results,
                                             result_column)

    # handle file error exception
    except FileNotFoundError:
        print('\nCould not read ' + file_name)
        sys.exit(2)

    return results


def track_dates(a, date_column, results):

    # check that dates are in a readable format
    try:
        year, month, day = a[date_column].split('-')
        year, month, day = int(year), int(month), int(day)
        today = dt.date(year, month, day)

    except(ValueError):
        print('\nDates in column {} not 8 digit \
                YYYY-MM-DD format'.format(date_column))
        sys.exit(1)

    # logic for counting days and filling gaps.
    # initialize "yesterday" for day 1
    if not yesterday:
        yesterday = today - dt.timedelta(days=1)

    delta = today - yesterday
    # move forward one day
    yesterday = today

    # append single zero or multiple zeros if multi columns
    if delta.days > 1:
        for day in range(delta.days - 1):
            if type(result_column) == int:
                results.append(0)
            elif type(result_column) == list:
                vals = []
                for col in result_column:
                    vals.append(0)
                results.append(vals)

    try:
        if delta.days < 0:
            raise ValueError

    except(ValueError):
        print('\nDates are not in order')
        sys.exit(3)

        return results


def append_results(a, results, result_column):
    if type(result_column) == int:
        value = a[result_column]
        # convert to ints if possible
        try:
            value = int(value)
        except(ValueError):
            pass
        results.append(value)
    elif type(result_column) == list:
        vals = []
        for col in result_column:
            value = a[col]
            # convert to ints if possible
            try:
                value = int(value)
            except(ValueError):
                pass
            vals.append(value)
        results.append(vals)
    else:
        print('Please enter integers for columns')
        sys.exit(1)

    return results


if __name__ == '__main__':
    main()
