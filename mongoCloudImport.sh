#!/bin/bash
COLLECTION = "$1"
mongoimport mongodb+srv://owner:zer0@cluster0.uvhcq.mongodb.net/Data-Backup --collection $COLLECTION --file owid-covid-data.csv --type csv --headerline
