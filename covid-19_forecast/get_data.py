#!/usr/bin/env python3

import datetime
import git
import os
import time


def get_data():
    """
    Get the lastest COVID-19 data from JHU

    :return  Latest update on success, None on failure
    :rtype String
    """
    repo_url = 'https://github.com/CSSEGISandData/COVID-19.git'
    covid_data = 'covid_data'

    cwd = os.getcwd()

    covid_data = os.path.join(cwd, covid_data)

    exists = os.path.exists(covid_data)
    if not exists:
        print('[+] Getting COVID-19 data from {}'.format(repo_url))
        repo = git.Repo.clone_from(repo_url, covid_data)
        print('[+] Wrote COVID-19 data to {}'.format(covid_data))
    else:
        print('[+] Found COVID-19 data at {}'.format(covid_data))
        repo = git.Repo(covid_data)

    # Make sure the lastest is pulled down
    orig = repo.remotes.origin
    orig.pull()

    last_commit = repo.iter_commits('master', max_count=1)
    last_commit_date = repo.head.commit.committed_date
    last_commit_date_str = time.strftime("%m/%d/%Y %H:%M:%S %Z", time.gmtime(last_commit_date))
    return last_commit_date_str


if __name__ == '__main__':
    time_str = get_data()
    print('[+] Last commit:\t {}'.format(time_str))
    cur_time = datetime.datetime.utcnow()
    cur_time_str = cur_time.strftime("%m/%d/%Y %H:%M:%S")
    print('[+] Current time:\t {} UTC'.format(cur_time_str))
