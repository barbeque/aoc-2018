import datetime

with open('input4.txt') as i:
    lines = i.readlines()

def get_date(line):
    return line[1:11]

assert get_date('[1518-11-01 00:00] Guard #10 begins shift') == '1518-11-01'

def get_datetime(line):
    return line[1:17]

def get_instruction(line):
    return line[18:].strip()

def decomp_datetime(datetime):
    year = int(datetime[:4])
    month = int(datetime[5:7])
    day = int(datetime[8:10])
    hour = int(datetime[11:13])
    minute = int(datetime[14:17])
    return (year, month, day, hour, minute)

def minutes_between(a, b):
    (year_a, month_a, day_a, hour_a, minute_a) = decomp_datetime(a)
    (year_b, month_b, day_b, hour_b, minute_b) = decomp_datetime(b)

    a = datetime.datetime(year_a, month_a, day_a, hour_a, minute_a)
    b = datetime.datetime(year_b, month_b, day_b, hour_b, minute_b)

    return (b - a).total_seconds() / 60

assert decomp_datetime('2014-11-12 22:12') == (2014, 11, 12, 22, 12)
assert minutes_between('2014-11-01 22:00', '2014-11-01 22:01') == 1

# input is unsorted; need to sort this by date and time
lines = sorted(lines, key=get_datetime)

current_guard = ''
last_sleep = ''

# need to keep track of spans (start, length)
sleep_records = {}

for line in lines:
    this_datetime = get_datetime(line)
    (date, time) = this_datetime.split()
    instruction = get_instruction(line)

    if instruction.startswith('Guard #'):
        # guard beginning shift, parse their number
        new_guard = ''
        for i in range(7, len(instruction)):
            if instruction[i] == ' ':
                current_guard = new_guard
                break
            else:
                new_guard += instruction[i]
        #print 'Guard now [%s]' % new_guard
        last_sleep = ''
    elif instruction.startswith('falls asleep'):
        assert last_sleep == '', "Double sleep detected"
        last_sleep = this_datetime
    elif instruction.startswith('wakes up'):
        # measure distance between this datetime and last_sleep
        this_sleep = minutes_between(last_sleep, this_datetime)
        start_mins = int(last_sleep.split()[1][3:])

        sleep_record = (start_mins, this_sleep)

        if current_guard in sleep_records:
            sleep_records[current_guard].append(sleep_record)
        else:
            sleep_records[current_guard] = [ sleep_record ]

        last_sleep = ''

most_minutes = -1
heaviest_sleeper = ''

for guard in sleep_records.keys():
    total_minutes_slept = 0
    for (start, length) in sleep_records[guard]:
        total_minutes_slept += length # ehhhh so ugly

    if total_minutes_slept > most_minutes:
        most_minutes = total_minutes_slept
        heaviest_sleeper = guard

print "Heaviest sleeper was %s with %i minutes" % (heaviest_sleeper, most_minutes)



def get_sleepiest_minute(guard):
    # find minute of most overlap
    minute_to_sleeps = {}
    for wall_minute in range(0, 59):
        for (start, length) in sleep_records[guard]:
            # i think i saw 23:59 some places, so watch out for that
            if wall_minute >= start and wall_minute < start + length:
                # count it
                if wall_minute not in minute_to_sleeps:
                    minute_to_sleeps[wall_minute] = 1
                else:
                    minute_to_sleeps[wall_minute] += 1

    # find overlappiest minute
    max_sleeps = -1
    max_minute = -1
    for minute in minute_to_sleeps.keys():
        if minute_to_sleeps[minute] > max_sleeps:
            max_sleeps = minute_to_sleeps[minute]
            max_minute = minute

    return (max_minute, max_sleeps)

# Part 1: which minute is the sleepiest guard
# the most consistently asleep for?

(max_minute, max_sleeps) = get_sleepiest_minute(heaviest_sleeper)

print "Most popular minute = %i (slept %i times)" % (max_minute, max_sleeps)

print "Part 1: answer is maybe %i x %i = %i" % (int(heaviest_sleeper), int(max_minute), int(heaviest_sleeper) * int(max_minute))

# Part 2: Which guard is the most consistently asleep?

most_sleeps_so_far = -1
their_minute = -1
that_guard = -1

for guard in sleep_records.keys():
    (their_sleepiest_minute, times_slept_then) = get_sleepiest_minute(guard)
    if times_slept_then > most_sleeps_so_far:
        most_sleeps_so_far = times_slept_then
        their_minute = their_sleepiest_minute
        that_guard = guard

print "Guard %s slept %i times on minute %i" % (that_guard, most_sleeps_so_far, their_minute)

print "Part 2: answer is maybe guard %i x minute %i = %i" % (int(that_guard), int(their_minute), int(that_guard) * int(their_minute))
