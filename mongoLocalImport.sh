#!/bin/bash
mongoimport --db Data-Backup --collection data20210421 --file owid-covid-data.csv --type csv --headerline
