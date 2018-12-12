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


def should_apply(rule, pot_idx, state):
    # get the slice representing the pot idx
    if pot_idx + 2 >= len(state) or pot_idx + 1 >= len(state):
        # ran off right side
        return False
    if pot_idx - 2 < 0 or pot_idx -1 < 0:
        # ran off left side
        return False

    chunk = state[(pot_idx - 2):(pot_idx)] + state[(pot_idx):(pot_idx + 3)]
    assert len(chunk) == 5, 'sliced chunk at position %i is wrong size %i' % (i, len(chunk))
    
    if chunk == rule[0]:
        return True
    return False

assert should_apply(([True, True, False, True, True], True), 2, [True, True, False, True, True])

def apply_rules(rules, state):
    new_state = []

    # how the fuck do we deal with the negative numbers?
    # do they get applied? do we always assume anything left of 0 is always not-plant?

    # apply rules
    for i in range(0, len(state)):
        for rule in rules:
            if should_apply(rule, i, state):
                # apply rule
                new_state.append(rule[1])
                break
        else:
            # no rule applied, so don't bother
            new_state.append(state[i])

    assert len(state) == len(new_state), "Lengths not the same on input and output, corrupted"
    return new_state

original_length = len(state)

# there is clearly a ton of padding in both fucking directions - it inflates a length 25 to a length 39 in the example
PADDING = 100 # that should be enough
for i in range(0, PADDING):
    state = [False] + state + [False]

start_offset = PADDING

display_state(0, state)

NUM_GENS = 20
for turn in range(0, NUM_GENS):
    state = apply_rules(rules, state)
    display_state(turn + 1, state)

# get the sum of plants
s = 0
for i in range(0, original_length):
    if state[i + PADDING] == True:
        s += 1

print 'Total number of plants at end of run: %i' % s
# it wasn't 48, 46, 40, or 33 - we need to solve the fucking negative index problem
