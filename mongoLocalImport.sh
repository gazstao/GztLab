#!/bin/bash
mongoimport --db Data-Backup --collection data20210419 --file owid-covid-data.csv --type csv --headerline
