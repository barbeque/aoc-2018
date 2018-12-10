import re

with open('input10.txt') as i:
    lines = i.readlines()

# position=< 30238,  20137> velocity=<-3, -2>
nodes = []
for line in lines:
    match = re.match(r'position\=\<\s*(-*\d+)\,\s*(-*\d+)\>\s*velocity\=\<\s*(-*\d+)\,\s*(-*\d+)\>', line)
    assert match, 'Should have matched for line %s' % line

    x = int(match.group(1))
    y = int(match.group(2))
    vx = int(match.group(3))
    vy = int(match.group(4))

    print 'position = %i, %i => velocity = %i, %i' % (x, y, vx, vy)
