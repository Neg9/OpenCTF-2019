"""
stylist - a CTF challenge
=========================

Hide a flag in an HTML file with CSS rules.
"""
import random

import config


def read_flag(path=config.FLAG_PATH):
    """ Read the flag from disk.
    """
    with open(path) as fp:
        return fp.read().strip()


class StyleCreator:

    # A template for CSS colors
    COLOR_TEMPLATE = '#0000{}'

    # HTML for the challenge
    HTML_STRING_TEMPLATE = '''
<!DOCTYPE html>
<html>
  <head>
  <title>Stylist</title>
  <meta charset="utf-8">
  <style>
    #blocks div {
      height: 2em;
      width: 2em;
      margin: 1em;
      display: inline-block;
    }
  </style>
  </head>
  <body>
    <div id="blocks">
%(blocks)s
    </div>
  </body>
</html>
'''

    # A prefix for HTML IDs
    ID_PREFIX = 'n'

    # An HTML template for one block
    BLOCK_TEMPLATE = '      <div id="{}{:02d}" style="background: {};"></div>'

    def __init__(self):
        """ Initialize the flag.
        """
        self.flag = read_flag()

    def generate_html(self):
        """ Generate HTML for the challenge.
        """
        prefix = self.ID_PREFIX
        colors = [self.COLOR_TEMPLATE.format(value)
                  for value
                  in self.get_color_values()]

        blocks = [self.BLOCK_TEMPLATE.format(prefix, i, color)
                  for i, color in enumerate(colors)]

        shuffler = random.SystemRandom()
        shuffler.shuffle(blocks)

        return self.HTML_STRING_TEMPLATE % {
            'blocks': '\n'.join(blocks),
        }

    def get_color_values(self):
        """ Get hex color values.
        """
        for character in self.flag:
            number = ord(character)
            hex_value = hex(number)[2:]
            padded = hex_value.zfill(2)
            yield padded


def main():
    """ Create the challenge file.
    """
    style = StyleCreator()
    html = style.generate_html()
    with open(config.HTML_PATH, 'w') as fp:
        fp.write(html)


if __name__ == '__main__':
    main()
