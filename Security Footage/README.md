Commands used on TryHackMe room Security Footage https://tryhackme.com/room/securityfootage

extract all files / images from pcap file:

binwalk --dd='.*' -e security-footage-1648933966395.pcap

foremost -i security-footage-1648933966395.pcap -o output_dir

Generate a video from a list of images:

ffmpeg -framerate 10 -pattern_type glob -i '*.jpg'   -c:v libx264 footage.mp4

Generate a gif from from a list of images:

ffmpeg -framerate 10 -pattern_type glob -i '*.jpg'  -vf "scale=640:-1:flags=lanczos" output.gif

convert -delay 20 -loop 0 *.jpg output2.gif

Generate a pdf file from a list of images:

convert  *.jpg output.pdf
