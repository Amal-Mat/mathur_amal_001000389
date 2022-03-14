#!/usr/bin/env bash

read -p "Enter the File Name to be sent through email: " f_name
read -p "Enter the receiver's Email ID: " email_id

if [[ "$email_id" =~ ^[a-zA-Z0-9]+[_.+-]?[a-zA-Z0-9]+@northeastern.edu$ ]]
then
  echo "Email ID is valid"
else
  echo "Enter a valid Northeastern Email ID"
  exit 1
fi

cat ~/test_file-3 | s-nail -s 'Subject' -a $f_name $email_id

if [ "$?" -eq 0 ]
then
  echo "Email is sent successfully!"
else
  echo "Sending an email was unsuccessful!"
fi
