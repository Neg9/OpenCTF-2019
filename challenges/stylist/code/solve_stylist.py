"""
Solve the "stylist" CTF challenge.

Sort by <div> IDs, then convert the hex colors to an ASCII character.
"""
import re

import config


def process_styles(divs):
    """ Read values from CSS rules in an HTML file.
    """
    for style in divs:
        pattern = re.compile(r'n(\d+).* #([a-f0-9]{6})')
        match = re.search(pattern, style)
        index = int(match[1])
        color = int(match[2], 16)
        yield (index, color)

def solve():
    """ Parse colors in an HTML file, to get a flag.
    """
    with open(config.HTML_PATH) as fp:
        divs = [
            line.strip()
            for line in fp
            if 'background' in line
        ]
        styles = process_styles(divs)
        numbers = [number for _, number in sorted(styles)]
        result = ''.join(chr(number) for number in numbers)
        return result


def main():
    """ Solve the challenge, and print the solution.
    """
    solution = solve()
    print(solution)


if __name__ == '__main__':
    main()

