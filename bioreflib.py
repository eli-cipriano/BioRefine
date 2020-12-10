"""
This library aids the development of an integrated bioprocess for a specified
product. It is used primarily by biorefine.py to allow the user to create a
bioprocess and then manipulate the steps within that process. The bioprocess is
made up of 12 Modular Units:

    [product, process, substrate, material,
    side1, sub1, proc1, prod1,
    side2, sub2, proc2, prod2]

Two additional mods boost1, and boost2 may be added in later. The bioprocess is
built and updated in the same directional flow. It starts at the "top", which
is the "product" Unit, and goes through process and substrate, ending on the
"material" Unit. After these four steps, if a side material exists, the flow
will go to the "side1" Modular Unit and populate the subsequent Modular Units.
If a second side material exists, the flow jumps to the "side2" Modular Unit
and populates those subsequent Modular Units.

The main database is made up of three CSV files that describe the properties of
various raw materials (mat2sub), waste by-products (side2sub), and
chemical processes (sub2prod).

The two main functions for the bioprocessing side of the code are:
- user_build: is used to initialize a bioprocess based on a given product.

- user_change: is used to update the values of the bioprocess every time there
is a change. The user is only allowed to pick a new value from a list of valid
options. For example, if the user wants to change the current material, they
will only be allowed to pick from a list of materials that are associated with
the Modular Unit immediately infront of it, which is "substrate". Similarly, to
change "sub1", it must be compatible with "side1", according to the directional
flow of the program.

The main functions for the database side of the code are:
- build_
"""

import sys
import json


def get_mod_units():
    mod_units = ['product', 'process', 'substrate', 'material',
                 'side1', 'sub1', 'proc1', 'prod1', 'boost1',
                 'side2', 'sub2', 'proc2', 'prod2', 'boost2']
    return mod_units


