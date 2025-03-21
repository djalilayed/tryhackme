Tshark command used:

tshark -C tryhackme -r challenge.pcapng -Y "http.request.uri contains \"ORD%28MID%28%28SELECT%20IFNULL%28CAST%28%60description%60%20AS%20NCHAR%29%2C0x20%29%20FROM%20profile_db.%60profiles%60%20ORDER%20BY%20id%20LIMIT\" and http.request.uri contains \"description\" and http.response.code == 200 " -T fields -e frame.number -e http.content_length  -e http.request.uri  -E separator=, -E quote=d | python3 -c 'import sys, urllib.parse; [print(urllib.parse.unquote(line), end="") for line in sys.stdin]' > 1.csv

csv file is start like below:

"2940","156","/search_app/search.php?query=1 AND ORD(MID((SELECT IFNULL(CAST(`description` AS NCHAR),0x20) FROM profile_db.`profiles` ORDER BY id LIMIT 0,1),1,1))>64"
"2955","156","/search_app/search.php?query=1 AND ORD(MID((SELECT IFNULL(CAST(`description` AS NCHAR),0x20) FROM profile_db.`profiles` ORDER BY id LIMIT 0,1),3,1))>64"
"2956","156","/search_app/search.php?query=1 AND ORD(MID((SELECT IFNULL(CAST(`description` AS NCHAR),0x20) FROM profile_db.`profiles` ORDER BY id LIMIT 0,1),2,1))>64"


example command used to find the last character: 

grep -i "LIMIT 6,1),41,1" 1.csv > youtube/limit61.csv
