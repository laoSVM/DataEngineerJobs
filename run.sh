#!/bin/bash

us_states=(
    'Alabama United States' 'Alaska United States' 'Arizona United States' 'Arkansas United States' 
    'California United States' 'Colorado United States' 'Connecticut United States' 'Delaware United States' 
    'Florida United States' 'Georgia United States' 'Hawaii United States' 'Idaho United States' 
    'Illinois United States' 'Indiana United States' 'Iowa United States' 'Kansas United States' 
    'Kentucky United States' 'Louisiana United States' 'Maine United States' 'Maryland United States' 
    'Massachusetts United States' 'Michigan United States' 'Minnesota United States' 'Mississippi United States' 
    'Missouri United States' 'Montana United States' 'Nebraska United States' 'Nevada United States' 
    'New Hampshire United States' 'New Jersey United States' 'New Mexico United States' 'New York United States' 
    'North Carolina United States' 'North Dakota United States' 'Ohio United States' 'Oklahoma United States' 
    'Oregon United States' 'Pennsylvania United States' 'Rhode Island United States' 'South Carolina United States' 
    'South Dakota United States' 'Tennessee United States' 'Texas United States' 'Utah United States' 
    'Vermont United States' 'Virginia United States' 'Washington United States' 'West Virginia United States' 
    'Wisconsin United States' 'Wyoming United States'
)

for location in "${us_states[@]}"; do
    for profession in "Data Engineer" "Data Analyst"; do
        python main.py -l "$location" -p "$profession"
    done 
done
echo "Job completed successfully"