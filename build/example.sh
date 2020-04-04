#!/bin/bash

# install python requirements
pip install -r ./requirements.txt

# print help
python3 covid-19_forecast.pyz -h

# run with default values
python3 covid-19_forecast.pyz
