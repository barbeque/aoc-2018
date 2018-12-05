with open('input5.txt') as i:
    polymers = i.read()[:-1]
    assert len(polymers) == 50000

# scan through the file and find the next match

def dropchr(string, idx):
    return string[:idx] + string[(idx + 1):]

def kill_all_of_type(c, string):
    i = 0
    while True:
        if string[i] == c or chr(ord(string[i]) + 32) == c:
            string = dropchr(string, i)
            i = max(0, i - 1) # eliminated this pair
        else:
            i += 1
        if i >= len(string):
            return string # done matching off

def length_after_react(string):
    i = 0
    drops = 0
    while True:
        if abs(ord(string[i + 1]) - ord(string[i])) == 32:
            # match
            string = dropchr(string, i)
            string = dropchr(string, i) # i + 1 shifted left
            i = max(0, i - 1) # start over (slow but sure)
            drops += 1
            if drops % 1000 == 0:
                print "Reached %i drops, left = %i chars" % (drops, len(string))
        else:
            i += 1
        if i + 1 >= len(string):
            # we're done
            return len(string)

assert dropchr('taco', 1) == 'tco'
assert length_after_react('dabAcCaCBAcCcaDA') == 10
assert kill_all_of_type('a', 'bBaAbB') == 'bBbB'
print "Done tests"

smallest_length = 1000000
best_letter = ''

i = 0

for letter in 'abcdefghijklmnopqrstuvwxyz': # all kinds of letters
    input_length = len(polymers)
    without_this_letter = kill_all_of_type(letter, polymers)
    assert len(polymers) == input_length, "Length changed, sweet cheeks"

    this_truncated_length = length_after_react(without_this_letter)
    if this_truncated_length < smallest_length:
        smallest_length = this_truncated_length
        best_letter = '' + letter

    i += 1
    if i % 5 == 0:
        print "letter now " + letter

print "Best letter was %s with length of %i" % (best_letter, smallest_length)
