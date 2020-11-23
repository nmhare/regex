import re
import spacy
import pandas as pd
import pyap
import string


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
    curr = string
    instances = []
    for elem in elems:
        while (elem.lower() in curr.lower()):
            elem_index = curr.lower().index(elem.lower())
            elem = curr[elem_index:len(elem) + elem_index]
            if char_after(curr, elem) == 's':
                elem = elem + 's'
            instances.append((elem.strip(), elem_index))
            curr = curr[:elem_index] + curr[:len(elem) + elem_index]
            print(curr)
    print(instances)
    return instances
    
myfile = open('sample_string (1).txt', 'r')
lines = myfile.readlines()
outF = open("myOutFile.txt", "w")

nlp = spacy.load('en_core_web_sm')

streets = pd.read_csv("street.csv")
suffixes = pd.read_csv("street_suf.csv")
streetsuffixes = set(pd.concat([suffixes['Primary'],suffixes['Commonly'],suffixes['Postal Service']], ignore_index=True))
streetnames = set(streets.street_name)
zipcodes = set(str(streets.zip))
cities = set(['Louisville'])
states = set(['KY'])

attributes = [streetnames, streetsuffixes, zipcodes, cities, states]

for line in lines:
    newline = line.translate(str.maketrans('', '', string.punctuation))
    
    phone = re.findall(r'\(?[0-9]{3}\)?[-./]?\s*[0-9]{3}\s*[-./]?\s*[0-9]{4}[.x]?[0-9]{0,}\b', newline)
    for p in phone:
        newline = newline.replace(p, '"phone"')   
    
    email = re.findall(r'[\w.\-\+%]+@[\w\.\+]+\.\w+', newline)
    for e in email:
        newline = newline.replace(e, '"email"')

    names = findallnames(newline, nlp)
    for n in names:
        newline = newline.replace(n, '"name"')

    doc = nlp(newline.strip())
    word = '"address"'
    for token in doc:
        for attribute in attributes:
            if token.text.lower() in map(str.lower, attribute):
                print(token.text.lower(), 'was inside attribute ', attribute )
                newline = newline.replace(token.text, word)
    
    instances = findinstances(newline, [word])
    print(instances)
    max_ = max(instances, key=lambda x:x[1])
    print('max is ', max_)
    min_ = min(instances, key=lambda x:x[1])
    print('min is ', min_, 'newline is', newline)
    substring = newline[min_:(max_ + len(word))]
    substring = substring.replace(word, '')
    substring = substring.replace('"name"', '')
    newline = newline[:min_] + substring + newline[max_ + len(word):]
    outF.write(newline)
outF.close()