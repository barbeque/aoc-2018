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

        # time to complete
        self.duration = 60 + (ord(my_id) - ord('A') + 1)

    def mark_visited(self):
        assert self.can_mark()

        self.has_visited = True

    def can_mark(self):
        return len(filter(lambda n: n.has_visited != True, self.in_nodes)) == 0

    def attach_child(self, new_node):
        # doubly linked
        self.out_nodes.append(new_node)
        new_node.in_nodes.append(self)

assert GraphNode('A').duration == 61
assert GraphNode('Z').duration == 86

# let's build the graph
all_nodes = {}

# part 1: construct all nodes
for instruction in instructions:
    if instruction[0] not in all_nodes.keys():
        all_nodes[instruction[0]] = GraphNode(instruction[0])
    if instruction[1] not in all_nodes.keys():
        all_nodes[instruction[1]] = GraphNode(instruction[1])

print 'Nodes loaded = %i' % len(all_nodes)

total = 0
for node in all_nodes.values():
    total += node.duration
print 'Total time to complete those nodes sequentially would be %i seconds' % (total)

# part 2: construct all relationships
# sure this is slower, but it doesn't really matter
for instruction in instructions:
    from_node = all_nodes[instruction[0]]
    to_node = all_nodes[instruction[1]]
    from_node.attach_child(to_node)

def is_being_worked_on(node, work_in_progress):
    for (started_on, job_node) in work_in_progress:
        if job_node == node:
            return True
    return False

def get_available_nodes(all_nodes, work_in_progress):
    untraveled_nodes = filter(lambda n: not n.has_visited, all_nodes.values())
    markable_nodes = filter(lambda n: n.can_mark(), untraveled_nodes)
    not_working_on = filter(lambda n: not is_being_worked_on(n, work_in_progress), markable_nodes)
    return not_working_on

# part 3: traverse graph
def get_next_available_node(all_nodes, work_in_progress):
    avails = get_available_nodes(all_nodes, work_in_progress)

    # there may not be work available for a worker right now
    if len(avails) < 1:
        return None

    s = sorted(avails, key=lambda n: n.my_id)
    return s[0]

traversal_log = []
t = 0
work_in_progress = []
WORKER_COUNT = 5

def should_close_work(t, wip_record):
    # started_on + time to close
    close_time = wip_record[0] + wip_record[1].duration

    assert t <= close_time, "close_time is in the past. we missed it?"

    return t == close_time

while len(traversal_log) < len(all_nodes):
    # close out all work that closes in this second
    work_to_close = filter(lambda wip: should_close_work(t, wip), work_in_progress)
    for (start, node) in work_to_close:
        node.mark_visited()
        work_in_progress.remove((start, node))
        print "Node %s completed." % (node.my_id)
        traversal_log.append(node.my_id)

    # pick up new work
    while len(work_in_progress) < WORKER_COUNT:
        hit_next = get_next_available_node(all_nodes, work_in_progress)
        if hit_next != None:
            work_in_progress.append( ( t, hit_next ) )
            print "Started worker %i on job %s" % (len(work_in_progress), hit_next.my_id)
        else:
            # worker idled, no work for them :(
            break

    t += 1

print 'Traversal log: %s' % ''.join(traversal_log)
print 'Total time: %i' % (t - 1) # i think -1 is right
