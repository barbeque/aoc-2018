import re

with open('input9.txt') as i:
    lines = i.readlines()

problems = []
for line in lines:
    match = re.match(r'([0-9]+) players; last marble is worth ([0-9]+) points', line)
    assert match, "Should have matched this line"
    players = int(match.group(1))
    winning_score = int(match.group(2))
    problems.append({ 'players': players, 'winning_score': winning_score })

def print_state(player_idx, marble_idx, circle):
    line = '[%i] ' % player_idx
    for i in range(0, len(circle)):
        if i == marble_idx:
            line += '(' + str(circle[i]) + ') '
        else:
            line += str(circle[i]) + ' '
    print line

def get_high_score(players, winning_score):
    # we don't know how many marbles there are, so i guess
    # just keep going until we hit the winning score, then
    step = 0
    total_scores = [ 0 ] * players
    next_marble = 0
    current_marble_idx = 0
    circle = []

    # set up marble 0
    circle.append(0)
    assert circle[current_marble_idx] == 0
    next_marble += 1

    while True:
        this_player = step % players

        # print_state(this_player, current_marble_idx, circle)

        # install the next marble
        # between 1 and 2 marbles clockwise
        if next_marble % 23 == 0:
            # keep the marble
            score = next_marble
            next_marble += 1
            # remove the marble 7 counterclockwise
            idx = (current_marble_idx - 7) % len(circle)
            score += circle.pop(idx)
            # the new current marble is one clockwise of that
            current_marble_idx = (idx) % len(circle)
            
            # add the score
            total_scores[this_player] += score
        else:
            next_i = (current_marble_idx + 2) % len(circle)
            circle.insert(next_i, next_marble)
            next_marble += 1
            current_marble_idx = next_i

        if next_marble - 1 == winning_score:
            print 'Marble worth %i has been placed' % winning_score
            return max(total_scores)

        step += 1

for problem in problems:
    high_score = get_high_score(problem['players'], problem['winning_score'])
    print 'High score for %i players: %i' % (problem['players'], high_score)