def user_change(changingMod, newVal, currentMods):
    """
    This function takes a specific Modular Unit to change (see top for Modular
    Units). This function becomes much more clear after the use of biorefine.py
    or GUI_biorefine.py.

    The logical flow follows the directional flow described in the
    documentation for this library. It starts by first checking the product
    Unit. If the user has chosen the product as the Modular Unit they want
    to change, that code block will activate and change the product to the
    new value. Then, the program checks the compatibility of the next Unit,
    "process", with the new "product" value.

    If the next Modular Unit is compatible, then the code stops checking other
    Modular Units and updates all the values that were changed.

    If the next Modular Unit is not compatible, a new value for that Modular
    Unit is selected and the program moves to the next code block. This process
    repeats along the directional flow of the program until it reaches a
    compatible Unit.

    Compatability is even more complicated in this function because we have to
    check that the new values are compatible with the Bioprocess that existed
    before the changes. For instance, if the user specifies a new material, the
    side1 and side2 Modular Units need to both be updated since they depend on
    the value of the material. If side1 then updates to a new value, this could
    affect all or none of the following Modular Units, depending on the value
    of side1.

    Parameters
    -----------
    changingMod: str, modular unit you want to change
    newVal: str, modular unit you want to change changingMod to
    currentMods: str, the position of the modular unit to change

    Returns
    --------
    The bioprocess map is updated with newVal in the currentMods position

    """
    # extract main dicts:
    dicts = call_json()
    PRODUCTS = dicts['PRODUCTS']
    PROCESSES = dicts['PROCESSES']
    SUBSTRATES = dicts['SUBSTRATES']
    MATERIALS = dicts['MATERIALS']
    SIDES = dicts['SIDES']

    # make Modular Unit dictionaries to determine current state
    # of the Bioprocess
    product = currentMods['product']
    process = currentMods['process']
    substrate = currentMods['substrate']
    material = currentMods['material']
    side1 = currentMods['side1']
    sub1 = currentMods['sub1']
    proc1 = currentMods['proc1']
    prod1 = currentMods['prod1']
    boost1 = currentMods['boost1']
    side2 = currentMods['side2']
    sub2 = currentMods['sub2']
    proc2 = currentMods['proc2']
    prod2 = currentMods['prod2']
    boost2 = currentMods['boost2']

    # begin updating Modular Unit values based on user input

    if changingMod == 'product':
        # change process to new newVal
        product = PRODUCTS.get(newVal)
        currentMods['product'] = product
        # if new substrate fits with current material, we're done!
        # Otherwise, changingMod will be 'process'
        changingMod, newVal = check_process(currentMods,
                                            changingMod,
                                            newVal,
                                            PROCESSES
                                            )

    if changingMod == 'process':
        # change process to new newVal
        process = PROCESSES.get(newVal)
        currentMods['process'] = process
        # if new process fits with current substrate, we're done!
        # Otherwise, changingMod will be 'substrate'
        changingMod, newVal = check_substrate(currentMods,
                                              changingMod,
                                              newVal
                                              )

    if changingMod == 'substrate':
        # change substrate to new newVal
        substrate = SUBSTRATES.get(newVal)
        currentMods['substrate'] = substrate
        # if new substrate fits with current material, we're done!
        # Otherwise, changingMod will be 'material'
        changingMod, newVal = check_material(currentMods,
                                             changingMod,
                                             newVal
                                             )

    if changingMod == 'material':
        # change material to new newVal
        material = MATERIALS.get(newVal)
        currentMods['material'] = material
        # if new material fits with current side1 and side2, we're done!
        # Otherwise, changingMod will be 'side1/2'
        changingMod, newVal = check_sides(currentMods,
                                          changingMod,
                                          newVal,
                                          floNum=1
                                          )

    if changingMod == 'side1':
        if newVal == 'none':
            currentMods = replace_sideFlow('side1', currentMods)
        else:
            # change side1 to new newVal
            side1 = SIDES.get(newVal)
            currentMods['side1'] = side1
            # if new side1 fits with current sub1, we're done!
            # Otherwise, changingMod will be 'sub1'
            changingMod, newVal = check_subs(currentMods,
                                             changingMod,
                                             newVal,
                                             floNum=1
                                             )

    if changingMod == 'sub1':
        # change sub1 to new newVal
        sub1 = SUBSTRATES.get(newVal)
        currentMods['sub1'] = sub1
        # if new sub1 fits with current proc1 and prod1, we're done!
        # Otherwise, changingMod will be 'proc1'
        changingMod, newVal = check_procs(currentMods,
                                          changingMod,
                                          newVal,
                                          PROCESSES,
                                          floNum=1
                                          )

    if changingMod == 'proc1':
        # change proc1 to new newVal
        proc1 = PROCESSES.get(newVal)
        currentMods['proc1'] = proc1
        # if new proc1 fits with current product, we're done!
        # Otherwise, changingMod will be 'prod1'
        changingMod, newVal = check_prods(currentMods,
                                          changingMod,
                                          newVal,
                                          floNum=1
                                          )

    if changingMod == 'prod1':
        # change prod1 to new newVal
        if newVal:
            prod1 = PRODUCTS.get(newVal)
            currentMods['prod1'] = prod1
        # if new material fits with current side2, we're done!
        # Otherwise, changingMod will be 'side2'
        changingMod, newVal = check_sides(currentMods,
                                          changingMod,
                                          newVal,
                                          floNum=2
                                          )

    if changingMod == 'side2':
        if newVal == 'none':
            currentMods = replace_sideFlow('side2', currentMods)
        else:
            # # change side2 to new newVal
            side2 = SIDES.get(newVal)
            currentMods['side2'] = side2
            # if new side1 fits with current sub1, we're done!
            changingMod, newVal = check_subs(currentMods,
                                             changingMod,
                                             newVal,
                                             floNum=2
                                             )

    if changingMod == 'sub2':
        # change sub2 to new newVal
        sub2 = SUBSTRATES.get(newVal)
        currentMods['sub2'] = sub2
        # if new sub2 fits with current proc2 and prod2, we're done!
        # Otherwise, changingMod will be 'proc2'
        changingMod, newVal = check_procs(currentMods,
                                          changingMod,
                                          newVal,
                                          PROCESSES,
                                          floNum=2
                                          )

    if changingMod == 'proc2':
        # change proc2 to new newVal
        proc2 = PROCESSES.get(newVal)
        currentMods['proc2'] = proc2
        # if new proc2 fits with current product, we're done!
        # Otherwise, changingMod will be 'prod2'
        changingMod, newVal = check_prods(currentMods,
                                          changingMod,
                                          newVal,
                                          floNum=2
                                          )

    if changingMod == 'prod2':
        # change proc2 to new newVal
        prod2 = PRODUCTS.get(newVal)
        currentMods['prod2'] = prod2
        # end of updates, move on to next part of function:
        # assembly of string-pattern

        """
        In the future, we will add "boost" Modular Units for increasing the
        amount of side material, i.e switchgrass, algae, food waste, etc.

        These can be used to link multiple bioprocesses together. For instance,
        if you had a process that used both corn and sugar cane, you could
        incorporate the use of switchgrass to generate enough cellulosic
        biomass between the 3 plant sources for a large-operation cellulose
        refinement process, which could allow for the co-production of more
        distantly-related products.
        """

    # assemble bioprocess into string-pattern
    flows = assemble_flows(currentMods)

    return flows, currentMods


