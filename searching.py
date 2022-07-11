import shelve

shelve_file = shelve.open('data_file')
regions = shelve_file['regions']

county_input = input("welcome, Check whether power outage is in your area:\n Enter your county name to see planned "
                     "outages.").upper()

for region in regions.keys():
    if county_input in regions[region].keys():
        print('The following areas will experience Power outages')
        for area in regions[region][county_input].keys():
            print(area, end=' |*|')
        area_input = input('Enter the area from the above to see the exact place that will be affected').lower()
        print(regions[region][county_input][area_input]['when'].upper())
        for place in ''.join(regions[region][county_input][area_input]['where']).split(','):
            print(place.strip())
