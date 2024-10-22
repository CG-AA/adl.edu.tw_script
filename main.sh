#!/bin/bash

# Prompt the user for input
read -p "Enter the number of times to loop: " count

suc=0

# Loop the specified number of times
for ((i=1; i<=count; i++))
do
    res=$(cat cURL.txt | bash)
    # if message is {"msg":"\u7b54\u5c0d\u4e86\uff01"} add 1 to suc
    if [ "$res" == '{"msg":"\u7b54\u5c0d\u4e86\uff01"}' ]; then
        suc=$((suc + 1))
        echo "success"
        echo $suc
        echo $((suc * 100 / count))"%"
    fi
done