######################## "CHECK" Helper Functions ##############################
"""
The following "check" functions are used in the user_change function to make
sure the Modular Unit values comprise a real, feasable bioprocess. This is done
by referencing the datasets describing the conversion of three types of Modular
Units: materials, sides, and substrates (stored in .biorefine/data and written
by brf functions).
"""


def check_process(currentMods,
                  changingMod,
                  newVal,
                  PROCESSES):

    # call specific Modular Untis from currentMods dictionary
    substrate = currentMods['substrate']
    product = currentMods['product']
    process = currentMods['process']
    # check if current process is compatible with current subprod combo
    key = '2'.join([substrate['name'], product['name']])
    # process = PROCESSES.get(process['name'])
    subprod = process['subprods'].get(key)
    # if new product fits with current process & substrate, we're done!
    if subprod is None:
        for key, val in process['subprods'].items():
            sub, prod = key.split('*2*')
            if prod == product['name']:
                changingMod = 'substrate'
                newVal = sub

        if changingMod == 'product':
            changingMod = 'process'
            newVal = product['processes'][0]

    return changingMod, newVal


def check_substrate(currentMods,
                    changingMod,
                    newVal
                    ):
    # call specific Modular Unit Values
    substrate = currentMods['substrate']
    process = currentMods['process']
    product = currentMods['product']

    # check compatability of substrate with current process
    key = '2'.join([substrate['name'], product['name']])
    subprod = process['subprods'].get(key)
    if subprod is None:
        for key, val in process['subprods'].items():
            sub, prod = key.split('*2*')
            if prod == product['name']:
                changingMod = 'substrate'
                newVal = sub

    return changingMod, newVal


def check_material(currentMods,
                   changingMod,
                   newVal
                   ):
    # call specific Modular Unit Values
    substrate = currentMods['substrate']
    material = currentMods['material']
    # check compatability of material with new substrate
    if material['name'] not in substrate['materials']:
        changingMod = 'material'
        newVal = substrate['materials'][0]

    return changingMod, newVal


def check_sides(currentMods,
                changingMod,
                newVal,
                floNum=1
                ):

    # call specfic Modular Unit Values
    side1 = currentMods['side1']
    side2 = currentMods['side2']
    material = currentMods['material']
    substrate = currentMods['substrate']

    # check compatability of side1 with new material
    if side1['name'] not in material['sides'] and floNum != 2:
        sides = material['sides']
        for side in sides:
            if side not in ['NA', substrate['name']]:
                changingMod = 'side1'
                newVal = side
        if changingMod != 'side1':
            currentMods = replace_sideFlow('side1', currentMods)
            newVal = ''
            changingMod = 'prod1'

    # check compatability of side2 with new material
    elif side2['name'] not in material['sides'] and floNum:
        sides = material['sides']
        for side in sides:
            if side not in ['NA', substrate['name'], side1['name']]:
                changingMod = 'side2'
                newVal = side
        if changingMod != 'side2':
            currentMods = replace_sideFlow('side2', currentMods)

    return changingMod, newVal


def check_subs(currentMods,
               changingMod,
               newVal,
               floNum=1
               ):

    # get keys for whichever sideFlow is being looked at
    subKey = 'sub{}'.format(floNum)
    sideKey = 'side{}'.format(floNum)
    # call specific Modular Unit Values
    sub = currentMods[subKey]
    side = currentMods[sideKey]

    if sub['name'] not in side['substrates']:
        changingMod = 'sub{}'.format(floNum)
        newVal = side['substrates'][0]

    return changingMod, newVal


