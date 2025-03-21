# script used on tryhackme Hackfinity Battle Sequel Dump https://tryhackme.com/room/HackfinityBattle
# script geneate by Claudi Ai, Google Gemini and Grok
# video walk through: https://youtu.be/Wjz8igduiDw

import re
from collections import defaultdict
import csv
from io import StringIO

def parse_csv_data(csv_content):
    """Parse CSV content into a list of dictionaries, handling no header and 3 columns"""
    # Use StringIO to treat the string content as a file-like object for csv.reader
    f = StringIO(csv_content.strip())
    reader = csv.reader(f, quotechar='"')
    
    data = []
    for line in reader:  # Iterate directly over reader
        if len(line) == 3:  # Expect 3 columns: "No.", "Content length", "Request URI"
            entry = {
                "Request URI": line[2],  # 3rd column (index 2)
                "Content length": line[1]  # 2nd column (index 1)
            }
            data.append(entry)
    
    return data

# The rest of the script remains unchanged
def analyze_sql_injection(csv_data):
    row_lengths = {}
    char_data = defaultdict(lambda: defaultdict(dict))
    
    for row in csv_data:
        uri = row.get("Request URI", "")
        
        if "query=1 AND" not in uri:
            continue
        
        content_length = row.get("Content length", "")
        if not content_length:
            continue
            
        try:
            content_length = int(content_length)
        except ValueError:
            continue
        is_true = content_length > 150
        
        limit_match = re.search(r'LIMIT (\d+),1', uri)
        if not limit_match:
            continue
            
        row_num = int(limit_match.group(1))
        
        if "CHAR_LENGTH" in uri:
            comp_match = re.search(r'>(\d+)', uri)
            if comp_match:
                value = int(comp_match.group(1))
                
                if is_true:
                    row_lengths.setdefault(row_num, {"min": 0, "max": 100})
                    row_lengths[row_num]["min"] = max(row_lengths[row_num]["min"], value)
                else:
                    row_lengths.setdefault(row_num, {"min": 0, "max": 100})
                    row_lengths[row_num]["max"] = min(row_lengths[row_num]["max"], value)
        else:
            pos_match = re.search(r'MID\(.*?,(\d+),1\)', uri)
            if not pos_match:
                continue
                
            pos = int(pos_match.group(1))
            
            comp_match = re.search(r'>(\d+)', uri)
            if not comp_match:
                continue
                
            value = int(comp_match.group(1))
            
            if is_true:
                char_data[row_num][pos].setdefault("min", 0)
                char_data[row_num][pos]["min"] = max(char_data[row_num][pos]["min"], value)
            else:
                char_data[row_num][pos].setdefault("max", 127)
                char_data[row_num][pos]["max"] = min(char_data[row_num][pos]["max"], value)
    
    final_lengths = {}
    for row_num, data in row_lengths.items():
        if data["max"] < 100:
            final_lengths[row_num] = data["min"] + 1
        else:
            final_lengths[row_num] = data["min"] + 1
    
    extracted_data = {}
    for row_num in char_data.keys():
        text = ""
        max_pos = max(char_data[row_num].keys()) if char_data[row_num] else 0
        
        for pos in range(1, max_pos + 1):
            if pos in char_data[row_num]:
                min_val = char_data[row_num][pos].get("min", 0)
                max_val = char_data[row_num][pos].get("max", 127)
                
                char_val = min_val + 1
                
                if 32 <= char_val <= 126:
                    text += chr(char_val)
                else:
                    text += f"[{char_val}]"
            else:
                text += "?"
        extracted_data[row_num] = text
    
    return final_lengths, extracted_data

def main(csv_content):
    """Main function to process the CSV data"""
    csv_data = parse_csv_data(csv_content)
    row_lengths, extracted_data = analyze_sql_injection(csv_data)
    
    print("Detected row lengths:")
    for row_num, length in sorted(row_lengths.items()):
        print(f"Row {row_num}: {length} characters")
    
    print("\nExtracted data:")
    for row_num, text in sorted(extracted_data.items()):
        print(f"Row {row_num}: {text}")
    
    if 6 in extracted_data:
        print("\nPotential flag (Row 6):")
        print(extracted_data[6])
    
    return extracted_data

# Example usage
with open('1.csv', 'r') as f:
    csv_content = f.read()
extracted_data = main(csv_content)
