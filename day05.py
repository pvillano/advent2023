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
    for section in sections[1:]:
        ass = []
        title, rest = section.split(" map:\n")
        for line in rest.splitlines():
            dest, src, leng = extract_ints(line)
            ass.append((range(src, src + leng), range(dest, dest + leng)))
        ret.append(ass)
    return seeds, ret


def part1(raw: str):
    seeds, mapmap = parse(raw)
    endlocs = []
    for seed in seeds:
        for mm in mapmap:
            for srcrange, destrange in mm:
                if seed in srcrange:
                    seed = seed + destrange[0] - srcrange[0]
                    break
        endlocs.append(seed)
    return min(endlocs)


def part2(raw: str):
    seeds, mapmap = parse(raw)
    seeds = list(zip(seeds[::2], seeds[1::2]))
    seeds = (range(x, x + y) for x, y in seeds)
    seedlist = list(seeds)
    for stage in mapmap:
        newseedlist = []
        partinglines = sorted(set(
            chain([x.start for x, _ in stage], [x.stop for x, _ in stage], [x.start for x in seedlist], [x.stop for x in seedlist])))
        for start, stop in zip(partinglines, partinglines[1:]):
            for seed in seedlist:
                if start in seed and stop-1 in seed:
                    newseedlist.append(range(start, stop))
                    break
        # should be in order with no repeats
        seedlist = newseedlist
        newseedlist = []

        for seed in seedlist:
            used_seed = False
            for srcrange, destrange in stage:
                if seed.start in srcrange and seed.stop - 1 in srcrange:
                    newseedlist.append(range(seed.start + destrange.start - srcrange.start,
                                                 seed.stop + destrange.start - srcrange.start))
                    used_seed = True
                    break
            if not used_seed:
                newseedlist.append(seed)
        seedlist = sorted(set(newseedlist), key= lambda x: x.start)
        # print(seedlist)
    return min([x.start for x in seedlist])


def main():
    raw = get_day(5, test)
    benchmark(part1, raw)
    benchmark(part2, raw)


if __name__ == "__main__":
    main()
