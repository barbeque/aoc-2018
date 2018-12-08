with open('input8.txt') as i:
    tokens = map(lambda i: int(i), i.read().split())

print '%i tokens loaded' % len(tokens)

def parse_node(offset, tokens):
    ip = offset

    children = tokens[ip]
    ip += 1
    metadata = tokens[ip]
    ip += 1

    nodes = []

    for i in range(0, children):
        (length, node) = parse_node(ip, tokens)
        nodes.append(node)
        ip += length # advance to the next node

    metadatas = []

    for j in range(0, metadata):
        metadatas.append(tokens[ip])
        ip += 1

    node = { 'length': ip - offset, 'metadatas': metadatas, 'nodes': nodes }
    return (ip - offset, node)

def total_metadata(node):
    s = 0
    for child in node['nodes']:
        s += total_metadata(child)
    s += sum(node['metadatas'])
    return s

# let's do it
(length, root) = parse_node(0, tokens)
assert length == len(tokens), "Root node was wrong length %i" % length

# okay let's iterate it
total_mds = total_metadata(root)
print 'Total metadata = %i' % total_mds
