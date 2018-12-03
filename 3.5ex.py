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

fabric = []
for y in range(0, FABRIC_HEIGHT):
    for x in range(0, FABRIC_WIDTH):
        fabric.append([]) # ugh

def mark(dest, line_id, x, y, w, h):
    for px in range(0, w):
        for py in range(0, h):
            item = dest[(y + py) * FABRIC_WIDTH + (x + px)]
            item.append(line_id)
#            print '(%i, %i) length = %i' % (x + px, y + py, len(item))

def get_id(line):
    hash_loc = line.index('#')
    id_str = ''
    for i in range(hash_loc + 1, len(line)):
        if line[i] == '@':
            return int(id_str)
        else:
            id_str += line[i]

line_ids = []

for line in lines:
    # format "#1 @ 1,3: 4x4"
    line = line.replace(' ', '')
    x, y = coords(line)
    w, h = dimensions(line)

    line_id = get_id(line)
    line_ids.append(line_id)
    #print 'line_id = %s' % line_id

    mark(fabric, line_id, x, y, w, h)

# sum total of square inches of overlap
overlapping_cells = filter(lambda x: len(x) > 1, fabric)
print "Overlapping cell count = %i" % len(overlapping_cells)

for line_id in line_ids:
    cells_with_me = filter(lambda x: line_id in x, fabric)
    cells_with_only_me = filter(lambda x: len(x) == 1, cells_with_me)
    if len(cells_with_me) == len(cells_with_only_me):
        print 'Found a singleton = %i' % line_id
        return