def check_procs(currentMods,
                changingMod,
                newVal,
                PROCESSES,
                floNum=1
                ):

    # get keys for whichever sideFlow is being looked at
    procKey = 'proc{}'.format(floNum)
    subKey = 'sub{}'.format(floNum)
    prodKey = 'prod{}'.format(floNum)
    # call specific Modular Unit Values
    proc = currentMods[procKey]
    sub = currentMods[subKey]
    prod = currentMods[prodKey]

    if proc['name'] != '':
        key = '2'.join([sub['name'], prod['name']])
        # proc = PROCESSES.get(proc['name'])
        subprod = proc['subprods'].get(key)
        if subprod is None:
            for key, val in proc['subprods'].items():
                s, p = key.split('*2*')
                if s == sub['name']:
                    changingMod = prodKey
                    newVal = p

            if changingMod == subKey:
                changingMod = procKey
                newVal = sub['processes'][0]
    else:
        changingMod = procKey
        newVal = sub['processes'][0]

    return changingMod, newVal


def check_prods(currentMods,
                changingMod,
                newVal,
                floNum=1
                ):

    # get keys for whichever sideFlow is being looked at
    procKey = 'proc{}'.format(floNum)
    subKey = 'sub{}'.format(floNum)
    prodKey = 'prod{}'.format(floNum)
    # call specific Modular Unit Values
    proc = currentMods[procKey]
    sub = currentMods[subKey]
    prod = currentMods[prodKey]
    # compare compatability with current process
    key = '2'.join([sub['name'], prod['name']])
    subprod = proc['subprods'].get(key)
    if subprod is None:
        for key, val in proc['subprods'].items():
            s, p = key.split('*2*')
            if s == sub['name']:
                changingMod = prodKey
                newVal = p

    return changingMod, newVal

################################################################################


############################## Helper Functions ################################
"""
These functions are used for various procedures throughout the GUI program and
this library.
"""


def replace_sideFlow(side, currentMods):
    """
    Helper function for erasing current sideFlow Modular units

    Parameters
    -------------
    side = str, should be "side1" or "side2"

    currentMods = dictionary, Current Modular Units of bioprocess

    Returns
    -------------
    currentMods
    """
    # initialize or reset values for sideFlows
    if side == 'side1':
        currentMods['side1'] = {'name': ''}
        currentMods['sub1'] = {'name': ''}
        currentMods['proc1'] = {'name': ''}
        currentMods['prod1'] = {'name': ''}
        currentMods['boost1'] = {'name': ''}
    elif side == 'side2':
        currentMods['side2'] = {'name': ''}
        currentMods['sub2'] = {'name': ''}
        currentMods['proc2'] = {'name': ''}
        currentMods['prod2'] = {'name': ''}
        currentMods['boost2'] = {'name': ''}
    return currentMods


def assemble_flows(currentMods):
    """
    Helper function for building the process diagram, or "biomap" for output to
    the text file.

    Parameters
    -------------
    currentMods = dictionary, Current Modular Units of bioprocess

    Returns
    -------------
    [flows] = a list of the 3 flows shown in the "biomap"
    """
    ts = ' -> '  # transition string
    product = currentMods['product']['name']
    process = currentMods['process']['name']
    substrate = currentMods['substrate']['name']
    material = currentMods['material']['name']

    mainFlow = material + ts + substrate + ts + process + ts + product

    side1 = currentMods['side1']['name']
    sub1 = currentMods['sub1']['name']
    proc1 = currentMods['proc1']['name']
    prod1 = currentMods['prod1']['name']
    # boost1 = currentMods.get('boost1').get('name')
    side2 = currentMods['side2']['name']
    sub2 = currentMods['sub2']['name']
    proc2 = currentMods['proc2']['name']
    prod2 = currentMods['prod2']['name']
    # boost2 = currentMods.get('boost2').get('name')

    sideFlow1, sideFlow2 = '', ''
    if side1 != '':
        sideFlow1 = side1 + ts + sub1 + ts + proc1 + ts + prod1
    if side2 != '':
        sideFlow2 = side2 + ts + sub2 + ts + proc2 + ts + prod2

    return [mainFlow, sideFlow1, sideFlow2]


