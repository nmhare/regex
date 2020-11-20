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

def char_after(string, substring):
    return string[string.index(substring) + len(substring) : string.index(substring) + len(substring) + 1]

def findinstances(string, elems):
    instances = []
    for elem in elems:
        if (elem.lower() in string.lower()):
            elem_index = string.lower().index(elem.lower())
            elem = string[elem_index:len(elem) + elem_index]
            if char_after(string, elem) == 's':
                elem = elem + 's'
            instances.append(elem.strip())
    print(instances)
    return instances 

myfile = open('sample_string (2).txt', 'r')
lines = myfile.readlines()
outF = open("myOutFile.txt", "w")

nlp = spacy.load('en_core_web_sm')

streetsuffixes = ['Alley', 'Avenue', 'Branch', 'Bridge', 'Brook', 'Burg',
        'Bypass', 'Camp', 'Canyon', 'Cape', 'Causeway', 'Center', 'Circle',
        'Cliff', 'Club', 'Common', 'Corner', 'Course', 'Court',
        'Cove', 'Creek', 'Crescent', 'Crest', 'Crossing', 'Crossroad', 'Curve',
        'Dale', 'Dam', 'Divide', 'Drive', 'Estate','Expressway',
        'Extension', 'Fall', 'Ferry', 'Field', 'Flat',
        'Ford', 'Forest','Forge', 'Fork', 'Fort', 'Freeway',
        'Garden', 'Gateway', 'Glen', 'Glens', 'Green', 'Grove', 'Harbor',
        'Haven', 'Heights', 'Highway',  'Hill', 'Hollow', 'Inlet', 'Islands', 'Island', 'Isles', 
        'Isle',  'Junction', 'Key',  'Knoll',
        'Lake', 'Landing', 'Land', 'Lane', 'Light', 'Loaf', 'Lock', 'Lodge',
         'Loop', 'Mall', 'Manor', 'Meadow', 'Mews', 'Mill', 'Mills', 'Mission',
        'Mission', 'Motorway', 'Mount', 'Mountains', 'Mountain',  'Neck', 'Orchard',
        'Overpass', 'Parkway', 'Park', 'Passage', 'Pass', 'Path', 'Pike', 'Pine',
        'Place', 'Plain', 'Plaza', 'Points', 
        'Port', 'Prairie', 'Radial', 'Ramp', 'Ranch', 'Rapid', 'Rest', 'Ridge',
        'River', 'Road', 'Route', 'Row', 'Rue', 'Run', 'Shoal',
        'Shore', 'Skyway', 'Spring',  'Spurs', 'Square',
        'Station', 'Stravenue',  'Stream', 'Street',
        'Summit', 'Terrace', 'Throughway', 'Trace', 'Track', 'Trafficway',
        'Trail', 'Tunnel', 'Turnpike', 'Turnpike', 'Underpass', 'Union',
        'Valley', 'Via', 'Viaduct', 'View', 'Village', 'Ville',
        'Vista', 'Walk', 'Wall', 'Way',  'Well', 'Ave', 'St', 'Blvd']


endings = ['.,',',', ' ', '.','\n']
newsuffixes = []
for suffix in streetsuffixes:
    for ending in endings:
        newsuffixes.append(' ' + suffix + ending)

region1 = r'\b((?:ky|Ky|KY)|(?:[Kk][Ee][Nn][Tt][Uu][Cc][Kk][Yy]))\b'

for line in lines:
    # credit: u/buckley, 
    # https://stackoverflow.com/questions/34527917/extracting-phone-numbers-from-a-free-form-text-in-python-by-using-regex    
    # credit: u/0x90, 
    # https://stackoverflow.com/questions/17681670/extract-email-sub-strings-from-large-document
    
    newline = line
    print(line)
    phone = re.findall(r'\(?[0-9]{3}\)?[-./]?\s*[0-9]{3}\s*[-./]?\s*[0-9]{4}[.x]?[0-9]{0,}\b', newline)
    for p in phone:
        newline = newline.replace(p, '"phone"')    

    foundsuffixes = findinstances(newline, newsuffixes)
    names = findallnames(newline, nlp)

    for foundsuffix in foundsuffixes:
        for n in names:
            if foundsuffix in n:
                names.remove(n)
        doc = nlp(newline)
        number = ''
        i = 0
        for token in doc:
            if token.pos_ == 'NUM':
                number = token.text
                break
            i = i + 1
        j = 0
        for token in doc:
            if token.text == foundsuffix:
                break
            elif token.text == foundsuffix[-1] and not foundsuffix[-1:].isalnum():
                break
            j = j + 1
        if j - i not in range(0,4):
            foundsuffixes.remove(foundsuffix)

    for suffix in foundsuffixes:
        newaddr = ''
        if foundsuffixes[0] in newline:
            cityname = 'Louisville'
            if cityname in newline:
                cityname = cityname + char_after(newline, cityname)
                if cityname[-1] != ' ':
                    cityname = cityname + ' '
                newline = newline.replace(cityname, '')
            newaddr = newaddr + cityname

            statename = re.findall(region1, newline)
            if statename != []:
                statename[0] = statename[0] + ' '
                newline = newline.replace(statename[0], '')
                newaddr = newaddr + statename[0]
            else:
                newaddr = newaddr + ' KY ' #might need to fix spacing

            zipcode = re.findall(r'\d{5}', newline) #might want to hold off on this
            if zipcode != []:
                newline = newline.replace(zipcode[-1], '')
                newaddr = newaddr + zipcode[-1]

            if suffix[-1:] == ' ':
                newline = newline.replace(suffix, suffix + newaddr + ' ')
            elif suffix[-1:] == '\n':
                newline = newline.replace(suffix, suffix[:-1] + ' ' + newaddr + '\n') 
            else:    
                newline = newline.replace(suffix, suffix + ' ' + newaddr) 
    
            break

    address = pyap.parse(newline, country='US')
    for a in address:
        newline = newline.replace(str(a), '"address"')

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