#!/usr/bin/env bash

read -p "Enter a postal code: " postal_code

regex_U="^[[:digit:]]{5}$"
regex_C="^[^DFIOQUWZa-z][0-9][^DFIOQUa-z] [0-9][^DFIOQUa-z][0-9]$"

if [[ $postal_code =~ $regex_U ]]
then
  echo "USA"
elif [[ $postal_code =~ $regex_C ]]
then
  echo "Canada"
else
  echo "None"
fi
