import sys
import datetime as dt
from matplotlib import pyplot as plt


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

                if query_value is None:
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

                elif a[query_column] == query_value:

                    if date_column is not None:
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

                    # append result values to results list
                    # case for single columns
                    if type(result_column) == int:
                        value = a[result_column]
                        # convert to ints if possible
                        try:
                            value = int(value)
                        except(ValueError):
                            pass
                        results.append(value)

                    # case for multiple columns
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

    # handle file error exception
    except FileNotFoundError:
        print('\nCould not read ' + file_name)
        sys.exit(2)

    return results


def get_daily_count(totals):
    """Return a list of daily values converted from cummulative values.

    Parameters:
    -----------
    totals: list of int, must be cummulative data and have continuous dates.

    Returns:
    --------
    daily: a list ofint, converted daily values.
    """
    # input is a list of cummulative cases/deaths in a state or
    daily = []
    for i, num in enumerate(totals):

        # day 1 boundary condition
        if i == 0:
            daily.append(num)
        else:
            daily_count = num - totals[i-1]
            if daily_count < 0:
                daily_count = 0

            daily.append(daily_count)

    return daily


def running_average(data, window=5):
    """Return a list of running averages.

    Parameters:
    -----------
    data: list of int, daily data that needs to be smoothed
    window: int, size of window used to calculate running avg

    Returns:
    --------
    running_avg: list of int, values from data over
    """
    running_avg = []

    # edge case for when window is too large
    if window > len(data):
        window = len(data)

    for i, value in enumerate(data):
        try:
            window_vals = data[i:window+i]

        except(IndexError):
            # most current running average calculated
            break
        running_avg.append(sum(window_vals)/len(window_vals))

    return running_avg


def lin_search(key, L, search_index=0, result_index=1):
    """Perform linear search for key in L

    Parameters:
    ----------
    key: any type, must be same type as keys in L
    L: list of lists
    search_index: int, index of lists in L used for search
    result_index: int, index of lists in L for results

    Returns:
    --------
    None: if not found
    value: if found
    """
    s = search_index
    r = result_index
    for val in L:
        if L[s] == key:
            return L[r]
    return None


def bin_search(key, L, search_index=0, result_index=1):
    """Perform binary search for key in L

    Parameters:
    ----------
    key: any type, must be same type as keys in L
    L: list of lists, must be sorted by one of its items
    search_index: int, index of lists in L used for search
    result_index: int, index of lists in L for results

    Returns:
    --------
    None: if not found
    value: if found
    """
    s = search_index
    r = result_index
    start = 0
    end = len(L)

    while (end - start) > 1:
        mid = (start + end)//2
        if key == L[mid][s]:
            return L[mid][r]
        elif key < L[mid][s]:
            end = mid
        else:
            start = mid
    return None


def get_rates(results,
              result_column=0,
              key='Denver',
              state='Colorado',
              year_col=7):
    """Take a list of raw values and divide by county population

    Parameters:
    ----------
    results: list or list of lists, to be converted to rates
    result_column: int, if results has many columns,
                   specify which is being converted
    key: str, specify county of interest
    state: str,specify state of county in key

    Returns:
    --------
    rates: list of lists containing raw values and new rates
    """

    pop_vals = get_column('co-est2019-alldata.csv',
                          query_column=5,
                          query_value=state,
                          result_column=[6, year_col])

    # values already sorted alphabetically by county
    key_pop = bin_search(key+' County',
                         pop_vals)

    # case struct for different scenarios
    if key_pop is None:
        print('County not found in state {}.'.format(state))
        sys.exit(3)

    if type(results[0]) == list:
        for r in results:
            r.append(r[result_column]/key_pop)
        rates = results
    elif type(results[0]) == int or type(results[0]) == float:
        rates = []
        for r in results:
            rates.append([r, r/key_pop])
    else:
        print('Rates must be calculated from numerical data')
        sys.exit(1)
    return rates


def plot_lines(points, labels, file_name):
    """Take a list of list of points and plot each list as a line.

    Parameters
    ----------
    points : list of list of points
    Each sublist corresponds to the points for one element.
    Each point has two values, the first will be the X value
    and the second the Y value
    labels : list of strings
    Each element in lables corresponds to the sublist at the
    same poisiting in data
    file_name : string
    Name of the output file.
    """
    fig = plt.figure(figsize=(10, 3), dpi=300)
    ax = fig.add_subplot(1, 1, 1)
    i = 0
    for L in points:
        X = []
        Y = []
        for pairs in L:
            X.append(pairs[0])
            Y.append(pairs[1])

        ax.plot(X, Y, lw=0.5)
        ax.text(X[-1], Y[-1], labels[i], size=5)
        i += 1
    plt.savefig(file_name, bbox_inches='tight')

    return None
