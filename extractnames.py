import re
import spacy
import pandas as pd
import pyap

def findallnames(text: str, nlp):
    named_entities = []
    doc = nlp(text.strip())
    for i in doc.ents:
        if i.label_ in ['PERSON', 'ORG']:
            named_entities.append(str(i))
    return named_entities

myfile = open('sample_string (1).txt', 'r')
outF = open("myOutFile.txt", "w")

nlp = spacy.load('en_core_web_sm')




streetsuffixes = ['Alley', 'Avenue', 'Ave', 'ave', 'Branch', 'Bridge', 'Brook', 'Brooks', 'Burg',
        'Burgs', 'Bypass', 'Camp', 'Canyon', 'Cape', 'Causeway', 'Center', 'Centers', 'Circle',
        'Circles', 'Cliff', 'Cliffs', 'Club', 'Common', 'Corner', 'Corners', 'Course', 'Court',
        'Courts', 'Cove', 'Coves', 'Creek', 'Crescent', 'Crest', 'Crossing', 'Crossroad', 'Curve',
        'Dale', 'Dam', 'Divide', 'Drive', 'Drive', 'Drives', 'Estate', 'Estates', 'Expressway',
        'Extension', 'Extensions', 'Fall', 'Falls', 'Ferry', 'Field', 'Fields', 'Flat', 'Flats',
        'Ford', 'Fords', 'Forest', 'Forge', 'Forges', 'Fork', 'Forks', 'Fort', 'Freeway', 'Garden',
        'Gardens', 'Gateway', 'Glen', 'Glens', 'Green',  'Greens', 'Grove', 'Groves', 'Harbor', 'Harbors',
        'Haven', 'Heights', 'Highway', 'Hill', 'Hills', 'Hollow', 'Inlet', 'Inlet', 'Island', 'Island',
        'Islands', 'Islands', 'Isle', 'Isle', 'Junction', 'Junctions', 'Key', 'Keys', 'Knoll', 'Knolls',
        'Lake', 'Lakes', 'Land', 'Landing', 'Lane', 'Light', 'Loaf', 'Lock', 'Locks', 'Locks', 'Lodge',
        'Lodge', 'Loop', 'Mall', 'Manor', 'Manors', 'Meadow', 'Meadows', 'Mews', 'Mill', 'Mills', 'Mission',
        'Mission', 'Motorway', 'Mount', 'Mountain', 'Mountain', 'Mountains', 'Mountains', 'Neck', 'Orchard',
        'Overpass', 'Park', 'Parks', 'Parkway', 'Parkways', 'Pass', 'Passage', 'Path', 'Pike', 'Pine',
        'Pines', 'Place', 'Plain', 'Plains', 'Plains', 'Plaza', 'Plaza', 'Point', 'Points', 'Port', 'Port',
        'Ports', 'Ports', 'Prairie', 'Prairie', 'Radial', 'Ramp', 'Ranch', 'Rapid', 'Rapids', 'Rest', 'Ridge',
        'Ridges', 'River', 'Road', 'Road', 'Roads', 'Roads', 'Route', 'Row', 'Rue', 'Run', 'Shoal', 'Shoals',
        'Shore', 'Shores', 'Skyway', 'Spring', 'Springs', 'Springs', 'Spur', 'Spurs', 'Square', 'Square',
        'Squares', 'Squares', 'Station', 'Station', 'Stravenue', 'Stravenue', 'Stream', 'Stream', 'Street',
        'Street', 'Streets', 'St', 'st', 'Summit', 'Summit', 'Terrace', 'Throughway', 'Trace', 'Track', 'Trafficway',
        'Trail', 'Trail', 'Tunnel', 'Tunnel', 'Turnpike', 'Turnpike', 'Underpass', 'Union', 'Unions',
        'Valley', 'Valleys', 'Via', 'Viaduct', 'View', 'Village', 'Village', 'Villages', 'Ville',
        'Vista', 'Vista', 'Walk', 'Walks', 'Wall', 'Way', 'Ways', 'Well', 'Wells']


region1 = r'\b((?:ky|Ky|KY)|(?:[Kk][Ee][Nn][Tt][Uu][Cc][Kk][Yy]))\b'


lines = myfile.readlines()
for line in lines:
    # credit: u/buckley, 
    # https://stackoverflow.com/questions/34527917/extracting-phone-numbers-from-a-free-form-text-in-python-by-using-regex    
    # credit: u/0x90, 
    # https://stackoverflow.com/questions/17681670/extract-email-sub-strings-from-large-document
    
    newline = line
    
    phone = re.findall(r'\(?[0-9]{3}\)?[-./]?\s*[0-9]{3}\s*[-./]?\s*[0-9]{4}[.x]?[0-9]{0,}\b', newline)
    for p in phone:
        newline = newline.replace(p, '"phone"')
    

    endings = [',', ' ', '.','\n']
    newsuffixes = []
    for suffix in streetsuffixes:
        for ending in endings:
            newsuffixes.append(' ' + suffix + ending)

    for suffix in newsuffixes:
        newaddr = ''
        if suffix in newline:
            cityname = 'Louisville'
            if cityname in newline:
                char = newline[newline.index(cityname) + 10 : newline.index(cityname) + 11]
                if char != ' ':
                    char = char + ' '
                cityname = cityname + char
                newline = newline.replace(cityname, '')
            newaddr = newaddr + cityname

            statename = re.findall(region1, newline)
            if statename != []:
                statename[0] = statename[0] + ' '
                newline = newline.replace(statename[0], '')
                newaddr = newaddr + statename[0]
            else:
                newaddr = newaddr + ' KY'

            zipcode = re.findall(r'\d{5}', newline)
            if zipcode != []:
                newline = newline.replace(zipcode[-1], '')
                newaddr = newaddr + zipcode[0]

            if suffix[-1:] == ' ':
                newline = newline.replace(suffix, suffix + newaddr + ' ')
            elif suffix[-1:] == '\n':
                print('HELLO')
                newline = newline.replace(suffix, suffix[:-1] + ' ' + newaddr + '\n') 
            else:    
                newline = newline.replace(suffix, suffix + ' ' + newaddr) 
    
            print('at the end, we had constructed newline', newline)
            break

    address = pyap.parse(newline, country='US')
    print('pyap found', address)
    for a in address:
        newline = newline.replace(str(a), '"address"')

    names = findallnames(newline, nlp)
    for n in names:
        newline = newline.replace(n, '"name"')

    email = re.findall(r'[\w.\-\+%]+@[\w\.\+]+\.\w+', newline)
    for e in email:
        newline = newline.replace(e, '"email"')
    
    #codes = re.findall(r'\b\d{5,}\b', line)
    #for c in codes: 
        #newline = newline.replace(c, '"numeric code"')

    outF.write(newline)

outF.close()