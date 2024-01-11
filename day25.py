import networkx as nx

from utils import benchmark, get_day, test


def parse(raw: str):
    ret = dict()
    for line in raw.splitlines():
        key, values = line.split(': ')
        values = values.split(' ')
        ret[key] = values
    return ret


def part1(raw: str):
    lines = parse(raw)
    g = nx.Graph(lines)
    cut_value, partition = nx.stoer_wagner(g)
    assert cut_value == 3
    return len(partition[0]) * len(partition[1])


test1 = """jqt: rhn xhk nvd
rsh: frs pzl lsr
xhk: hfx
cmg: qnr nvd lhk bvb
rhn: xhk bvb hfx
bvb: xhk hfx
pzl: lsr hfx nvd
qnr: nvd
ntq: jqt hfx bvb xhk
nvd: lhk
lsr: lhk
rzs: qnr cmg lsr rsh
frs: qnr lhk lsr"""

expected1 = 54


def main():
    test(part1, test1, expected1)
    raw = get_day(25, override=True)
    benchmark(part1, raw)


if __name__ == "__main__":
    main()
