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

def is_step_available(rs, completed_steps, instructions):
    # get all my pre-reqs in instructions
    # req => action
    # rs[0] must have been completed
    if rs[0] not in completed_steps:
        print 'Rejected %s => %s because %s not completed' % (rs[0], rs[1], rs[0])
        return False
    # all pre-reqs of rs[1] must be in completed_steps
    my_prereqs = filter(lambda i: i[1] == rs[1], instructions)
    unmet_prereqs = filter(lambda i: i[0] not in completed_steps, my_prereqs)

    if len(unmet_prereqs) == 0:
        print '%s => %s can go ahead' % (rs[0], rs[1])
        return True
    else:
        print '%s => %s rejected because %s has unmet requirements' % (rs[0], rs[1], rs[1])
        return False

def find_available_steps(completed_steps, instructions):
    return filter(lambda rs: is_step_available(rs, completed_steps, instructions), instructions)

# ok let's iterate some steps
instructions = sorted(instructions, key=lambda kv: kv[0])
print '%i instructions' % len(instructions)

completed_steps = []

# first step: find a step, or steps with no pre-requisite for it
potential_first_steps = []
for rs in instructions:
    prereq = rs[0]
    if len(filter(lambda rs: rs[1] == prereq, instructions)) == 0:
        # there is no pre-requisite for this step, so advance to it
        potential_first_steps.append(prereq)

print 'There are %i choices for a first step.' % len(potential_first_steps)

# let's run them ALL
for starter in set(potential_first_steps):
    completed_steps.append(starter)

# let's go
assert is_step_available(('A', 'C'), ['A'], [('A', 'C')])
assert not is_step_available(('D', 'F'), ['A'], [('A', 'C'), ('D', 'F')])
assert not is_step_available(('D', 'E'), ['B', 'D'], [('C', 'E'), ('D', 'E')])
assert find_available_steps(['A'], [('A', 'C'), ('D', 'F')]) == [('A', 'C')]

instruction_count = len(instructions)

while len(completed_steps) < instruction_count:
    potential_next_steps = find_available_steps(completed_steps, instructions)
    assert len(potential_next_steps) > 0, ("Ran out of steps... ", completed_steps, len(completed_steps))

    # take the alphabetically earliest one
    # ...and delete it
    next_rs = sorted(potential_next_steps)[0]
    instructions.remove(next_rs)

    print 'Possible steps: %s' % ', '.join(map(lambda rs: "%s => %s" % (rs[0], rs[1]), potential_next_steps))
    print 'Taking %s => %s' % (next_rs[0], next_rs[1])

    if next_rs[1] in completed_steps:
        assert "DOUBLE VISITED %s" % next_rs[1]

    # mark it down and keep going
    completed_steps.append(next_rs[1])

# i assume we are completed now
s = ''.join(completed_steps)
print '%i steps taken' % len(s)
print 'Correct order: %s' % s
