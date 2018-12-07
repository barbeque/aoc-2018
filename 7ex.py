import re

with open('input7.txt') as i:
    lines = i.readlines()

instructions = []

for line in lines:
    match = re.match(r'Step ([A-Z]+) must be finished before step ([A-Z]+) can begin\.', line)

    if match:
        prerequisite = match.group(1)
        step = match.group(2)
        instructions.append((prerequisite, step))
    else:
        assert "no match on line '%s'" % line

class GraphNode:
    def __init__(self, my_id):
        self.my_id = my_id
        self.has_visited = False
        # from this node to another
        self.out_nodes = []
        # from another node to this one
        self.in_nodes = []

    def mark_visited(self):
        assert self.can_mark()

        self.has_visited = True

    def can_mark(self):
        return len(filter(lambda n: n.has_visited != True, self.in_nodes)) == 0

    def attach_child(self, new_node):
        # doubly linked
        self.out_nodes.append(new_node)
        new_node.in_nodes.append(self)

# let's build the graph
all_nodes = {}

# part 1: construct all nodes
for instruction in instructions:
    if instruction[0] not in all_nodes.keys():
        all_nodes[instruction[0]] = GraphNode(instruction[0])
    if instruction[1] not in all_nodes.keys():
        all_nodes[instruction[1]] = GraphNode(instruction[1])

print 'Nodes loaded = %i' % len(all_nodes)

# part 2: construct all relationships
# sure this is slower, but it doesn't really matter
for instruction in instructions:
    from_node = all_nodes[instruction[0]]
    to_node = all_nodes[instruction[1]]
    from_node.attach_child(to_node)

def get_available_nodes(all_nodes):
    untraveled_nodes = filter(lambda n: not n.has_visited, all_nodes.values())
    markable_nodes = filter(lambda n: n.can_mark(), untraveled_nodes)
    return markable_nodes

# part 3: traverse graph
def get_next_available_node(all_nodes):
    avails = get_available_nodes(all_nodes)
    assert len(avails) > 0, "Ran out of nodes!"
    s = sorted(avails, key=lambda n: n.my_id)
    return s[0]

traversal_log = []
while len(traversal_log) < len(all_nodes):
    hit_next = get_next_available_node(all_nodes)
    hit_next.mark_visited()

    traversal_log.append(hit_next.my_id)

print 'Traversal log: %s' % ''.join(traversal_log)
