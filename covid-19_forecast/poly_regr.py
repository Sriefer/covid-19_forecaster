#!/usr/bin/env python3

import datetime
import numpy

import matplotlib.pyplot as plt


def fit_data(data_dict, max_count, degrees=6, title=''):
    """
    Try to fit the data to a polynomial of degrees and output when the max_count it reached

    :param dict data_dict: Dictionary containing dates and totals
    :param int max_count: Maximum number to reach
    :param int degrees: Polynomial degree
    :return  None
    :rtype None
    """

    numpy.set_printoptions(suppress=True)

    x_range = range(0, len(data_dict.values()))

    x = list(x_range)
    y = list(data_dict.values())
    coeffs = numpy.polyfit(x, y, degrees)
    predict = numpy.poly1d(coeffs)

    coeffs_list = coeffs.astype(float).tolist()
    eq_str = ''
    deg = degrees
    for c in coeffs_list:
        if deg > 1:
            eq_str += '{:1.6f}x^{} + '.format(c, deg)
        elif deg == 1:
            eq_str += '{:1.6f}x + '.format(c)
        else:
            eq_str += '{:1.6f}'.format(c)

        if deg > 0 and deg % 4 == 0:
            eq_str += '\n'
        deg -= 1

    print('[+] eq_str: {}'.format(eq_str))

    # calc r2
    yhat = predict(x)
    ybar = numpy.sum(y)/len(y)
    ssreg = numpy.sum((yhat-ybar)**2)
    sstot = numpy.sum((y - ybar)**2)
    r2 = ssreg / sstot

    print('[+]   Equation:\n{}'.format(predict))
    print('[+]   r2:\t{}'.format(r2))

    last_day = next(reversed(data_dict.keys()))
    datetime_object = datetime.datetime.strptime(last_day, '%m/%d/%y')

    last_day_val = next(reversed(data_dict.values()))

    orig_date = datetime_object

    not_max = True
    cur_index = len(x)
    max_days = 100

    x1 = []
    y1 = []
    for i in x_range:
        x1.append(i)
        y1.append(predict(i))

    while(not_max):
        datetime_object += datetime.timedelta(days=1)
        date_hit = datetime_object.strftime('%m/%d/%y')
        print('{} at {:,}'.format(date_hit, int(predict(cur_index))))

        x1.append(cur_index)
        y1.append(int(predict(cur_index)))
        if predict(cur_index) < 0:
            not_max = False
            print('[-] Error: Polynomial goes negative')
            continue

        if predict(cur_index) > max_count:
            not_max = False
        cur_index += 1

        if cur_index > len(x) + max_days:
            print('[-] Failed to find max within {} days. Current prediction '
                  'is: {} on {}'
                  .format(max_days, predict(cur_index), date_hit))
            not_max = False

    fig = plt.figure()
    ax = plt.subplot()
    ax.set_xlim(0, len(x1))

    plt.title('{} for {} (Day {})'.format(title, last_day, len(x)-1))
    plt.rc('font', size=8)
    plt.text(2, max(y1) - 0.05 * max(y1), eq_str)
    plt.plot(x1, y1, 'r--', x, y, 'b--')
    plt.xlabel('Days since 1/22/20')
    plt.ylabel('Count')
    plt.grid(True)
    plt.show()

    return date_hit, int(predict(cur_index))
