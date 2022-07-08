import re


pattern1_a = re.compile(r"Interruption of", re.IGNORECASE)
pattern1_b = re.compile(r"etc\.\)", re.IGNORECASE)
pattern2_a = re.compile(r"For further", re.IGNORECASE)
pattern2_b = re.compile(r"www\.kplc\.co\.ke", re.IGNORECASE)
flag = True
with open(r'content.txt', 'r', encoding='utf-8') as myfile:
    for line in myfile:
        if pattern1_a.search(line) or pattern2_a.search(line):
            flag = False
        if flag and line.strip():
            with open('new.txt', 'a') as f:
                f.write(line)
        if pattern1_b.search(line) or pattern2_b.search(line):
            flag = True