def print_bioprocess(mainFlow, sideFlow1, sideFlow2):
    """
    Helper function for printing the 3 flows to std out and to the "biomap" var

    Parameters
    -------------
    side = str, should be "side1" or "side2"

    currentMods = dictionary, Current Modular Units of bioprocess

    Returns
    -------------
    currentMods
    """
    biomap = \
        '-------------------------------------------------------' \
        '------------------------\n' \
        + sideFlow1 \
        + '\n  |  \n' \
        + mainFlow \
        + '\n  |  \n' \
        + sideFlow2 \
        + '\n-------------------------------------------------------' \
        '------------------------\n'
    print(biomap)
    return biomap


def write_bioprocess(currentMods, fileName, mod_units=None, biomap=None):
    """
    Helper function for saving the bioprocess, both to JSON and text file.
    These two file types are for loading presaved biomaps into the program
    (JSON) and for viewing a write-up of the bioprocess (text).

    The function uses other helper functions to determine where the files are
    to be saved as well as to ensure the proper file type is saved.

    Parameters
    -------------
    currentMods = dictionary, Current Modular Units of bioprocess

    fileName = str, path to file. Can include custom directory, uses processes/
                by default.

    mod_units = list of str, list of Modular Unit names

    biomap = str, output from print_bioprocess, which assembles the flow strings
                into the diagram referred to as the "biomap"

    Returns
    -------------
    None
    """
    # get appropriate fiel extensions
    fileName = default_path(fileName)
    jName, fileName = get_file_ext('.json', fileName)
    tName, fileName = get_file_ext('.txt', fileName)

    # saves current bioprocess to json and txt files
    # also used to create a startup file in the case that the start up is missing
    with open(jName, 'w') as f:
        json.dump(currentMods, f)

    # if both variables are passed in, then write the text file.
    if mod_units and biomap:
        with open(tName, 'w') as f:
            f.write(biomap + '\n')
            details = []
            for mod in mod_units:
                detailText = print_Details(mod, currentMods)
                f.write(mod.upper() + '\n')
                f.write(detailText + '\n')

    return None


def get_file_ext(ext, fileName):
    """
    Helper function for making sure the correct file ending is appended.

    Parameters
    -------------
    ext = str, file extension. ex) ".json" or ".txt"

    fileName = str, path to file. Can include custom directory, uses processes/
                by default.

    Returns
    -------------
    typeName, fileName = str, file paths including the extension (typeName) and
                         without (fileName).
    """
    if ext != fileName[-len(ext):].lower():
        typeName = ''.join([fileName, ext])
    else:
        fileName = fileName[0:-len(ext)]
        typeName = ''.join([fileName, ext])

    return typeName, fileName


def default_path(fileName):
    """
    Helper function for making sure the correct file path is added.

    Parameters
    -------------
    fileName = str, path to file. Can include custom directory, uses processes/
                by default.

    Returns
    -------------
    fileName = str, file path including specific file location
    """
    noPath = '/' not in fileName and '\\' not in fileName
    if noPath:
        fileName = ''.join(['processes/', fileName])
    return fileName


def get_avails(mod, mod_units, currentMods):
    """
    Helper function for determining which options the user can choose from.

    Parameters
    -------------
    mod = str, name of Modular Unit

    mod_units = list of str, names of Modular Units

    currentMods = dictionary, Current Modular Units of bioprocess

    Returns
    -------------
    avails = list of str, all available options for chosen Modular Unit "mod"
    """
    avails = []
    dicts = call_json()
    if mod in mod_units[0:4]:
        if mod == 'product':
            avails = list(dicts['PRODUCTS'].keys())
        elif mod == 'process':
            avails = currentMods['product']['processes']
        elif mod == 'substrate':
            subprods = currentMods['process']['subprods']
            product = currentMods['product']['name']
            for key, val in subprods.items():
                sub, prod = key.split('*2*')
                if prod == product:
                    avails.append(sub)
        elif mod == 'material':
            avails = currentMods['substrate']['materials']
        return avails

    elif mod in mod_units[4:14]:
        if mod in ['prod1', 'prod2']:
            if mod == 'prod1':
                subprods = currentMods['proc1']['subprods']
                substrate = currentMods['sub1']['name']
            elif mod == 'prod2':
                subprods = currentMods['proc2']['subprods']
                substrate = currentMods['sub2']['name']
            for key, val in subprods.items():
                sub, prod = key.split('*2*')
                if sub == substrate:
                    avails.append(prod)
        elif mod in ['proc1', 'proc2']:
            if mod == 'proc1':
                avails = currentMods['sub1']['processes']
            elif mod == 'proc2':
                avails = currentMods['sub2']['processes']
        elif mod in ['sub1', 'sub2']:
            if mod == 'sub1':
                avails = currentMods['side1']['substrates']
            elif mod == 'sub2':
                avails = currentMods['side2']['substrates']
        elif mod in ['side1', 'side2']:
            avails = currentMods['material']['sides']
        return avails


