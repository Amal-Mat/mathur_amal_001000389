#!/usr/bin/env bash

read -p "Enter your Birth Date in the format [MM/DD/YYYY]: " birth_date

echo "$birth_date" | awk -F '/' '{ sum = 0;
		for(i=1; i<=NF; i++){
		j=int($i);
                        	while(j>=1) {
                        sum += j%10;
                    j = int(j/10);
		}
		}
			print "Sum of digits: ", sum;
	}'
