import re
import spacy
import pandas as pd
import pyap

def findallnames(text: str, nlp):
    named_entities = []
    doc = nlp(text.strip())
    for i in doc.ents:
        if i.label_ in ['PERSON', 'ORG']:
            print('appending', i)
            named_entities.append(str(i))
        else:
            print('not appending', i, 'it was ', i.label_)
    return named_entities

myfile = open('generateRandomProfiles.txt', 'r')
outF = open("myOutFile.txt", "w")

nlp = spacy.load('en_core_web_sm')

lines = myfile.readlines()
for line in lines:
    # credit: u/buckley, 
    # https://stackoverflow.com/questions/34527917/extracting-phone-numbers-from-a-free-form-text-in-python-by-using-regex    
    # credit: u/0x90, 
    # https://stackoverflow.com/questions/17681670/extract-email-sub-strings-from-large-document
    
    print('____________________')
    newline = line
    
    phone = re.findall(r'\(?[0-9]{3}\)?[-./]?\s*[0-9]{3}\s*[-./]?\s*[0-9]{4}[.x]?[0-9]{0,}\b', newline)
    for p in phone:
        print(p)
        newline = newline.replace(p, '"phone"')
    
    address = pyap.parse(newline, country='US')
    for a in address:
        print(str(a))
        newline = newline.replace(str(a), '"address"')
    
    names = findallnames(newline, nlp)
    for n in names:
        print(n)
        newline = newline.replace(n, '"name"')

    email = re.findall(r'[\w.\-\+%]+@[\w\.\+]+\.\w+', newline)
    for e in email:
        print(e)
        newline = newline.replace(e, '"email"')
    
    #codes = re.findall(r'\b\d{5,}\b', line)
    #for c in codes: 
        #newline = newline.replace(c, '"numeric code"')

    outF.write(newline)

outF.close()