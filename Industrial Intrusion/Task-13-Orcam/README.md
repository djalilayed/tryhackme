tryhackme room Orcam part of Industrial Intrusion CTF https://tryhackme.com/room/industrial-intrusion

YouTube video walk throug: https://youtu.be/uGhuElHm1Ys

Scenario: You get an email with attachment, Microsoft docm file. with Macro enable. you need to analyses the VBA code inside the macro to get the flag.

pip3 install eml-extractor

eml-extractor -r writing_template.eml
pip3 install oletools
oleid  Project_Template.docm
olevba Project_Template.docm

unzip Project_Template.docm -d docm_contents

olevba docm_contents/word/vbaProject.bin
