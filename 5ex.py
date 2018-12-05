with open('input5.txt') as i:
    polymers = i.read()

# scan through the file and find the next match

def dropchr(string, idx):
    return string[:idx] + string[(idx + 1):]

def length_after_react(string):
    i = 0
    drops = 0
    while True:
        if abs(ord(string[i + 1]) - ord(string[i])) == 32:
            # match
            string = dropchr(string, i)
            string = dropchr(string, i) # i + 1 shifted left
            i = 0 # start over (slow but sure)
            drops += 1
            if drops % 1000 == 0:
                print "Reached %i drops, left = %i chars" % (drops, len(string))
        else:
            i += 1
        if i + 1 >= len(string):
            # we're done
            return len(string)

assert length_after_react('dabAcCaCBAcCcaDA') == 10
print "Done tests"

input_length = length_after_react(polymers)
print "Length is %i" % input_length
