#!/usr/bin/env python3

import datetime
import numpy

from sklearn.preprocessing import PolynomialFeatures


def fit_data(data_dict, max_count, degrees=6):
    """
    Try to fit the data to a polynomial of degrees and output when the max_count it reached

    :param dict data_dict: Dictionary containing dates and totals
    :param int max_count: Maximum number to reach
    :param int degrees: Polynomial degree
    :return  None
    :rtype None
    """

    numpy.set_printoptions(suppress=True)

    x = list(range(0, len(data_dict.values())))
    y = list(data_dict.values())
    coeffs = numpy.polyfit(x, y, degrees)
    predict = numpy.poly1d(coeffs)

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

    orig_date = datetime_object

    not_max = True
    cur_index = len(x)
    max_days = 100

    while(not_max):
        datetime_object += datetime.timedelta(days=1)
        date_hit = datetime_object.strftime('%m/%d/%y')
        if predict(cur_index) > max_count:
            not_max = False
        cur_index += 1

        if cur_index > len(x) + max_days:
            print('[-] Failed to find max within {} days. Current prediction '
                  'is: {} on {}'
                  .format(max_days, predict(cur_index), date_hit))
            not_max = False

    return date_hit, int(predict(cur_index))
