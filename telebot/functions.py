import codecs
import json
import os
import re
import time
from datetime import datetime
from pathlib import Path
import redis
import bs4
import requests
import textract


# This function checks the kplc website for the latest pdf on planned power interruptions and downloads it.
def parse_content():
    os.makedirs('telebot/content/', exist_ok=True)
    res = requests.get('https://kplc.co.ke/category/view/50/planned-power-interruptions')
    res.raise_for_status()

    soup = bs4.BeautifulSoup(res.text, 'html.parser')

    links = soup.select('.items .intro li a')
    if not links:
        print('No content Found')
    else:
        dates = []
        for link in links:
            file_name = os.path.basename(link.get('href'))
            date_pattern = re.compile(r"""^(.*?)
                ((0|1|2|3)?\d)\.
                ((0|1)?\d)\.
                ((19|20)\d\d)
                (.*?)$
                """, re.VERBOSE)
            mo = date_pattern.search(file_name)
            day_part = mo.group(2)
            month_part = mo.group(4)
            year_part = mo.group(6)
            send = day_part + '.' + month_part + '.' + year_part
            dates.append(send)
        latest_date = max(dates, key=lambda d: datetime.strptime(d, '%d.%m.%Y'))
        pattern_latest_date = re.compile(rf"{latest_date}", re.IGNORECASE)
        for link in links:
            if pattern_latest_date.search(str(os.path.basename(link.get('href')))):
                url = link.get('href')
                break
        res = requests.get(url)
        res.raise_for_status()
        p = Path('telebot/content/')
        print(list(p.glob('*')))
        pdf_name = str(os.path.basename(url))
        if len(list(p.glob('*.pdf'))) > 0:
            os.remove(list(p.glob('*.pdf'))[0])
        with open('telebot/content/' + pdf_name, 'wb') as r:
            r.write(res.content)
        conn = redis.from_url(os.environ.get("REDIS_URL"))
        conn.set('pdf_name', pdf_name)
        return pdf_name


# This function extracts content from the pdf and saves it to a text file
def extract_pdf(pdf_name):
    os.makedirs('telebot/content', exist_ok=True)
    textract_text = textract.process(f'telebot/content/{pdf_name}')
    textract_str_text = codecs.decode(textract_text)
    with open(f'telebot/content/extracted_data.txt', 'w') as f:
        f.write(textract_str_text.strip('\n'))


# This function removes irrelevant data from the text file created above and saves it to another text file
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


# Reads data from the text file created above and forms a nested dictionary of it and stores it in a shelve binary.
def save_data_to_shelve():
    regions = {}
    region_regex = re.compile(r"region", re.IGNORECASE)
    area_regex = re.compile(r"area:", re.IGNORECASE)
    county_regex = re.compile(r"county", re.IGNORECASE)
    remove_regex = re.compile(r"sub-county", re.IGNORECASE)
    previous_line = ''
    with open('telebot/content/cleaned_data.txt', 'r') as r:
        for line in r.readlines():
            if region_regex.search(line):
                region_name = " ".join(line.split()[:-1])
                county_name = ''
                continue
            if county_regex.search(line) and not 'offices' in line.casefold() and not remove_regex.search(line):
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
    conn = redis.from_url(os.environ.get("REDIS_URL"))
    regions_json = json.dumps(regions)
    conn.set('regions', regions_json)


# If a county has power interruptions planned, it returns areas in the specified county that will be affected.
def area_list(county, regions):
    for region in regions.keys():
        if county.strip().upper() in regions[region].keys():
            print(county)
            print(region)
            areas = [area for area in regions[region][county.strip().upper()].keys()]
            print(areas)
            if '' in areas:
                areas.remove('')
            return areas
        else:
            continue
    return None


# returns places in the specific area passed that will be affected by the power interruption.
def place_list(county, area, regions):
    county = county.strip().upper()
    for region in regions.keys():
        if county in regions[region].keys():
            time_outage = regions[region][county][area]['when'].upper()
            time_outage = re.sub('(\s\s\s)+', '', time_outage)
            time_outage = '\n⏱️TIME'.join(time_outage.split('TIME'))
            place_outage = [place.strip().capitalize() for place in
                            ''.join(regions[region][county][area]['where']).split(',')]
            return place_outage, time_outage

