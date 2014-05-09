import sys
import unittest

sys.path.insert(0, "../src/build")
import addonconf

class AddonConfModuleTestCase(unittest.TestCase):
    def test_load(self):
        # act
        config = addonconf.load("configs/config.json")

        # assert
        self.assertEqual(config, None, "Wrong return value for not exists config")

    def test_load2(self):
        # act
        config = addonconf.load("configs/config.json.1")

        # assert
        self.assertEqual(config, None, "Wrong return value for unvalide config")

    def test_load3(self):
        # arrange
        correct_config = {'version': '0.1', 'xpi': {'theme': 'firefox-theme-test.xpi', 'package': 'firefox-test-@VERSION@.xpi', 'extension': 'firefox-extension-test.xpi'}, 'max-version': '31.0a1', 'directory-structure': {'shared-dir': 'chrome'}, 'min-version': '29.0'}

        # act
        config = addonconf.load("configs/config.json.2")

        # assert
        self.assertEqual(config, correct_config, "Uncorrect load config")

if __name__ == '__main__':
    unittest.main()

