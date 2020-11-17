import spacy

nlp = spacy.load('en_core_web_sm')
myfile = open('sample_string (1).txt')
lines = myfile.readlines()
for line in lines:
    doc = nlp(line)
    for token in doc:
        print(token.lemma_, end=' ')
    for token in doc:
        print(token.pos_, end=' ')