myfile = open("myOutFile.txt", 'r')
lines = myfile.readlines()

attributes = ['"name"','"address"','"phone"', '"email"']
tally = [0,0,0,0,0,0]
for line in lines:
    i = 0
    for attribute in attributes:
        if attribute in line:
            tally[i] += 1
        else:
            print('Line ', tally[5] + 1, ' was missing attribute: ', attributes[i])
        i += 1
    tally[5] += 1

i = 0
for attribute in attributes:
    print (attribute + " percent found: ", tally[i] / tally[5])
    i += 1