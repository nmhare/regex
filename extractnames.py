import re
import spacy
import pandas as pd

# Credit: Aboyami Adewole, 
# https://www.ayobamiadewole.com/Blog/named-entity-extraction-from-text-in-python
# known bug - the apostrophe after names is saved as part of the name,
# e.g. Jane Doe's is saved as "Jane Doe 'S", as if a 3rd name
def extract(text: str, spacy_nlp):
    doc = spacy_nlp(text.strip())
    named_entities = []
    for i in doc.ents:
        entry = str(i.lemma_).lower()
        if i.label_ in ["PERSON"]:
            named_entities.append(entry.title())
    return named_entities


myfile = open('sample_string.txt', 'r')
spacy_nlp = spacy.load('en_core_web_sm')
groupings = []
lines = myfile.readlines()
for line in lines:
    # credit: u/buckley, 
    # https://stackoverflow.com/questions/34527917/extracting-phone-numbers-from-a-free-form-text-in-python-by-using-regex
    phone = re.findall(r'\(?\b[2-9][0-9]{2}\)?[-. ]?\s*[2-9][0-9]{2}\s*[-. ]?\s*[0-9]{4}\b', line)
    
    # credit: u/0x90, 
    # https://stackoverflow.com/questions/17681670/extract-email-sub-strings-from-large-document
    email = re.findall(r'[\w\.-]+@[\w\.-]+\.\w+', line)
    groupings.append([" ".join(extract(line, spacy_nlp)), " ".join(email), " ".join(phone)])

df = pd.DataFrame(groupings)
df.columns = ['Name', 'Email','Phone Number']
df.to_csv("ContactInfo.csv")