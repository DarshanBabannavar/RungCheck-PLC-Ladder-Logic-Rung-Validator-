import re
import sys

INPUT_INSTRUCTIONS = ("XIC", "XIO")
OUTPUT_INSTRUCTIONS = ("OTE", "OTU")

INPUT_ADDRESS = re.compile(r"^I[0-9]\.[0-9]$")
OUTPUT_ADDRESS = re.compile(r"^O[0-9]\.[0-9]$")


def check_rung(line):
    tokens = line.split()
    kinds = []

    if not tokens:
        return "empty rung"

    for position in range(0, len(tokens), 2):
        instruction = tokens[position]

        if instruction in INPUT_INSTRUCTIONS:
            pattern = INPUT_ADDRESS
            kinds.append("in")
        elif instruction in OUTPUT_INSTRUCTIONS:
            pattern = OUTPUT_ADDRESS
            kinds.append("out")
        else:
            return "unknown instruction"

        address = tokens[position + 1] if position + 1 < len(tokens) else ""

        if not pattern.match(address):
            return "bad address"

    output_count = kinds.count("out")

    if output_count == 0:
        return "missing output"
    if output_count > 1:
        return "too many outputs"

    if kinds.index("out") != len(kinds) - 1 or len(kinds) == 1:
        return "output not last"

    return None


def check_lines(lines):
    rung_count = 0
    problems = []

    for line_number, raw in enumerate(lines, start=1):
        line = raw.strip()

        if not line:
            continue

        rung_count += 1
        reason = check_rung(line)

        if reason is not None:
            problems.append((line_number, reason))

    return rung_count, problems


def check_file(path):
    with open(path, encoding="utf-8") as handle:
        return check_lines(handle)


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv

    if len(argv) != 1:
        print("usage: pass the path of exactly one rung file")
        return 2

    try:
        rung_count, problems = check_file(argv[0])
    except OSError as error:
        print("cannot read {}: {}".format(argv[0], error.strerror))
        return 2

    for line_number, reason in problems:
        print("{}: {}".format(line_number, reason))

    print("Checked {} rungs, {} invalid.".format(
        rung_count, len(problems)
    ))

    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())