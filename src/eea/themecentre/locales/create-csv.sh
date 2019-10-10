#!/usr/bin/env bash

# how to install po2csv (and related commands) on devel machines
# apt-get update
# apt-get install python python-dev
# apt-get install translate-toolkit

# loop through each folder
for d in */ ; do
    OutFileName="${d::-1}-merged.csv"
    FormattedFileName="${d::-1}-formatted.csv"
    # echo "${d::-1}-merged.csv"

    # create csv folder
    mkdir -p "$d/csv"

    # po2csv LC_MESSAGES folder to csv folder
    po2csv "$d/LC_MESSAGES" "$d/csv"

    # loop through csv files and merge them into 1
    index=0
    for filename in $d/csv/*.csv; do
        if [ "$filename"  != "$d/csv/$OutFileName" ] && [ "$filename" != "$d/csv/$FormattedFileName" ] && [ "$filename" != "$d/csv/eea.csv" ] ;
        then 
          if [[ $index -eq 0 ]] ; then 
              head -1  "$filename" >   "$d/csv/$OutFileName" # Copy header if it is the first file
          fi
          tail -n +2  "$filename" >>  "$d/csv/$OutFileName" # Append from the 2nd line each file
          index=$(( $index + 1 ))
        fi
    done

    # empty formatted file, disable empty after correct generation
    > "$d/csv/$FormattedFileName"

    # remove first column containing location
    cut -d, -f1 --complement "$d/csv/$OutFileName" >> "$d/csv/$FormattedFileName"

    # replace headers
    sed -i '1s/.*/message in EN, message in <ISO-code>/' "$d/csv/$FormattedFileName"
done

# format headers with iso codes
python iso_codes.py