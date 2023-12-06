from itertools import chain

from utils import benchmark, get_day, extract_ints

test = """seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4
"""


def parse(raw: str):
    sections = raw.split("\n\n")
    seeds = extract_ints(sections[0])
    ret = []
    for stage in sections[1:]:
        stage_mappings = []
        title, rest = stage.split(" map:\n")
        for line in rest.splitlines():
            dest, src, leng = extract_ints(line)
            stage_mappings.append((range(src, src + leng), range(dest, dest + leng)))
        ret.append(stage_mappings)
    return seeds, ret


def part1(raw: str):
    seed_list, stage_list = parse(raw)
    end_zones = []
    for seed in seed_list:
        for mapping_list in stage_list:
            for src_range, dest_range in mapping_list:
                if seed in src_range:
                    seed = seed + dest_range[0] - src_range[0]
                    break
        end_zones.append(seed)
    return min(end_zones)


def part2(raw: str):
    seed_list, stage_list = parse(raw)
    seed_list = list(zip(seed_list[::2], seed_list[1::2]))
    seed_list = (range(x, x + y) for x, y in seed_list)
    seed_list = list(seed_list)
    for stage in stage_list:
        # in order with no repeats
        parting_lines = sorted(set(
            chain(chain.from_iterable((src_range.start, src_range.stop) for src_range, _ in stage),
                  chain.from_iterable((seed.start, seed.stop) for seed in seed_list))))

        # also in order with no repeats
        new_seed_list = []
        for start, stop in zip(parting_lines, parting_lines[1:]):
            for seed in seed_list:
                if start in seed and stop - 1 in seed:
                    new_seed_list.append(range(start, stop))
                    break
        seed_list = new_seed_list

        new_seed_list = []
        for seed in seed_list:
            used_seed = False
            for src_range, dest_range in stage:
                if seed.start in src_range and seed.stop - 1 in src_range:
                    new_seed_list.append(range(seed.start + dest_range.start - src_range.start,
                                               seed.stop + dest_range.start - src_range.start))
                    used_seed = True
                    break
            if not used_seed:
                new_seed_list.append(seed)
        seed_list = new_seed_list

    return min([x.start for x in seed_list])


def main():
    raw = get_day(5, test)
    benchmark(part1, raw)
    benchmark(part2, raw)


if __name__ == "__main__":
    main()
