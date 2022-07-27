import codecs
import re
import shelve
import textract
import os


def extract_pdf():
    os.makedirs('telebot/content', exist_ok=True)
    textract_text = textract.process(f'../../../Desktop/kplc/Interruptions - 21.07.2022.pdf')
    textract_str_text = codecs.decode(textract_text)
    with open(f'telebot/content/extracted_data.txt', 'w') as f:
        f.write(textract_str_text.strip('\n'))


def clean_extracted_data():
    pattern1_a = re.compile(r"Interruption of", re.IGNORECASE)
    pattern1_b = re.compile(r"etc\.\)", re.IGNORECASE)
    pattern2_a = re.compile(r"For further", re.IGNORECASE)
    pattern2_b = re.compile(r"www\.kplc\.co\.ke", re.IGNORECASE)
    flag = True
    with open('telebot/content/cleaned_data.txt', 'w'):
        pass

    with open(r'telebot/content/extracted_data.txt', 'r', encoding='utf-8') as myfile:
        for line in myfile:
            if pattern1_a.search(line) or pattern2_a.search(line):
                flag = False
            if flag and line.strip():
                with open('telebot/content/cleaned_data.txt', 'a') as f:
                    f.write(line)
            if pattern1_b.search(line) or pattern2_b.search(line):
                flag = True


def save_data_to_shelve():
    regions = {}
    region_regex = re.compile(r"region", re.IGNORECASE)
    area_regex = re.compile(r"area:", re.IGNORECASE)
    county_regex = re.compile(r"county", re.IGNORECASE)
    previous_line = ''
    with open('telebot/content/cleaned_data.txt', 'r') as r:
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
    f = shelve.open('telebot/content/data_file')
    f['regions'] = regions
    f.close()


def area_list(county, regions):
    for region in regions.keys():
        if county.strip().upper() in regions[region].keys():
            print(region)
            areas = [area for area in regions[region][county.strip().upper()].keys()]
            print(areas)
            if '' in areas:
                areas.remove('')
            return areas
        else:
            continue
    return None


def place_list(county, area, regions):
    county = county.strip().upper()
    for region in regions.keys():
        if county in regions[region].keys():
            time_outage = regions[region][county][area]['when'].upper()
            time_outage = re.sub('(\s\s\s)+', '', time_outage)
            time_outage = '\nTIME'.join(time_outage.split('TIME'))
            place_outage = [place.strip().capitalize() for place in
                            ''.join(regions[region][county][area]['where']).split(',')]
            return place_outage, time_outage
