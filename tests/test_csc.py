__author__ = 'yairgrosu'

import unittest
import yaml
from csc.csc import CascadingConfig
from csc.yamlcsc import YamlCascadingConfig

refText = """
src:
  aa:
    bb: [12, 1.5, dont]
    ph: aaa
  cc: this is a cc just for nada
dest:
  based_on: src
dest2:
  based_on:
    - src
    - [ !Add {  path: aa/bb, values: [ lalala, ooo] }, !Del {  aa/bb: [12, lalala, dont] }, !Del {  path: cc } ]
"""

yamlRefText = """
---
src:
  aa:
    bb: [12, 1.5, dont]
    ph: aaa
  cc: this is a cc just for nada
dest:
  based_on: src
dest2:
  based_on:
    - src
    - [ !Add {  path: aa/bb, values: [ lalala, ooo] }, !Del {  aa/bb: [12, lalala, dont] }, !Del {  path: cc } ]
"""


class TestCscOps(unittest.TestCase):

    def test_load_basic(self):
        items = yaml.load(refText)
        cscdata = CascadingConfig()
        cscdata.add_dicts(items)

        dest = cscdata.get_dict('dest')
        self.assertIsNotNone(dest, "should not be none")
        self.assertIn(12, dest['aa']['bb'], 'path /aa/bb should  have 12')
        self.assertEqual(dest['aa']['ph'], 'aaa', 'path /aa/ph should be aaa')

    def test_load_complex(self):
        items = yaml.load(refText)
        cscdata = CascadingConfig()
        cscdata.add_dicts(items)

        dest = cscdata.get_dict('dest2')
        self.assertIsNotNone(dest, "should not be none")
        self.assertNotIn(12, dest['aa']['bb'], 'path /aa/bb should NOT have 12')
        self.assertIn('ooo', dest['aa']['bb'], 'path /aa/bb should  have "ooo"')

        self.assertNotIn('cc', dest, 'path / should NOT have "cc"')
        self.assertEqual(dest['aa']['ph'], 'aaa', 'path /aa/ph should be aaa')

    def test_yaml_load(self):
        cscdata = YamlCascadingConfig(text=yamlRefText)

        dest = cscdata.get_dict('dest2')
        self.assertIsNotNone(dest, "should not be none")
        self.assertNotIn(12, dest['aa']['bb'], 'path /aa/bb should NOT have 12')
        self.assertIn('ooo', dest['aa']['bb'], 'path /aa/bb should  have "ooo"')

        self.assertNotIn('cc', dest, 'path / should NOT have "cc"')
        self.assertEqual(dest['aa']['ph'], 'aaa', 'path /aa/ph should be aaa')

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestCscOps)
    unittest.TextTestRunner(verbosity=2).run(suite)