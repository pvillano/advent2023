from utils import benchmark, get_day, test, debug_print

test1 = """rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7"""

expected1 = 1320

test2 = test1
expected2 = 145


def parse(raw: str):
    ret = []
    for line in raw.split(","):
        ret.append(line)
    return ret


def box_hash(raw: str):
    cv = 0
    for ch in raw:
        cv += ord(ch)
        cv *= 17
        cv %= 256
    return cv


def part1(raw: str):
    return sum(map(box_hash, parse(raw)))


def part2(raw: str):
    boxes = [list() for _ in range(256)]
    for line in raw.split(","):
        if "=" in line:
            label, focal_length = line.split("=")
            focal_length = int(focal_length)
            box_id = box_hash(label)
            box = boxes[box_id]
            done = False
            for i in range(len(box)):
                if box[i][0] == label:
                    box[i][1] = focal_length
                    done = True
                    break
            if not done:
                box.append([label, focal_length])
        else:
            label = line.removesuffix("-")
            box_id = box_hash(label)
            box = boxes[box_id]
            for i in range(len(box)):
                if box[i][0] == label:
                    box.remove(box[i])
                    break
        debug_print(f'After "{line}":')
        for box in boxes:
            if box:
                debug_print(box)
    s = 0
    for i, box in enumerate(boxes, start=1):
        for j, lens in enumerate(box, start=1):
            s += i * j * lens[1]
    return s


def main():
    test(part1, test1, expected1)
    raw = get_day(15, override=True)
    benchmark(part1, raw)
    test(part2, test2, expected2)
    benchmark(part2, raw)


if __name__ == "__main__":
    main()
