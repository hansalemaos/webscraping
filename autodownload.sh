#!/bin/bash

rm * -f

check_if_finished_writing() {
    timeout2=$(($SECONDS + timeoutfinal))

    while true; do
        if [ $SECONDS -gt "$timeout2" ]; then
            return 1
        fi
        initial_size=$(stat -c %s "$1")
        sleep "$2"
        current_size=$(stat -c %s "$1")
        if [ "$current_size" -eq "$initial_size" ]; then
            return 0
        fi
    done
}

while true; do
    input tap 840 50
    sleep 1.5
    file_contents=$(ls *.html -1 | tail -n 1)

    if [ -z "$file_contents" ]; then
        continue
    else
        if check_if_finished_writing "$file_contents" 0.1; then
            cat "$file_contents"
            rm * -f
        fi
    fi
done
