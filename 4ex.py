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

# TODO: find minute of most overlap
