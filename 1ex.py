frequency = 0

with open('input1.txt') as i:
    lines = i.readlines()

for line in lines:
    frequency += int(line)

print "Freq = %i" % frequency
