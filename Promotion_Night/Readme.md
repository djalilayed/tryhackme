below from Tryhackme room Promotion Night First Shift CTF https://tryhackme.com/room/first-shift-ctf
YouTube video walk through: https://youtu.be/iq41S-HWBeE

**Below commands used on TryHackMe room Promotion Night First Shift CTF YouTube video walk through:**

Below query is based on initial query shared by user Ph1sherman at TryHackMe discord

```
index=* sourcetype="wineventlog"  EventCode=4104
| rex field=_raw "Creating Scriptblock text \((?<part>\d+) of (?<total>\d+)\):"
| rex field=_raw "(?s)\):\s*(?<chunk>.*?)\s*ScriptBlock ID:"
| sort 0 ScriptBlock_ID part
| stats list(chunk) as scriptblock by ScriptBlock_ID
| eval scriptblock=mvjoin(scriptblock, "")
| eval sb_len=len(scriptblock)
| table ScriptBlock_ID sb_len scriptblock
| sort - sb_len
```

index=* sourcetype="wineventlog" EventCode=4104
Pulls PowerShell Script Block Logging events (4104).
These are the logs that contain the actual PowerShell code that ran.

| rex field=_raw "Creating Scriptblock text \((?<part>\d+) of (?<total>\d+)\):"
Looks inside the raw log text and extracts:

part = which chunk this is (1, 2, 3, …)

total = how many chunks exist for that scriptblock
Example: “(2 of 5)” means this event contains chunk 2 out of 5.

| rex field=_raw "(?s)\):\s*(?<chunk>.*?)\s*ScriptBlock ID:"
Extracts the actual code text from this event into a field called chunk.
It grabs everything after the “):” up to “ScriptBlock ID:”.
The (?s) part means “treat newlines as normal characters,” so it can capture multi-line code.

| sort 0 ScriptBlock_ID part
Sorts so that for each scriptblock:

chunk 1 comes before chunk 2,

chunk 2 before chunk 3, etc.
sort 0 means “don’t limit results while sorting” (important when there are many events).

| stats list(chunk) as scriptblock by ScriptBlock_ID
Groups events by ScriptBlock_ID (each ID = one PowerShell scriptblock).
For each scriptblock ID, it collects all the chunks into a list in the right order.

| eval scriptblock=mvjoin(scriptblock, "")
Joins that list of chunks into one single full script text (no separator).
This is the “stitching back together” step.

| eval sb_len=len(scriptblock)
Calculates the length of the rebuilt scriptblock (sb_len).
Long scripts are often the suspicious ones (encoded payloads, loaders, etc.).

| table ScriptBlock_ID sb_len scriptblock
Displays only:

the ScriptBlock ID,

its length,

the reconstructed full script.

| sort - sb_len
Sorts so the longest scriptblocks appear first (highest chance of being the malicious loader with the big Base64 blob).
