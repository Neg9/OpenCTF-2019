"""
Generate and write a YAML config file for the scoreboard.
"""
import os.path

import config
import generate_stylist


TEMPLATE = """category: coding
description: Decode a flag within an HTML page
flags:
    - flag: {}
name: Stylist
value: {}
files:
- stylist.html
"""


def main():
    """ Write the challenge YAML file.
    """
    with open(config.YAML_PATH, 'w') as fp:
        flag = generate_stylist.read_flag()
        text = TEMPLATE.format(flag, config.POINTS)
        fp.write(text)


if __name__ == '__main__':
    main()

