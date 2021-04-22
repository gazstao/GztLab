#!/bin/bash
mongoimport mongodb+srv://owner:zer0@cluster0.uvhcq.mongodb.net/Data-Backup --collection data20210421 --file owid-covid-data.csv --type csv --headerline
