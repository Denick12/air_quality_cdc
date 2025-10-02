#!/bin/bash
pip install -r /requirements.txt
airflow db upgrade
airflow users create \
    --username admin \
    --firstname Admin \
    --lastname User \
    --role Admin \
    --email admin@example.com \
    --password admin
