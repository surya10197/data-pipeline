#!/usr/bin/env bash

echo 'Creating virtual environment...'
virtualenv -p python3 env

echo 'Activating virtual environment'
source env/bin/activate

echo 'Getting current woring directory'
curr_dir=`pwd`
mkdir -p $curr_dir'/Images'

echo 'Installing dependencies...'
pip3 install -r requirements.txt

echo 'Data pipeline started...Please check the pipeline.log file for more information'
python run.py

