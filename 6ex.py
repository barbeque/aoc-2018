def manhattan_distance(x1, y1, x2, y2):
    return abs(x2 - x1) + abs(y2 - y1)
assert manhattan_distance(0, 0, 2, 0) == 2
assert manhattan_distance(0, 0, 2, 1) == 3
assert manhattan_distance(0, 0, 0, 0) == 0
assert manhattan_distance(10, 5, 0, 0) == 15

with open('input6.txt') as i:
    lines = i.readlines()

coords = []
for line in lines:
    x, y = line.split(',')
    coords.append( ( int(x), int(y) ) )
