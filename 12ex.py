import sys

def parse_rule(rule):
    (match, arrow, result) = rule.split()
    new_match = []
    # what is the pattern we identify?
    for c in match:
        if c == '#':
            new_match.append(True)
        elif c == '.':
            new_match.append(False) # should use map
        else:
            assert "Unknown character in rule"

    # what do we turn the pot under inspection into?
    if result == '#':
        return (new_match, True, rule.strip())
    else:
        return (new_match, False, rule.strip())

assert parse_rule('##### => .')[0] == [True, True, True, True, True]
assert parse_rule('##### => .')[1] == False
assert parse_rule('#.#.# => .')[0] == [True, False, True, False, True]

with open('input12-test.txt') as i:
    initial_state = i.readline()
    assert initial_state.startswith('initial state:')

    idx = len('initial state: ')
    initial_state = initial_state[idx:].strip() # works
    print initial_state # works

    i.readline() # skip blank

    # read the rest
    rules = i.readlines()

    # parse the rules
    new_rules = []
    for rule in rules:
        new_rules.append(parse_rule(rule))

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

def display_state(turn, offset, state):
    sys.stdout.write('%04d:' % turn)
    for i in range(0, len(state) - offset):
        if state[i + offset]:
            sys.stdout.write('#')
        else:
            sys.stdout.write('.')
    print ''


def should_apply(rule, pot_idx, state):
    # get the slice representing the pot idx
    if pot_idx + 2 >= len(state) or pot_idx + 1 >= len(state):
        # ran off right side
        return False
    if pot_idx - 2 < 0 or pot_idx - 1 < 0:
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

    # apply rules
    for i in range(0, len(state)):
        for rule in rules:
            if should_apply(rule, i, state):
                # apply rule
                new_state.append(rule[1])
                #print 'applying rule [%s] at idx %i' % (rule[2], i - 100) # hack
                break
        else:
            # no rule applied, copy from the old state
            new_state.append(False) # hack

    assert len(state) == len(new_state), "Lengths not the same on input and output, corrupted"
    return new_state

original_length = len(state)

# there is clearly a ton of padding in both fucking directions - it inflates a length 25 to a length 39 in the example
PADDING = 100 # that should be enough
for i in range(0, PADDING):
    state = [False] + state + [False]
assert len(state) == original_length + 2 * PADDING

start_offset = PADDING

display_state(0, start_offset, state)

NUM_GENS = 20
for turn in range(0, NUM_GENS):
    state = apply_rules(rules, state)
    display_state(turn + 1, start_offset, state)

# get the sum of plant indices starting at position 0
s = 0
for i in range(0, original_length):
    if state[i + PADDING] == True:
        s += i

print 'Index-sum of plants at end of run: %i' % s
# it wasn't 2186, 48, 46, 40, or 33 - we need to solve the fucking negative index problem
