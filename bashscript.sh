#!/bin/bash
x=1
y=$((x + 1))
echo "$y"
while true; do
    y=$((y + 1))
    echo "$y"
    if [ "$y" -gt "10" ]; then
        break
    else
        echo "bobao"
    fi
done
echo "$SECONDS"
sleep 1
find -iname '*.html'
cat 'arquivo'
clear
find -iname '*.html' | awk -F. '{ print $2}'
