def include_in_checksum(word):
    # if has a letter that appears exactly twice,
    # and a letter that appears exactly three times,
    has_two_count = False
    has_three_count = False

    for letter in word:
        if word.count(letter) == 2:
            has_two_count = True
        if word.count(letter) == 3:
            has_three_count = True
    
    if has_two_count and has_three_count:
        return 'both'

    if has_two_count:
        return '2'

    if has_three_count:
        return '3'

    return ''

assert include_in_checksum('abcdef') == ''
assert include_in_checksum('bababc') == 'both', "got %s" % include_in_checksum('bababc')
assert include_in_checksum('abbcde') == '2'
assert include_in_checksum('abcccd') == '3'
assert include_in_checksum('aabcdd') == '2'
assert include_in_checksum('abcdee') == '2'
assert include_in_checksum('ababab') == '3'

with open('input2.txt') as i:
    lines = i.readlines()

two_count = 0
three_count = 0

for line in lines:
    result = include_in_checksum(line)
    if result == '2':
        two_count += 1
    elif result == '3':
        three_count += 1
    elif result == 'both':
        two_count += 1
        three_count += 1

print "Checksum is %i * %i = %i" % (two_count, three_count, two_count * three_count)
