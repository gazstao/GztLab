#!/bin/bash
mongoimport mongodb+srv://owner:zer0@cluster0.uvhcq.mongodb.net/gzt-lab --collection data-history --file owid-covid-data.csv --type csv --headerline
