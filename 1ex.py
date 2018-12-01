frequency = 0
import sys

seen_freqs = {}

with open('input1.txt') as i:
    lines = i.readlines()

while True:
    for line in lines:
        frequency += int(line)
        if frequency in seen_freqs:
            print "Seen %i before" % frequency
            sys.exit(0)
        seen_freqs[frequency] = True

print "Freq = %i" % frequency
