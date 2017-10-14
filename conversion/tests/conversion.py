import unittest
import subprocess
import os


class TestConversion(unittest.TestCase):
    def test_codeblock(self):
        self._compare_fixtures('code-example')

    def test_table(self):
        self._compare_fixtures('table')

    def _compare_fixtures(self, fixture_name):
        expected_fixture = 'expected-' + fixture_name

        dir_path = os.path.dirname(os.path.realpath(__file__))

        process = subprocess.Popen(
            [
                'python',
                dir_path + '/../DocBookToReST.py',
                dir_path + '/fixtures/' + fixture_name + '.xml'
            ],
            stdout=subprocess.PIPE
        )
        out, err = process.communicate()

        with open(dir_path + '/fixtures/' + expected_fixture + '.rst', 'r') as content_file:
            expected_content = content_file.read()

        self.assertEqual(out, expected_content)


if __name__ == '__main__':
    unittest.main()
