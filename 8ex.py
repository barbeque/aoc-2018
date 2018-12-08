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

def node_value(node):
    if len(node['nodes']) == 0:
        # if a node has no child nodes, its value is the
        # sum of its metadata
        return sum(node['metadatas'])
    else:
        # if a node DOES have child nodes, the metadata
        # is an index which refers to those child nodes
        # metadata = 1 means the first child node,
        # metadata = 2 the second...
        # result is the sum of the values of the child nodes
        # pointed to by the metadatas.
        s = 0
        for md in node['metadatas']:
            node_idx = md - 1 # 1-indexed
            if node_idx < len(node['nodes']) and node_idx >= 0:
                s += node_value(node['nodes'][node_idx])
        return s

# let's do it
(length, root) = parse_node(0, tokens)
assert length == len(tokens), "Root node was wrong length %i" % length

# okay let's iterate it
total_mds = total_metadata(root)
print 'Total metadata = %i' % total_mds

root_value = node_value(root)
print 'Node value of root = %i' % root_value
