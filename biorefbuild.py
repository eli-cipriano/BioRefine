"""This is a one-time use library for us to develop dictionaries and write
json files"""

import json
import sys
# develop master csv of all strains and their subprods, then use
# grep and command line filtering, my_utils.py, to get lists
# of relevant values for each dict.


def write_json():
    dicts = build_dicts()
    PRODUCTS = dicts.get('PRODUCTS')
    PROCESSES = dicts.get('PROCESSES')
    SUBSTRATES = dicts.get('SUBSTRATES')
    MATERIALS = dicts.get('MATERIALS')
    SIDES = dicts.get('SIDES')
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
    ethanol = {'processes': ['anaerobic_yeast', 'thermochemical'],
               'value': 'low',
               'name': 'ethanol'
               }
    isobutanol = {'processes': ['anaerobic_ecoli', 'anaerobic_yeast'],
                  'value': 'med',
                  'name': 'isobutanol'
                  }
    biodiesel = {'processes': ['thermochemical'],
                 'value': 'high',
                 'name': 'biodiesel'
                 }
    products['ethanol'] = ethanol
    products['isobutanol'] = isobutanol
    products['biodiesel'] = biodiesel

    return products


def build_processes():
    processes = {}
    subprods = build_subprods('anaerobic_yeast')
    anaerobic_yeast = {'subprods': subprods,
                       'products': ['ethanol', 'ABE'],
                       'substrates': ['glucose'],
                       'skills': 'ferment resistent',
                       'name': 'anaerobic_yeast'
                       }
    subprods = build_subprods('anaerobic_ecoli')
    anaerobic_ecoli = {'subprods': subprods,
                       'products': ['fatty acids', 'pha'],
                       'substrates': ['glucose', 'oil', 'glycerol'],
                       'skills': 'model organism',
                       'name': 'anaerobic_ecoli'
                       }

    subprods = build_subprods('thermochemical')
    thermochemical = {'subprods': subprods,
                      'products': ['biodiesel', 'fatty acids', 'ethanol'],
                      'substrates': ['oil'],
                      'skills': None,
                      'name': 'thermochemical'
                      }
    processes['anaerobic_yeast'] = anaerobic_yeast
    processes['anaerobic_ecoli'] = anaerobic_ecoli
    processes['thermochemical'] = thermochemical

    return processes


def build_subprods(process):
    subprods = {}
    # extract combos relevant to given process from grand csv
    if process == 'anaerobic_yeast':
        glucose2ethanol = {'substrate': ['glucose'],
                           'product': ['ethanol'],
                           'strain': [('s1', 0.5, 'source'),
                                      ('s2', 0.8, 'source'),
                                      ('s3', 0.3, 'source')]
                           }
        glucose2abe = {'substrate': ['glucose'],
                       'product': ['acetone', 'ethanol', 'butanol'],
                       'strain': [('s1', 0.5, 'source'),
                                  ('s2', 0.8, 'source'),
                                  ('s3', 0.3, 'source')]
                       }
    dicts = ['glucose2ethanol', 'glucose2abe']

    if process == 'anaerobic_ecoli':
        glycerol2fattyacids = {'substrate': ['glycerol'],
                               'product': ['fattyacids'],
                               'strain': [('s1', 0.5, 'source'),
                                          ('s2', 0.8, 'source'),
                                          ('s3', 0.3, 'source')]
                               }
        glycerol2pha = {'substrate': ['glycerol'],
                        'product': ['pha'],
                        'strain': [('s1', 0.5, 'source'),
                                   ('s2', 0.8, 'source'),
                                   ('s3', 0.3, 'source')]
                        }
        glucose2fattyacids = {'substrate': ['glucose'],
                              'product': ['fattyacids'],
                              'strain': [('s1', 0.5, 'source'),
                                         ('s2', 0.8, 'source'),
                                         ('s3', 0.3, 'source')]
                              }
        dicts = ['glycerol2fattyacids', 'glycerol2pha', 'glucose2fattyacids']

    if process == 'thermochemical':
        oil2biodiesel = {'substrate': ['oil'],
                         'product': ['biodiesel'],
                         'strain': [()],
                         }
        oil2ethanol = {'substrate': ['oil'],
                       'product': ['ethanol'],
                       'strain': [()],
                       }
        dicts = ['oil2biodiesel', 'oil2ethanol']

    for dic in dicts:
        subprods[dic] = eval(dic)

    return subprods


def build_substrates():

    substrates = {}
    glucose = {'materials': ['corn', 'sugarcane'],
               'processes': ['anaerobic_yeast',
                             'anaerobic_ecoli',
                             'thermochemical'],
               'name': 'glucose'
               }
    oil = {'materials': ['poplar', 'oil'],
           'processes': ['thermochemical'],
           'name': 'oil'
           }

    substrates['glucose'] = glucose
    substrates['oil'] = oil

    return substrates


def build_materials():
    materials = {}
    with open('data_mat2sub.csv', 'r') as f:
        header = f.readline()
        for line in f:
            a = line.rstrip().split(',')
            material = a[0]
            substrate = a[1]
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
    # for material, val in materials.items():
    #     print(material, val)
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

        sides[side] = {'name': side,
                       'substrates': substrates,
                       'treatments': treatments}
    return sides


def get_column(file_name,
               query_column=None,
               query_value=None,
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

                    matches = True
                    for i, query in enumerate(query_value):
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