def print_Details(mod, currentMods):
    """
    Helper function for writing detailed text from each Modular Unit.

    Parameters
    -------------
    mod = str, name of Modular Unit

    currentMods = dictionary, Current Modular Units of bioprocess

    Returns
    -------------
    detailText = str, information from currentMods for the user's reference
    """
    detailText = ''
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
            key = '*2*'.join([sub, prod])
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


def create_default():
    """
    Function for recreating a startup bioprocess in case the current one is
    deleted.
    """
    flows, cm = user_build('ethanol')
    flows, cm = user_change('process', 'yeast_anaerobic', cm)
    flows, cm = user_change('proc1', 'ecoli_anaerobic', cm)
    flows, cm = user_change('sub2', 'oil', cm)
    flows, cm = user_change('prod2', 'biodiesel', cm)

    mod_units = get_mod_units()

    mainFlow, sideFlow1, sideFlow2 = flows[:]
    biomap = print_bioprocess(mainFlow, sideFlow1, sideFlow2)

    write_bioprocess(cm,
                     '.startup_DO-NOT-DELETE',
                     mod_units=mod_units,
                     biomap=biomap)

    return flows, cm

###############################################################################
###############################################################################
#####################^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^###########################
#################### Functions for Making/Editing BP ##########################
###############################################################################
###############################################################################
###############################################################################
##################### Functions for Data Management ###########################
#####################vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv###########################
###############################################################################
###############################################################################


"""
This is a library for us to develop dictionaries and write
json files. It's only used when we want to update the database that the first
part of bioreflib relies on.
"""


def write_json():
    """
    Writes all dictionaries for products, processes, etc. to JSON files so they
    can be called later on rather than be built from scratch each time.
    """
    dicts = build_dicts()
    PRODUCTS = dicts['PRODUCTS']
    PROCESSES = dicts['PROCESSES']
    SUBSTRATES = dicts['SUBSTRATES']
    MATERIALS = dicts['MATERIALS']
    SIDES = dicts['SIDES']
    with open('.biorefine_data/Jproducts.json', 'w') as f:
        json.dump(PRODUCTS, f)
    with open('.biorefine_data/Jprocesses.json', 'w') as f:
        json.dump(PROCESSES, f)
    with open('.biorefine_data/Jsubstrates.json', 'w') as f:
        json.dump(SUBSTRATES, f)
    with open('.biorefine_data/Jmaterials.json', 'w') as f:
        json.dump(MATERIALS, f)
    with open('.biorefine_data/Jsides.json', 'w') as f:
        json.dump(SIDES, f)

    return None


def call_json():
    """
    Loads json files and organizes them into a dict of dicts
    """
    dicts = {}
    with open('.biorefine_data/Jproducts.json') as j:
        PRODUCTS = json.load(j)
    with open('.biorefine_data/Jprocesses.json') as j:
        PROCESSES = json.load(j)
    with open('.biorefine_data/Jsubstrates.json') as j:
        SUBSTRATES = json.load(j)
    with open('.biorefine_data/Jmaterials.json') as j:
        MATERIALS = json.load(j)
    with open('.biorefine_data/Jsides.json') as j:
        SIDES = json.load(j)

    tags = ['PRODUCTS', 'PROCESSES', 'SUBSTRATES', 'MATERIALS', 'SIDES']
    for tag in tags:
        dicts[tag] = eval(tag)

    return dicts


