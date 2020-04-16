#!/usr/bin/env python3

import collections
import csv
import os
import re
import sys


def read_in_csv(file_name):
    """
    Ingest csv data

    :param str file_name: File name to read
    :return  dict {date, daily total} on success, None on failure
    :rtype dictionary
    """

    if not os.path.exists(file_name):
        print('[-] Failed to find file: {}'.format(file_name))
        return None

    # Get sum for each day
    data_dates = collections.OrderedDict()
    data_dates_sum = collections.OrderedDict()
    with open(file_name, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        line_count = 0
        for row in csv_reader:
            # Get index for each day in first line
            if line_count == 0:
                pattern = re.compile(r'(\d+/\d+/\d+)')

                index = 0
                for i in row:
                    if pattern.match(i):
                        data_dates[i] = index
                    index += 1

                first_day = next(iter(data_dates.keys()))
                last_day = next(reversed(data_dates.keys()))
                line_count += 1
                continue

            for day in data_dates.keys():
                index = data_dates[day]

                # 4/15/20 Updated added floats to daily values
                try:
                    tmp_val = int(row[index])
                except ValueError:
                    tmp_val = int(float(row[index]))

                if day not in data_dates_sum.keys():
                    data_dates_sum[day] = tmp_val
                else:
                    data_dates_sum[day] += tmp_val
            line_count += 1

    print('[+] First day found:\t {} with {:,}'.format(first_day, data_dates_sum[first_day]))
    print('[+] Last day found:\t {} with {:,}'.format(last_day, data_dates_sum[last_day]))
    print('[+] Processed {:,} entries'.format(line_count))

    return data_dates_sum


if __name__ == '__main__':
    print('[+] Calculating daily infected')
    file_name = 'covid_data/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv'
    data_dates_sum = read_in_csv(file_name)
    if not data_dates_sum:
        sys.exit(-1)

    for key, value in data_dates_sum.items():
        print(key, value)
