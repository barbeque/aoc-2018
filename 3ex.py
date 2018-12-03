with open('input3.txt') as i:
    lines = i.readlines()

def coords(line):
    at_loc = line.index('@')
    x_str = ''
    y_str = ''
    building_y = False
    for i in range(at_loc + 1, len(line)):
        if line[i] == ',':
            building_y = True
        elif line[i] == ':':
            return int(x_str), int(y_str)
        else:
            if building_y:
                y_str += line[i]
            else:
                x_str += line[i]

def dimensions(line):
    colon_loc = line.index(':')
    building_h = False
    w_str = ''
    h_str = ''
    for i in range(colon_loc + 1, len(line)):
        if line[i] == 'x':
            building_h = True
        else:
            if building_h:
                h_str += line[i]
            else:
                w_str += line[i]
    return int(w_str), int(h_str)

FABRIC_WIDTH = 1000
FABRIC_HEIGHT = 1000

fabric = [0] * FABRIC_WIDTH * FABRIC_HEIGHT

def mark(dest, x, y, w, h):
    start_idx = y * FABRIC_WIDTH + x
    for px in range(0, w):
        for py in range(0, h):
            dest[(y + py) * FABRIC_WIDTH + (x + px)] += 1

for line in lines:
    # format "#1 @ 1,3: 4x4"
    line = line.replace(' ', '')
    x, y = coords(line)
    w, h = dimensions(line)

    mark(fabric, x, y, w, h)

# sum total of square inches of overlap
overlapping_cells = filter(lambda x: x > 1, fabric)
print "Overlapping cell count = %i" % len(overlapping_cells)
