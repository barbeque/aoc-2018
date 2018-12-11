serial_number = 1309

# array is 300x300, 1 to 300 inclusive
cells = [ 0 ] * 300 * 300
assert len(cells) == 300 * 300

def hunnets(num):
    s = str(num)
    if len(s) < 3:
        return 0
    else:
        return int(s[::-1][2])

assert hunnets(12345) == 3
assert hunnets(1234567) == 5

for x in range(1, 301):
    for y in range(1, 301):
        rack_id = x + 10
        power_level = rack_id * y
        power_level += serial_number
        power_level *= rack_id
        power_level = hunnets(power_level)

        # array is 0-indexed of course
        idx = (y - 1) * 300 + (x - 1)
        assert idx < len(cells), "Something went wrong at (%i,%i)" % (x, y)
        cells[idx] = power_level

def sum_power(cells, x, y):
    s = 0
    for dx in range(0, 3):
        if x + dx >= 300:
            continue

        for dy in range(0, 3):
            if y + dy >= 300:
                continue

            s += cells[(y + dy) * 300 + (x + dx)]
    return s

# now that the cells exist let's search
best_coord = None
best_power = 0
for x in range(1, 301):
    for y in range(1, 301):
        total_power = sum_power(cells, x - 1, y - 1)
        if total_power > best_power:
            best_power = total_power
            best_coord = (x, y)

print "Best power %i at %i, %i" % (total_power, best_coord[0], best_coord[1])
