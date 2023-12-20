from collections import deque
from itertools import count
from math import lcm

from utils import benchmark, get_day, test, debug_print


def parse(raw: str):
    ret = {"output": ["%", [False], []]}
    for line in raw.splitlines():
        if line.startswith("broadcaster"):
            ins, outs = line.split(" -> ")
            outs = outs.split(", ")
            ret[ins] = [ins, None, tuple(outs)]
            continue
        kind, line = line[0], line[1:]
        ins, outs = line.split(" -> ")
        outs = outs.split(", ")
        match kind:
            case "%":
                state = [False]
            case "&":
                state = dict()
            case _:
                assert False
        ret[ins] = [kind, state, tuple(outs)]

    for line in raw.splitlines():
        kind, line = line[0], line[1:]
        ins, outs = line.split(" -> ")
        outs = outs.split(", ")
        for o in outs:
            if o in ret and ret[o][0] == "&":
                ret[o][1][ins] = False
    return ret


def part1(raw: str):
    modules = parse(raw)
    # q = deque([("broadcaster", False, "button")] * 1000)

    hpc, lpc = 0, 0
    for i in range(1000):
        q = deque([("broadcaster", False, "button")])
        while q:
            m_id, pulse, origin = q.popleft()
            debug_print(f"{origin} -{pulse}-> {m_id}")
            if pulse:
                hpc += 1
            else:
                lpc += 1
            if m_id not in modules:
                continue
            kind, state, outs = modules[m_id]
            match kind:
                case "broadcaster":
                    for o in outs:
                        q.append((o, False, m_id))
                case "%":
                    if pulse:
                        continue
                    state[0] = not state[0]
                    for o in outs:
                        q.append((o, state[0], m_id))
                case "&":
                    state[origin] = pulse
                    send_low = all(state.values())
                    for o in outs:
                        q.append((o, not send_low, m_id))
                case _:
                    assert False
        debug_print(f"{hpc=}, {lpc=}")
    return hpc * lpc


def part2(raw: str):
    modules = parse(raw)
    first_activated = {k: 0 for k in "hf nd sb ds".split(" ")}
    for i in count(1):
        if i.bit_count() == 1:
            print(f"on {i}")
        q = deque([("broadcaster", False, "button")])
        while q:
            m_id, pulse, origin = q.popleft()
            if m_id in first_activated and not pulse:
                if not first_activated[m_id]:
                    first_activated[m_id] = i
                if all(first_activated.values()):
                    return lcm(*first_activated.values())
            if m_id not in modules:
                continue
            kind, state, outs = modules[m_id]
            match kind:
                case "broadcaster":
                    for o in outs:
                        q.append((o, False, m_id))
                case "%":
                    if pulse:
                        continue
                    state[0] = not state[0]
                    for o in outs:
                        q.append((o, state[0], m_id))
                case "&":
                    state[origin] = pulse
                    send_low = all(state.values())
                    for o in outs:
                        q.append((o, not send_low, m_id))
                case _:
                    assert False


def vis(raw):
    with open("20.gv.txt", "w") as f:
        for line in raw.splitlines():
            if line.startswith("broadcaster"):
                ins, outs = line.split(" -> ")
                outs = outs.split(", ")
            else:
                kind, line = line[0], line[1:]
                ins, outs = line.split(" -> ")
                outs = outs.split(", ")
            f.write(f'"{ins}"\n')
            for o in outs:
                f.write(f'"{ins}" -> "{o}"\n')


test1 = """broadcaster -> a, b, c
%a -> b
%b -> c
%c -> inv
&inv -> a"""

expected1 = 32000000

test11 = """broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output"""

expected11 = 11687500

test2 = test1
expected2 = None


def main():
    test(part1, test1, expected1)
    test(part1, test11, expected11)
    raw = get_day(20, override=True)
    benchmark(part1, raw)

    # vis(raw)

    benchmark(part2, raw)


if __name__ == "__main__":
    main()
