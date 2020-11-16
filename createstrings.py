from faker import Faker
import numpy as np
import random

def randomly(seq):
    shuffled = list(seq)
    random.shuffle(shuffled)
    return iter(shuffled)

fake = Faker()
outF = open("generateRandomProfiles.txt", "w")
fields_ = ['name','residence','mail','phone_number']

for a in range(50):
    newline = ''
    attributes = fake.profile(fields_)
    attributes['phone_number'] = fake.phone_number()
    attributes['residence'] = attributes['residence'].replace('\n', ' ')

    for n in randomly(fields_):
        for m in range(random.randint(1,3)):
            newline += fake.word() + ' '
        newline += attributes[n] + ' '
    newline += '.\n'
    outF.write(newline)
outF.close()
    