def build_dicts():
    """
    Calls build functions to create dictionaries from CSV's. The plan for these
    build functions is to eventually change them to a sorted list rather than
    dictionaries, but this will only reduce the size of the databases and won't
    change the functionality of the program.
    """
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
    """
    Library of possible bio-products
    """
    products = {}
    # make a list of unique products
    prodList = get_column('.biorefine_data/data_sub2prod.csv', result_column=3)
    prodList = sorted(list(set(prodList)))

    # extract information for each product
    for prod in prodList:
        processes = []
        results = get_column('.biorefine_data/data_sub2prod.csv', result_column=0,
                             query_column=3, query_value=prod)
        for r in sorted(list(set(results))):
            processes.append(r)

        products[prod] = {'name': prod,
                          'processes': processes
                          }
    return products


def build_processes():
    """
    Library of possible biochemical processes
    """
    processes = {}
    # make a list of unique processes
    processList = get_column('.biorefine_data/data_sub2prod.csv', result_column=0)
    processList = sorted(list(set(processList)))

    # extract information for each process
    for proc in processList:
        results = get_column('.biorefine_data/data_sub2prod.csv',
                             result_column=[2, 3],
                             query_column=0,
                             query_value=proc)

        # make inner dictionary for specific substrate conversions
        subprods = build_subprods(results)
        substrates = []
        products = []
        for r in results:
            substrates.append(r[0])
            products.append(r[1])

        processes[proc] = {'name': proc,
                           'substrates': sorted(list(set(substrates))),
                           'products': sorted(list(set(products))),
                           'subprods': subprods
                           }
    return processes


def build_subprods(results):
    """
    Library of possible substrate conversions
    """
    subprods = {}
    # make a list of unique conversions
    pairs = []
    for r in results:
        pairs.append('*2*'.join([r[0], r[1]]))

    # get information for each conversion
    for pair in sorted(list(set(pairs))):
        substrate, product = pair.split('*2*')

        # pass in 2 queries so that both values have to be true
        strains = get_column('.biorefine_data/data_sub2prod.csv', result_column=[1, 4, 5, 6],
                             query_column=[2, 3], query_value=pair.split('*2*'))
        subprods[pair] = {'substrate': substrate,
                          'product': product,
                          'strains': strains}
    return subprods


def build_substrates():
    """
    Library of possible substrates
    """
    substrates = {}
    # make a list of unique substrates
    subList = get_column('.biorefine_data/data_sub2prod.csv', result_column=2)
    subList = sorted(list(set(subList)))
    for sub in subList:
        # get a list of unique processes
        results = get_column('.biorefine_data/data_sub2prod.csv', result_column=0,
                             query_column=2, query_value=sub)
        processes = []
        for r in sorted(list(set(results))):
            processes.append(r)

        # pass in 3 queries so that only one value has to be true
        # checking material, side1, side2 columns to
        # make a list of unique materials.
        results = get_column('.biorefine_data/data_mat2sub.csv', result_column=0,
                             query_column=[1, 2, 3],
                             query_value=[sub, sub, sub],
                             searchOr=True)
        materials = []
        for r in sorted(list(set(results))):
            materials.append(r)

        substrates[sub] = {'name': sub,
                           'processes': processes,
                           'materials': materials
                           }
    return substrates


def build_materials():
    """
    Library of possible materials:
    This is our first attempt before we started using get_column. Just realized
    I never went back and updated it, but this works for now.
    """
    materials = {}
    with open('.biorefine_data/data_mat2sub.csv', 'r') as f:
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
    # make list of unique side materials
    sidesList = get_column('.biorefine_data/data_side2sub.csv', result_column=0)
    sidesList = sorted(list(set(sidesList)))

    # extract information for each side material
    for side in sidesList:
        results = get_column('.biorefine_data/data_side2sub.csv', result_column=[1, 2, 3, 4],
                             query_column=0, query_value=side)
        substrates = []
        treatments = []
        for r in results:
            substrates.append(r[0])
            treatments.append(r[1:4])
        substrates = sorted(list(set(substrates)))

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

    * We may consider adding the my_utils.py library if linear/binary searching
    becomes necessary, but for now we just copied the get_columns code in. We
    could also link the code as a git subUnit.
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


def track_dates(a, date_column, results, result_column):
    """
    Used exclusively by get_column

    Parameters
    -----------
    a: parameter from get_column
    date_column: parameter from get_column
    results: why is results an input and also what is returned?
    result_column: parameter from get_column

    Returns
    --------
    formats date output in a readable format for get_column

    """
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
    """
    Used exclusively by get_column

    Parameters
    -----------
    a: parameter from get_column
    results:
    result_column: parameter from from get_column

    Returns
    --------
    append results to output in get_column

    """
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


