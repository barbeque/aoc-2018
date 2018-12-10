import re
from PIL import Image

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

    #print 'position = %i, %i => velocity = %i, %i' % (x, y, vx, vy)
    nodes.append({ 'x': x, 'y': y, 'vx': vx, 'vy': vy })

def bounding_rect(nodes):
    min_x = 100000
    min_y = 100000
    max_x = -100000
    max_y = -100000

    for node in nodes:
        if node['x'] < min_x:
            min_x = node['x']
        if node['y'] < min_y:
            min_y = node['y']
        if node['x'] > max_x:
            max_x = node['x']
        if node['y'] > max_y:
            max_y = node['y']
    return ( min_x, min_y, max_x, max_y )

def update(nodes):
    for node in nodes:
        node['x'] += node['vx']
        node['y'] += node['vy']

def dump_frame_to_disk(nodes, width, height, t):
    im = Image.new('L', (width + 1, height + 1), 'black')
    pixels = im.load()

    (min_x, min_y, max_x, max_y) = bounding_rect(nodes)

    for node in nodes:
        x = node['x'] - min_x
        y = node['y'] - min_y

        assert x >= 0 and x <= abs(max_x - min_x), "%i too big for width %i" % (x, width)
        assert y >= 0 and y <= abs(max_y - min_y), "%i too big for height %i" % (y, height)

        pixels[x, y] = 255 # white

    im.save('frame-%i.png' % t, 'PNG')

def render_frame(nodes, prev_width, prev_height, t):
    (min_x, min_y, max_x, max_y) = bounding_rect(nodes)

    width = abs(max_x - min_x)
    height = abs(max_y - min_y)

    if t > 9998:
        # clued in by about when dimensions started increasing
        dump_frame_to_disk(nodes, width, height, t)
        import pdb; pdb.set_trace()

    #print 'map is now %i by %i' % (width, height)

    return (width, height)

# i guess render steps
iters = 100000
w = 1000000
h = 1000000
for i in range(0, iters):
    (w, h) = render_frame(nodes, w, h, i)
    update(nodes)
