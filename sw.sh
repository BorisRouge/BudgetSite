#!/bin/sh
cd venv/bin
source activate
cd ..
cd ..
cd budget
python3 manage.py runserver
