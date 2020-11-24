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
    print('findinstances is workingwith string', string)
    instances = []
    for elem in elems:
        i = 0
        curr = string
        while (elem.lower() in curr.lower()):
            print('elem is ', elem, 'string is ', curr)
            elem_index = curr.lower().index(elem.lower())
            elem = curr[elem_index:len(elem) + elem_index]
            if char_after(curr, elem) == 's':
                elem = elem + 's'
            instances.append((elem.strip(), elem_index + len(elem) * i))
            i = i + 1
            curr = curr[:elem_index] + curr[len(elem) + elem_index:]
    print('at the end of findinstances we have', instances)
    return instances
    
myfile = open('sample_string (1).txt', 'r')
lines = myfile.readlines()
outF = open("myOutFile.txt", "w")

nlp = spacy.load('en_core_web_sm')

streets = pd.read_csv("street.csv")
suffixes = pd.read_csv("street_suf.csv")
streetprefixes = set(['n','s','e','w','nw','ne','sw','se'])
streetnames = set(streets.street_name)
streetsuffixes = set(pd.concat([suffixes['Primary'],suffixes['Commonly'],suffixes['Postal Service']], ignore_index=True))

streets['zipString'] = streets.zip.apply(str)
zipcodes = set(streets['zipString'])
cities = set(['Louisville', 'Chicago'])
states = set(['KY', 'IL'])
attributes = [streetnames, streetsuffixes, zipcodes, cities, states]

for line in lines:
    newline = line
    phone = re.findall(r'\(?[0-9]{3}\)?[-./]?\s*[0-9]{3}\s*[-./]?\s*[0-9]{4}[.x]?[0-9]{0,}\b', newline)
    for p in phone:
        newline = newline.replace(p, '"phone"')   
    
    email = re.findall(r'[\w.\-\+%]+@[\w\.\+]+\.\w+', newline)
    for e in email:
        newline = newline.replace(e, '"email"')

    #newline = newline.translate(str.maketrans('', '', string.punctuation))
    names = findallnames(newline, nlp)
    for n in names:
        newline = newline.replace(n, '"name"')


    doc = nlp(newline.strip())
    word = '"address"'
    for token in doc:
        for attribute in attributes:
            print(token.lemma_.lower())
            if token.lemma_.lower() in set(map(str.lower, attribute)) and token.tag_ == 'NNP':
                newline = newline.replace(token.text, word)
                print('token.text.lower(), ', token.text.lower(), token.tag_, token.dep_, ',', newline)
    
    codes = re.findall(r'\b\d{4,}\b', line)
    for c in codes: 
        newline = newline.replace(c, '"numeric"')

    print('newline is', newline)
    instances = findinstances(newline, [word, '"numeric"'])
    print(instances)
    print('newline is', newline)
    if instances != [] and ('"address"' in instances[0] or '"numeric"' in instances[0]) :
        max_ = max(instances, key=lambda x:x[1])
        min_ = min(instances, key=lambda x:x[1])
        newline = newline[:min_[1]] + '"address"' + newline[max_[1] + len(max_[0]):]
    outF.write(newline)
outF.close()