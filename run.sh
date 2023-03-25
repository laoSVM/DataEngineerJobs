#!/bin/bash

for location in "California" "New York" "San Francisco" "Chicago"; do
    for profession in "Data Engineer" "Data Analyst"; do
        python main.py -l "$location" -p "$profession"
    done 
done
