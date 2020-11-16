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

myfile = open('sample_string (2).txt', 'r')
outF = open("myOutFile.txt", "w")

nlp = spacy.load('en_core_web_sm')

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
    
    attributes = ['zipcode','statename','statecode','louisville', 'street names']
    streetsuffixes = ['Alley', 'Avenue', 'Ave', 'Ave.', 'ave.', 'ave', 'Branch', 'Bridge', 'Brook', 'Brooks', 'Burg',
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
        'Street', 'Streets', 'St', 'St.', 'st', 'st.', 'Summit', 'Summit', 'Terrace', 'Throughway', 'Trace', 'Track', 'Trafficway',
        'Trail', 'Trail', 'Tunnel', 'Tunnel', 'Turnpike', 'Turnpike', 'Underpass', 'Union', 'Unions',
        'Valley', 'Valleys', 'Via', 'Viaduct', 'View', 'Village', 'Village', 'Villages', 'Ville',
        'Vista', 'Vista', 'Walk', 'Walks', 'Wall', 'Way', 'Ways', 'Well', 'Wells']

    region1 = r"""
        (?P<region1>
            (?:
                # states abbreviations
                AL|AK|AZ|AR|CA|CO|CT|DE|DC|FL|GA|HI|ID|IL|IN|IA|KS|KY|LA|ME|MD|MA|MI|
                MN|MS|MO|MT|NE|NV|NH|NJ|NM|NY|NC|ND|OH|OK|OR|PA|RI|SC|SD|TN|TX|UT|VT|
                VA|WA|WV|WI|WY|
                Ky|ky|
            
                # unincorporated & commonwealth territories
                AS|GU|MP|PR|VI
            )
            |
            (?:
                # states full
                [Aa][Ll][Aa][Bb][Aa][Mm][Aa]|
                [Aa][Ll][Aa][Ss][Kk][Aa]|
                [Aa][Rr][Ii][Zz][Oo][Nn][Aa]|
                [Aa][Rr][Kk][Aa][Nn][Ss][Aa][Ss]|
                [Cc][Aa][Ll][Ii][Ff][Oo][Rr][Nn][Ii][Aa]|
                [Cc][Oo][Ll][Oo][Rr][Aa][Dd][Oo]|
                [Cc][Oo][Nn][Nn][Ee][Cc][Tt][Ii][Cc][Uu][Tt]|
                [Dd][Ee][Ll][Aa][Ww][Aa][Rr][Ee]|
                [Dd][Ii][Ss][Tt][Rr][Ii][Cc][Tt]\ [Oo][Ff]\ 
                [Cc][Oo][Ll][Uu][Mm][Bb][Ii][Aa]|
                [Ff][Ll][Oo][Rr][Ii][Dd][Aa]|
                [Gg][Ee][Oo][Rr][Gg][Ii][Aa]|
                [Hh][Aa][Ww][Aa][Ii][Ii]|
                [Ii][Dd][Aa][Hh][Oo]|
                [Ii][Ll][Ll][Ii][Nn][Oo][Ii][Ss]|
                [Ii][Nn][Dd][Ii][Aa][Nn][Aa]|
                [Ii][Oo][Ww][Aa]|
                [Kk][Aa][Nn][Ss][Aa][Ss]|
                [Kk][Ee][Nn][Tt][Uu][Cc][Kk][Yy]|
                [Ll][Oo][Uu][Ii][Ss][Ii][Aa][Nn][Aa]|
                [Mm][Aa][Ii][Nn][Ee]|
                [Mm][Aa][Rr][Yy][Ll][Aa][Nn][Dd]|
                [Mm][Aa][Ss][Ss][Aa][Cc][Hh][Uu][Ss][Ee][Tt][Tt][Ss]|
                [Mm][Ii][Cc][Hh][Ii][Gg][Aa][Nn]|
                [Mm][Ii][Nn][Nn][Ee][Ss][Oo][Tt][Aa]|
                [Mm][Ii][Ss][Ss][Ii][Ss][Ss][Ii][Pp][Pp][Ii]|
                [Mm][Ii][Ss][Ss][Oo][Uu][Rr][Ii]|
                [Mm][Oo][Nn][Tt][Aa][Nn][Aa]|
                [Nn][Ee][Bb][Rr][Aa][Ss][Kk][Aa]|
                [Nn][Ee][Vv][Aa][Dd][Aa]|
                [Nn][Ee][Ww]\ [Hh][Aa][Mm][Pp][Ss][Hh][Ii][Rr][Ee]|
                [Nn][Ee][Ww]\ [Jj][Ee][Rr][Ss][Ee][Yy]|
                [Nn][Ee][Ww]\ [Mm][Ee][Xx][Ii][Cc][Oo]|
                [Nn][Ee][Ww]\ [Yy][Oo][Rr][Kk]|
                [Nn][Oo][Rr][Tt][Hh]\ [Cc][Aa][Rr][Oo][Ll][Ii][Nn][Aa]|
                [Nn][Oo][Rr][Tt][Hh]\ [Dd][Aa][Kk][Oo][Tt][Aa]|
                [Oo][Hh][Ii][Oo]|
                [Oo][Kk][Ll][Aa][Hh][Oo][Mm][Aa]|
                [Oo][Rr][Ee][Gg][Oo][Nn]|
                [Pp][Ee][Nn][Nn][Ss][Yy][Ll][Vv][Aa][Nn][Ii][Aa]|
                [Rr][Hh][Oo][Dd][Ee]\ [Ii][Ss][Ll][Aa][Nn][Dd]|
                [Ss][Oo][Uu][Tt][Hh]\ [Cc][Aa][Rr][Oo][Ll][Ii][Nn][Aa]|
                [Ss][Oo][Uu][Tt][Hh]\ [Dd][Aa][Kk][Oo][Tt][Aa]|
                [Tt][Ee][Nn][Nn][Ee][Ss][Ss][Ee][Ee]|
                [Tt][Ee][Xx][Aa][Ss]|
                [Uu][Tt][Aa][Hh]|
                [Vv][Ee][Rr][Mm][Oo][Nn][Tt]|
                [Vv][Ii][Rr][Gg][Ii][Nn][Ii][Aa]|
                [Ww][Aa][Ss][Hh][Ii][Nn][Gg][Tt][Oo][Nn]|
                [Ww][Ee][Ss][Tt]\ [Vv][Ii][Rr][Gg][Ii][Nn][Ii][Aa]|
                [Ww][Ii][Ss][Cc][Oo][Nn][Ss][Ii][Nn]|
                [Ww][Yy][Oo][Mm][Ii][Nn][Gg]|
                # unincorporated & commonwealth territories
                [Aa][Mm][Ee][Rr][Ii][Cc][Aa][Nn]\ [Ss][Aa][Mm][Oo][Aa]
                |[Gg][Uu][Aa][Mm]|
                [Nn][Oo][Rr][Tt][Hh][Ee][Rr][Nn]\ [Mm][Aa][Rr][Ii][Aa][Nn][Aa]\ 
                [Ii][Ss][Ll][Aa][Nn][Dd][Ss]|
                [Pp][Uu][Ee][Rr][Tt][Oo]\ [Rr][Ii][Cc][Oo]|
                [Vv][Ii][Rr][Gg][Ii][Nn]\ [Ii][Ss][Ll][Aa][Nn][Dd][Ss]
            )
        )
        """
    
    newaddr = ''
    streetmarker = ''
    for streettype in streetsuffixes:
        streetmarker = ''
        newaddr = ''
        if ' ' + streettype in newline:
            streetmarker = streettype
            print('-------------')

            cityname = 'Louisville'
            if cityname in newline:
                print(newline)
                newline = newline.replace(cityname, '')
                print(newline)
            print('newaddr is ', newaddr, ', cityname is ', cityname)
            newaddr = newaddr + cityname
            print('newaddr is ', newaddr)

            statename = re.findall(region1, newline)
            print(statename)
            if statename != []:
                newline = newline.replace(statename, '')
                newaddr = newaddr + statename
            else:
                newaddr = newaddr + ' KY'
                print('newaddr is ', newaddr)

            zipcode = re.findall(r'^[0-9]{5}(-[0-9]{4})?$', newline)
            print(zipcode)
            if zipcode != []:
                newline = newline.replace(zipcode, '')
                newaddr = newaddr + zipcode

            newline = newline.replace(streetmarker, streetmarker + ', ' +  newaddr)
            print('newline is', newline, ', streetmarker is ', streetmarker)
            break

    address = pyap.parse(newline, country='US')
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