def user_build(product, optimization=None, filter=None):
    """
    This function builds the "Bioprocess", which is the network of Modular
    Units and their values. The user only specifies the product, and then the
    rest of the values are ensured to be "compatible" and then chosen
    alphabetically. Eventually we want to implement some sort of optimization
    where it always chooses the "best" value.

    Compatibility of neighboring Modular Units is more complex for some Modular
    Units than others. For materials, it's jsut a matter of checking that a
    material exists within the "materials" key of the chosen substrate. For
    compatability of substrates, processes, and products, we have to check that
    within that process, it is actually possible to convert the chosen
    substrate to the specified product, which is described by the "sub2prod"
    key in the process Unit.

    Parameters
    -----------
    product: str, the name of the product you want to build towards
    optimization: str, which factor you want to optimize for in selecting
        a bioprocess (IN PROGRESS)
    filter: str, what you want to filter through in selecting a bioprocess
        (IN PROGRESS)

    Returns
    --------
    a bioprocess map towards that process, which can then be modified.

    """
    # initialize the bioprocess Modular Units for a specified product

    currentMods = {}  # dictionary of current Modular Unit values
    dicts = call_json()  # acquire libraries
    PRODUCTS = dicts['PRODUCTS']  # dictionary of all known products
    PROCESSES = dicts['PROCESSES']  # dictionary of all known processes
    SUBSTRATES = dicts['SUBSTRATES']  # dictionary of all known substrates
    MATERIALS = dicts['MATERIALS']  # dictionary of all known materials
    SIDES = dicts['SIDES']  # dictionary of all known side materials

    currentMods['product'] = PRODUCTS.get(product)  # update product
    if optimization is None and filter is None:
        # no opt or filt specified, choose first available Modular Unit value
        process = PRODUCTS.get(product)['processes'][0]
        for key, val in PROCESSES.get(process)['subprods'].items():
            sub, prod = key.split('*2*')
            if prod == product:
                substrate = sub
                break
        material = SUBSTRATES.get(substrate)['materials'][0]

        currentMods['process'] = PROCESSES.get(process)
        currentMods['substrate'] = SUBSTRATES.get(substrate)
        currentMods['material'] = MATERIALS.get(material)

        # initialize and update sideFlow Modular Unit values, output strings
        currentMods = replace_sideFlow('side1', currentMods)
        currentMods = replace_sideFlow('side2', currentMods)

        side1 = MATERIALS.get(material)['sides'][0]
        try:
            side2 = MATERIALS.get(material)['sides'][1]
        except(IndexError):
            side2 = 'NA'

        # if a by-product exists from the chosen material, populate sideFlow1
        if side1 != 'NA':
            sub1 = SIDES.get(side1)['substrates'][0]
            proc1 = SUBSTRATES.get(sub1)['processes'][0]
            for key, val in PROCESSES.get(proc1)['subprods'].items():
                sub, prod = key.split('*2*')
                if sub == sub1:
                    prod1 = prod
                    break

            currentMods['side1'] = SIDES.get(side1)
            currentMods['sub1'] = SUBSTRATES.get(sub1)
            currentMods['proc1'] = PROCESSES.get(proc1)
            currentMods['prod1'] = PRODUCTS.get(prod1)

        # if a second by-product exists, populate sideFlow2
        if side2 != 'NA':
            sub2 = SIDES.get(side2)['substrates'][0]
            proc2 = SUBSTRATES.get(sub2)['processes'][0]
            for key, val in PROCESSES.get(proc2)['subprods'].items():
                sub, prod = key.split('*2*')
                if sub == sub2:
                    prod2 = prod
                    break

            currentMods['side2'] = SIDES.get(side2)
            currentMods['sub2'] = SUBSTRATES.get(sub2)
            currentMods['proc2'] = PROCESSES.get(proc2)
            currentMods['prod2'] = PRODUCTS.get(prod2)

        flows = assemble_flows(currentMods)
    else:
        # filter available Modular Unit values and optimize decision making
        print('Optimization and Filtering options coming soon!')
        sys.exit(0)

    return flows, currentMods


if __name__ == '__main__':
    main()
