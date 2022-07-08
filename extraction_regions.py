import pprint
import re

regions = {}
region_regex = re.compile(r"region", re.IGNORECASE)
area_regex = re.compile(r"area", re.IGNORECASE)
county_regex = re.compile(r"county", re.IGNORECASE)
previous_line = ''
with open('new.txt', 'r') as r:
    for line in r.readlines():
        if region_regex.search(line):
            region_name = " ".join(line.split()[:-1])
            county_name = ''
            continue
        if county_regex.search(line) and not 'offices' in line.casefold():
            county_name = line.casefold().replace('parts of', '')
            county_name = ' '.join(county_name.split()[:-1]).upper()
            continue
        if area_regex.search(line):
            when = ''
            where = ''
            area_name = ''.join(line.split(':')[1:]).strip().lower()
            if county_name == '':
                county_name = region_name
            continue
        if 'date:' in line.casefold() or 'time:' in line.casefold():
            when += line.strip()
            continue
        where += line
        regions.setdefault(region_name, {})
        regions[region_name].setdefault(county_name, {})
        regions[region_name][county_name].setdefault(area_name, {'when': '', 'where': ''})
        if regions[region_name][county_name][area_name]['when'] == '':
            regions[region_name][county_name][area_name]['when'] = ''.join(when).lower()
        regions[region_name][county_name][area_name]['where'] += line.strip().lower()
with open('region.txt', 'w') as w:
    w.write(pprint.pformat(regions))
