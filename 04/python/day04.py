"""
Advent of Code 2018
Day 4: Repose Record
"""
from collections import namedtuple, defaultdict

Observation = namedtuple('Observation', ['year','month','day','hour','minute','event'])


def parse_observation(input_string):
    "Parse observation."
    year = int(input_string[1:5])
    month = int(input_string[6:8])
    day = int(input_string[9:11])
    hour = int(input_string[12:13])
    minute = int(input_string[15:17])
    event = input_string[19:]
    return Observation(year, month, day, hour, minute, event)


def solveA(observations):
    "Solve first part of puzzle."
    guard_sleep_time = defaultdict(int)
    guard_on_duty = 0
    sleep_time = None
    guard_events = defaultdict(list)
    for observation in observations:
        if observation.event[0] == 'G':
            guard_on_duty = int(observation.event.split()[1][1:])
        if observation.event == 'falls asleep':
            sleep_time = observation.minute
            guard_events[guard_on_duty].append((observation.minute, observation.event))
        if observation.event == 'wakes up':
            guard_sleep_time[guard_on_duty] += observation.minute - sleep_time
            guard_events[guard_on_duty].append((observation.minute, observation.event))
    _, sleepiest_guard = max((v, k) for k, v in guard_sleep_time.items())

    sleep_frequency = {}
    sleep_counter = 0
    for sleep_event in sorted(guard_events[sleepiest_guard]):
        if sleep_event[1] == 'falls asleep':
            sleep_counter += 1
        else:
            sleep_frequency[sleep_event[0] - 1] = sleep_counter
            sleep_counter -= 1
    _, most_frequent_sleep_time = max((v, k) for k, v in sleep_frequency.items())
    return most_frequent_sleep_time * sleepiest_guard


def main():
    "Main program."
    import sys
    observations = sorted([parse_observation(s.strip()) for s in sys.stdin])
    # print("\n".join(str(o) for o in observations))
    print(solveA(observations))


if __name__ == '__main__':
    main()
