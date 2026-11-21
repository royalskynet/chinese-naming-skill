import json
from pathlib import Path
import subprocess
import sys
import unittest

SCRIPTS = Path(__file__).resolve().parents[1] / 'chinese-naming' / 'scripts'
sys.path.insert(0, str(SCRIPTS))
from analyze import analyze
from suggest import suggest


class NamingTests(unittest.TestCase):
    def run_cli(self, script, *args):
        out = subprocess.run(
            [sys.executable, str(SCRIPTS / script), *args],
            capture_output=True, text=True, encoding='utf-8',
        )
        self.assertEqual(out.stderr, '')
        return out.returncode, json.loads(out.stdout)

    def test_analyze_known_names(self):
        cases = {
            '王力宏': [5, 6, 9, 13, 8],
            '陳大明': [17, 19, 11, 27, 9],
            '張三丰': [12, 14, 7, 18, 5],
            '歐陽娜娜': [32, 27, 20, 52, 26],
            '王力': [5, 6, 3, 6, 2],
        }
        for name, expected in cases.items():
            with self.subTest(name=name):
                status, result = self.run_cli('analyze.py', name)
                self.assertEqual(status, 0)
                self.assertEqual([grid['value'] for grid in result['ge'].values()], expected)

    def test_suggestions_match_analysis(self):
        for surname, limit in (('王', 1), ('歐陽', 1), ('微', 10)):
            suggestions = suggest(surname, limit=limit)
            self.assertTrue(suggestions)
            for row in suggestions:
                name = surname + row['mid_candidates'][0] + row['last_candidates'][0]
                with self.subTest(name=name):
                    if surname == '微':
                        self.assertNotIn('生', row['mid_candidates'])
                    result = analyze(name)
                    self.assertEqual(result['surname'], surname)
                    actual_grids = {
                        k: {field: v[field] for field in ('value', 'wuxing')}
                        for k, v in result['ge'].items()
                    }
                    self.assertEqual(actual_grids, row['ge'])
                    self.assertEqual(result['sancai']['config'], row['sancai'])
                    self.assertEqual(result['sancai']['result'], row['sancai_result'])

    def test_cli_reports_invalid_names_and_surnames_as_json(self):
        for script, inputs in (
            ('analyze.py', ('', '王')),
            ('suggest.py', ('', '王王', '王王王')),
        ):
            for value in inputs:
                with self.subTest(script=script, value=value):
                    status, result = self.run_cli(script, value)
                    self.assertEqual(status, 1)
                    self.assertTrue(result['error'])

    def test_single_character_given_name_keeps_existing_grade_filter(self):
        status, result = self.run_cli('suggest.py', '王', '--chars', '1')
        self.assertEqual(status, 0)
        self.assertEqual(result, {'total': 0, 'results': []})
