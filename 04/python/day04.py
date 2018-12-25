"""
Advent of Code 2018
Day 4: Repose Record
"""
from collections import namedtuple, defaultdict

Observation = namedtuple('Observation', ['month','day','hour','minute','event'])
Nap = namedtuple('Nap', ['id', 'start', 'end'])


def parse_observation(input_string):
    "Parse observation."
    month = int(input_string[6:8])
    day = int(input_string[9:11])
    hour = int(input_string[12:13])
    minute = int(input_string[15:17])
    event = input_string[19:]
    return Observation(month, day, hour, minute, event)


def observations_to_naps(observations):
    "Get rid of extraneous information."
    naps = []
    sleep_time = 0
    for observation in observations:
        if observation.event[0] == 'G':
            guard_on_duty = int(observation.event.split()[1][1:])
        if observation.event == 'falls asleep':
            sleep_time = observation.minute
        if observation.event == 'wakes up':
            naps.append(Nap(guard_on_duty, sleep_time, observation.minute))
    return naps


def total_nap_time(naps):
    "Get total nap times for each guard."
    nap_time = defaultdict(int)
    for nap in naps:
        nap_time[nap.id] += nap.end - nap.start
    return nap_time


def sleepiest_guard(nap_times):
    "Find the sleepiest guard."
    return max((t, g) for g, t in nap_times.items())[1]


def sleepiest_time(guard, naps):
    "Find the time the sleepiest guard is most likely asleep."
    sleepys_naps = list(filter(lambda x: x.id == guard, naps))
    starts = [(x.start, 1) for x in sleepys_naps]
    ends = [(x.end, -1) for x in sleepys_naps]
    intervals = sorted(starts + ends)
    nap_count = 0
    most_frequent_nap_time = -1
    most_frequent_nap_count = 0

    for interval in intervals:
        if interval[1] < 0:
            if nap_count > most_frequent_nap_count:
                most_frequent_nap_count = nap_count
                most_frequent_nap_time = interval[0] - 1
        nap_count += interval[1]
    return most_frequent_nap_time, most_frequent_nap_count


def solveA(naps):
    "Solve first part of puzzle."
    guard_nap_time = total_nap_time(naps)
    sleepy = sleepiest_guard(guard_nap_time)
    magic_minute = sleepiest_time(sleepy, naps)[0]
    return sleepy * magic_minute


def solveB(naps):
    "Solve second part of puzzle."
    guard_ids = set([x.id for x in naps])
    max_magic_minute_freq = 0
    max_magic_minute = 0
    max_magic_minute_guard = 0
    for guard in guard_ids:
        magic_minute, freq = sleepiest_time(guard, naps)
        if freq > max_magic_minute_freq:
            max_magic_minute_freq = freq
            max_magic_minute = magic_minute
            max_magic_minute_guard = guard
    return max_magic_minute_guard * max_magic_minute


def main():
    "Main program."
    import sys
    observations = sorted([parse_observation(s.strip()) for s in sys.stdin])
    naps = observations_to_naps(observations)
    print(solveA(naps))
    print(solveB(naps))


if __name__ == '__main__':
    main()
