import sys

with open('input12.txt') as i:
    initial_state = i.readline()
    assert initial_state.startswith('initial state:')

    idx = len('initial state: ')
    initial_state = initial_state[idx:].strip()

    i.readline() # skip blank

    # read the rest
    rules = i.readlines()
    
    # parse the rules
    new_rules = []
    for rule in rules:
        (match, arrow, result) = rule.split()
        new_match = []
        for c in match:
            if c == '#':
                new_match.append(True)
            else:
                new_match.append(False) # should use map
        if result == '#':
            new_rules.append((new_match, True))
        else:
            new_rules.append((new_match, False)) # so wasteful
    rules = new_rules

# load the initial_state into state
state = [ False ] * len(initial_state)
for i in range(0, len(initial_state)):
    if initial_state[i] == '#':
        state[i] = True
    elif initial_state[i] == '.':
        state[i] = False
    else:
        assert False, 'Unknown character in initial_state (%s)' % (initial_state[i])

def display_state(turn, state):
    sys.stdout.write('%04d:' % turn)
    for i in range(0, len(state)):
        if state[i]:
            sys.stdout.write('#')
        else:
            sys.stdout.write('.')
    print ''


display_state(0, state)

def should_apply(rule, pot_idx, state):
    # get the slice representing the pot idx
    chunk = state[(pot_idx - 2):(pot_idx)] + state[(pot_idx):(pot_idx + 3)]
    assert len(chunk) == 5, 'sliced chunk is wrong size %i' % len(chunk)
    
    import pdb; pdb.set_trace()

    if chunk == rule[0]:
        return True
    return False

assert should_apply(([True, True, False, True, True], True), 2, [True, True, False, True, True])

def apply_rules(rules, state):
    new_state = []

    # how the fuck do we deal with the negative numbers?
    # do they get applied? do we always assume anything left of 0 is always not-plant?

    assert len(state) == len(new_state), "Lengths not the same on input and output, corrupted"
    return new_state

NUM_GENS = 20
for turn in range(0, NUM_GENS):
    state = apply_rules(rules, state)
    display_state(turn + 1, state)

# get the sum of plants
s = 0
for i in range(0, len(state)):
    if state[i] == True:
        s += 1

print 'Total number of plants at end of run: %i' % s
