#!/usr/bin/env python3

import argparse
import datetime

import csv_data
import get_data
import poly_regr


def main():
    parser = argparse.ArgumentParser(description='Estimages date when COVID-19 will hit certain values. '
                                                 'This will download JHU data https://github.com/CSSEGISandData')
    parser.add_argument('-d', '--degrees', default=6, type=int, help='Nth degree polynomial for polynomial regression')
    parser.add_argument('-i', '--infected', default=1000000, type=int, help='Max infected')
    parser.add_argument('-f', '--fatalities', default=100000, type=int, help='Max fatalities')
    args = parser.parse_args()

    print('[+] Going to try and fit a {}-degree polynomial'.format(args.degrees))
    print('[+] Maximum infected:  {:,}'.format(args.infected))
    print('[+] Maximum fatality:  {:,}'.format(args.fatalities))

    # Get latest data
    time_str = get_data.get_data()
    print('[+] Last commit:\t {}'.format(time_str))

    # Print current time for comparison
    cur_time = datetime.datetime.utcnow()
    cur_time_str = cur_time.strftime("%m/%d/%Y %H:%M:%S")
    print('[+] Current time:\t {} UTC'.format(cur_time_str))

    # Read in data
    print('[+] Reading in US confirmed cases')
    infect_file = 'covid_data/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv'
    infected = csv_data.read_in_csv(infect_file)

    last_infected_day = next(reversed(infected.keys()))

    print('[+] Reading in US fatal cases')
    fatality_file = 'covid_data/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_US.csv'
    fatalities = csv_data.read_in_csv(fatality_file)

    last_fatality_day = next(reversed(fatalities.keys()))

    degrees = args.degrees
    hit_val = args.infected
    if infected[last_infected_day] > hit_val:
        print('[+] Already passed {:,} for infected'.format(hit_val))
    else:
        date_hit, predict_val = poly_regr.fit_data(infected, hit_val, degrees)
        print('[+] Infection hits {:,} on {} at {:,}'.format(hit_val, date_hit, predict_val))

    hit_val = args.fatalities
    if fatalities[last_fatality_day] > hit_val:
        print('[+] Already passed {:,} for fatalities'.format(hit_val))
    else:
        date_hit, predict_val = poly_regr.fit_data(fatalities, hit_val, degrees)
        print('[+] Fatalities hit {:,} on {} at {:,}'.format(hit_val, date_hit, predict_val))


if __name__ == '__main__':
    main()
