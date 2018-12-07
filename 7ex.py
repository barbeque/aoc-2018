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
    # Let's imagine we are evaluating B -> Y.

    # First stop, get all of the instructions that produce Y.
    instructions_producing_me = \
        filter(lambda i: i[1] == rs[1], instructions)

    # If there are, make sure that all of those instructions
    # can be executed, right now.
    # This will include checking if B has been travelled to.
    for instruction_producing_me in instructions_producing_me:
        prereq = instruction_producing_me[0]
        if prereq not in completed_steps:
            return False

    return True

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

while len(instructions) > 0:
    potential_next_steps = find_available_steps(completed_steps, instructions)

    if len(potential_next_steps) == 0:
        print "ran out of steps: %s [%i]" % (''.join(completed_steps), len(completed_steps))
        print "never-hit instructions:"
        for instruction in instructions:
            print "%s => %s" % (instruction[0], instruction[1])
        assert False
        

    # take the alphabetically earliest one
    # ...and delete it
    next_rs = sorted(potential_next_steps)[0]
    instructions.remove(next_rs)

    print 'Possible steps: %s' % ', '.join(map(lambda rs: "%s => %s" % (rs[0], rs[1]), potential_next_steps))
    print 'Taking %s => %s' % (next_rs[0], next_rs[1])

    # mark it down and keep going
    completed_steps.append(next_rs[1])

    # remove all other instructions where next_rs[1] == instruction[1],
    # so we don't double visit...
    instructions = filter(lambda inst: inst[1] != next_rs[1], instructions)

assert len(set(completed_steps)) == len(completed_steps), "DOUBLE VISIT DETECTED"

# i assume we are completed now
s = ''.join(completed_steps)
print '%i steps taken' % len(s)
print 'Correct order: %s' % s
