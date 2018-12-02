def dropchar(word, index):
    out = ''
    for i in range(0, len(word)):
        if i == index:
            continue
        out += word[i]
    return out

assert dropchar('hello', 1) == 'hllo'

with open('input2.txt') as i:
    lines = i.readlines()

i = 0
j = 0

for i in range(0, len(lines) - 1):
    a = lines[i]
    for j in range(i + 1, len(lines)):
        b = lines[j]
        # if the words differ by only one character, find the index

        diffs = 0
        last_diff = -1
        for k in range(0, len(lines[i])):
            if lines[i][k] != lines[j][k]:
                diffs += 1
                last_diff = k

        if diffs == 1:
            print "Two diffs are %i, %i at index %i" % (i, j, last_diff)
            print "Without that differing char, it should be %s" % dropchar(lines[i], last_diff)
