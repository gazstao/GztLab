#!/bin/bash
COLLECTION = "$1"
mongoimport mongodb+srv://owner:{}@cluster0.uvhcq.mongodb.net/Data-Backup --collection $COLLECTION --file owid-covid-data.csv --type csv --headerline
