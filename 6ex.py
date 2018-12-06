def manhattan_distance(x1, y1, x2, y2):
    return abs(x2 - x1) + abs(y2 - y1)
assert manhattan_distance(0, 0, 2, 0) == 2
assert manhattan_distance(0, 0, 2, 1) == 3
assert manhattan_distance(0, 0, 0, 0) == 0
assert manhattan_distance(10, 5, 0, 0) == 15

def equidistant(least_to_most):
    return least_to_most[0][1] == least_to_most[1][1]

def closest_to(x, y, coords):
    distances = []
    for coord in coords:
        distances.append((coord, manhattan_distance(x, y, coord[0], coord[1])))
    least_to_most = sorted(distances, key=lambda kv: kv[1])

    if equidistant(least_to_most):
        return None # equidistant
    return least_to_most[0][0] # i want the coord, not the distance

assert closest_to(0, 0, [(0, 1), (2, 3)]) == (0, 1)
assert closest_to(0, 0, [(0, 1), (1, 0)]) == None
assert closest_to(0, 0, [(0, 1), (10, 0), (-10, 0)]) == (0, 1)
assert closest_to(6, 6, [(6, 6), (7, 6)]) == (6,6)

print 'Self-test completed.'

filename = 'input6.txt'

with open(filename) as i:
    lines = i.readlines()

coords = []
for line in lines:
    x, y = line.split(',')
    coords.append( ( int(x), int(y) ) )

def calculate_coord_frequency_for_size(width, coords):
    grid = [ None ] * width * width
    half_width = width / 2
    
    # Pre-Bake the grid
    for y in range(0, width):
        for x in range(0, width):
            half_x = x - half_width
            half_y = y - half_width
            # move the origin point into the negative realm
            grid[ y * width + x ] = closest_to(half_x, half_y, coords)
    print "Grid is baked."

    results = {}
    for coord in coords:
        count = len(filter(lambda x: x == coord, grid))
        results[coord] = count

    return results

# try two different sizes
SIZE_A = 800
SIZE_B = 1000
run_a = calculate_coord_frequency_for_size(SIZE_A, coords)
print "Run A completed, size = %i" % SIZE_A
run_b = calculate_coord_frequency_for_size(SIZE_B, coords)
print "Run B completed, size = %i" % SIZE_B

biggest_area_so_far = 0
best_coord_so_far = None
for coord in coords:
    if run_a[coord] != run_b[coord]:
        print "Probably infinite: %i, %i" % (coord[0], coord[1])
        print "%i vs %i" % (run_a[coord], run_b[coord])
    else:
        print "(%i,%i) size = %i" % (coord[0], coord[1], run_a[coord])
        if run_a[coord] > biggest_area_so_far:
            biggest_area_so_far = run_a[coord]
            best_coord_so_far = coord

print "Biggest area is %i, from coord (%i,%i)" % (biggest_area_so_far, best_coord_so_far[0], best_coord_so_far[1])
