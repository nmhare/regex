import re
import spacy
import pandas as pd

def findallnames(text: str, nlp):
    named_entities = []
    doc = nlp(text.strip())
    for i in doc.ents:
         if i.label_ == 'PERSON':                
                named_entities.append(str(i))
    return named_entities

myfile = open('sample_string.txt', 'r')
outF = open("myOutFile.txt", "w")
nlp = spacy.load('en_core_web_sm')
lines = myfile.readlines()


for line in lines:
    # credit: u/buckley, 
    # https://stackoverflow.com/questions/34527917/extracting-phone-numbers-from-a-free-form-text-in-python-by-using-regex    
    # credit: u/0x90, 
    # https://stackoverflow.com/questions/17681670/extract-email-sub-strings-from-large-document
    
    phone = re.findall(r'\(?\b[0-9]{3}\)?[-./ ]?\s*[0-9]{3}\s*[-./ ]?\s*[0-9]{4}\b', line)
    email = re.findall(r'[\w.\-\+%]+@[\w\.\+]+\.\w+', line)
    names = findallnames(line, nlp)
    newline = line

    for e in email:
        newline = newline.replace(e, '"email"')
    for p in phone:
        newline = newline.replace(p, '"phone"')
    for n in names:
        newline = newline.replace(n, '"name"')
    outF.write(newline)

outF.close()