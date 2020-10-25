import unittest
import bioreflib as bl
import biorefbuild as bb
import os

# os.system('clear')


class TestBioRefine(unittest.TestCase):

    def test_write_json(self):
        bb.write_json()

    def test_user_change(self):
        dicts = bb.call_json()
        output = user_build('ethanol', dicts):
        currentMods = output[1]
        changingMod, newVal = 'process', 'thermochemical'
        bl.user_change(

    def test_get_column(self):
        results=bb.get_column('../covid_hw/test_data.csv',
                                [1, 2],
                                ['Boulder', 'Qolorado'],
                                [0, 4])
        self.assertEqual(results[0], ['2020-03-14', 1])
        self.assertEqual(len(results), 1)


if __name__ == '__main__':
    unittest.main()
