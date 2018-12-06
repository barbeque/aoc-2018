def manhattan_distance(x1, y1, x2, y2):
    return abs(x2 - x1) + abs(y2 - y1)
assert manhattan_distance(0, 0, 2, 0) == 2
assert manhattan_distance(0, 0, 2, 1) == 3
assert manhattan_distance(0, 0, 0, 0) == 0
assert manhattan_distance(10, 5, 0, 0) == 15

def closest_to(x, y, coords):
    distances = []
    for coord in coords:
        distances.append((coord, manhattan_distance(x, y, coord[0], coord[1])))
    least_to_most = sorted(distances, key=lambda kv: kv[1])

    if least_to_most[0][1] == least_to_most[1][1]:
        return None # equidistant
    return least_to_most[0][0] # i want the coord, not the distance

assert closest_to(0, 0, [(0, 1), (2, 3)]) == (0, 1)
assert closest_to(0, 0, [(0, 1), (1, 0)]) == None
assert closest_to(0, 0, [(0, 1), (10, 0), (-10, 0)]) == (0, 1)

with open('input6.txt') as i:
    lines = i.readlines()

coords = []
for line in lines:
    x, y = line.split(',')
    coords.append( ( int(x), int(y) ) )
