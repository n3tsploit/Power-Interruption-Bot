import shelve

shelve_file = shelve.open('../data_file')
regions = shelve_file['regions']


def area_list(county):
    for region in regions.keys():
        if county.strip().upper() in regions[region].keys():
            areas = [area for area in regions[region][county.strip().upper()].keys()]
            return areas
        else:
            return None


def place_list(county, area):
    county=county.strip().upper()
    for region in regions.keys():
        if county in regions[region].keys():
            time_outage = regions[region][county][area]['when'].upper()
            place_outage = [place.strip() for place in ''.join(regions[region][county][area]['where']).split(',')]
            return place_outage
