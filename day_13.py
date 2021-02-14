#!/usr/bin/python3

from collections import namedtuple

BusInfo = namedtuple("BusInfo", ["bus_id", "depart_time"])


def read_file(day: str):
    with open(f"input/day_{day}.txt") as file:
        lines = [line.strip() for line in file]
        timestamp = int(lines[0])
        line_ids = [int(bus_id) for bus_id in lines[1].split(",") if bus_id != "x"]
        contest_ids = list()
        all_ids = lines[1].split(",")
        for i in range(len(all_ids)):
            if all_ids[i] != "x":
                contest_ids.append(BusInfo(int(all_ids[i]), i))
        return timestamp, line_ids, contest_ids


def phase_1(input):
    timestamp = input[0]
    bus_ids = input[1]
    time_to_wait = [x - (timestamp % x) for x in bus_ids]
    # print(input)
    # print(f'Wait times: {time_to_wait}')
    min_time = min(time_to_wait)
    ix = time_to_wait.index(min_time)
    return f"Time to wait {min_time} for id {bus_ids[ix]}: {min_time * bus_ids[ix]}"


def phase_2(input):
    buses = sorted(input[2], key=lambda b: b.depart_time)
    print(f"Buses:{[(x.bus_id, x.depart_time) for x in buses]}")
    skip = 1  # Currently repeating interval
    t = 1  # time
    for bus in buses:
        # Find nex repeating interval (previous repeat + current)
        while (t + bus.depart_time) % bus.bus_id != 0:
            t += skip
        skip = skip * bus.bus_id
        print(f"At {t}, bus {bus.bus_id} done, skip is set to {skip}")

    return t


def execute(input):
    p1 = phase_1(input)
    print(f"Phase 1: {p1}\n")

    p2 = phase_2(input)
    print(f"Phase 2: {p2}")


if __name__ == "__main__":
    for day_input in ["13_s", "13"]:
        print(f"For {day_input}:")
        input = read_file(day_input)
        execute(input)
        print("..............")
