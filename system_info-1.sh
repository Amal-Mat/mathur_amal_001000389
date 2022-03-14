#!/usr/bin/env bash

a=$(uname -r)

echo "Kernel Release: $a"
echo "Bash Version: ${BASH_VERSION}"
echo "Free Storage: $(df -ha)"
echo "Free Memory: $(free)"
echo "Total files in any PWD: $(ls -la | wc -l)"
echo "IP Address: $(hostname -I)"
echo "Interfaces active: $(nmcli dev status | grep "connected \| unmanaged" | awk '{ ORS="" }; {print $1}')"
