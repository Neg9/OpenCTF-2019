"""
Configuration for the stylist CTF challenge.
"""
import os.path


# A path to the flag
FLAG_PATH = os.path.join(os.path.dirname(__file__), '..', 'flag.txt')

# An output file path
HTML_PATH = os.path.join(os.path.dirname(__file__), '..', 'stylist.html')

# A path to the scoreboard config file
YAML_PATH = os.path.join(os.path.dirname(__file__), '..', 'challenge.yaml')

# This challenge's point value
POINTS = 100

