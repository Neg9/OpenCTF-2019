"""
Test the flip-the-script CTF challenge.
"""
import unittest

import requests


# The local challenge HTTP server
SERVER = 'http://localhost:3000/'


class ChallengeTest(unittest.TestCase):
    """ Run integration tests for the Flip the Script challenge.
    """

    def test_correct(self):
        """ Test the correct answer.
        """
        result = self.send_answer('submit', '/*"+/*\'*/i/+target.exploit//')
        self.assertIn('flag{', result)

    def test_too_long(self):
        """ Test an answer that is too long.
        """
        result = self.send_answer('submit', '/*"+/*\'*/i/+target.exploit///')
        self.assertNotIn('flag{', result)

    def test_too_many_stars(self):
        """ Test an answer that works, but is banned.
        """
        result = self.send_answer('submit', '/*"+/*\'+/**/target.exploit//')
        self.assertNotIn('flag{', result)

    def test_invalid_characters(self):
        """ Test a solution with banned characters.
        """
        result = self.send_answer('submit', 'abc()')
        self.assertIn('Invalid characters', result)

    def test_empty_answer(self):
        """ GET the answer endpoint without submitting a solution.
        """
        result = self.get('submit')
        self.assertIn('Please provide', result)

    def test_html_and_javascript(self):
        """ Get the HTML and JavaScript files.
        """
        for filename in ['', 'flip-the-script.js', 'client.js']:
            result = self.get(filename)
            self.assertTrue(result)

    def test_invalid_web_file(self):
        """ Try to access the flag directly.
        """
        result = self.get('flag.txt')
        self.assertNotIn(result, 'flag{')

    def test_invalid_web_file(self):
        """ Get a nonexistent HTML or JavaScript file.
        """
        result = self.get('abc.html')
        self.assertIn('Invalid file', result)

    def send_answer(self, path, answer):
        """ Submit an answer.
        """
        response = self.get(path, headers={'answer': answer})
        return response

    def get(self, path, **kwargs):
        """ Make an HTTP request.
        """
        response = requests.get(SERVER + path, **kwargs)
        return response.text


if __name__ == '__main__':
    unittest.main()

