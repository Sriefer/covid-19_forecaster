This is a work in progress.

The goal of this project is try to ROUGHLY forecast when the counts for infected and fataly hit a specific number in the US assuming nothing changes and we stay on the same curve.  This script will download JHU data from https://github.com/CSSEGISandData.

As mentioned this is a rough approximation and comes with all the perils of polynomial regression.

This uses python3.  A pre-built version is located in build.  `example.sh` can be used to install python dependencies, give the usage of they python executable, and run the it.

Output on 4/4/20
```
(py_venv) $ python ./covid-19_forecast.pyz
[+] Going to try and fit a 6-degree polynomial
[+] Maximum infected:  1,000,000
[+] Maximum fatality:  100,000
[+] Getting COVID-19 data from https://github.com/CSSEGISandData/COVID-19.git
[+] Wrote COVID-19 data to build/covid_data
[+] Last commit:     04/04/2020 01:20:17 UTC
[+] Current time:    04/04/2020 06:07:17 UTC
[+] Reading in US confirmed cases
[+] First day found:     1/22/20 with 1
[+] Last day found:  4/3/20 with 275582
[+] Processed 3254 entries
[+] Reading in US fatal cases
[+] First day found:     1/22/20 with 0
[+] Last day found:  4/3/20 with 7087
[+] Processed 3254 entries
[+]   Equation:
           6            5          4        3       2
1.098e-06 x + 0.001852 x - 0.2498 x + 11.4 x - 212 x + 1426 x - 1916
[+]   r2:   0.9989947109677593
[+] Infect hits 1,000,000 on 04/15/20
[+]   Equation:
           6             5           4          3         2
2.578e-06 x - 0.0004573 x + 0.03067 x - 0.9586 x + 13.82 x - 76.81 x + 87.57
[+]   r2:   0.9988011042709928
[+] Fatalities hits 100,000 on 04/23/20
```

Updates, fixes, suggestions, etc. are all welcome.

Stay safe.
