import unittest
import bioreflib as bl
import biorefbuild as bb
import os

# os.system('clear')


class TestBioRefine(unittest.TestCase):

    def test_dicts(self):
        # bb.write_json()  # sometimes germ comes out as a biogas side...
        dicts = bb.call_json()
        # print(dicts['MATERIALS']['biogas']['sides'])
        # print(dicts['SIDES']['germ'])
        # print(dicts['SUBSTRATES']['germ'])
        sub_ex = ['glucose', 'methane', 'acetate', 'germ', 'oil']
        mat_ex = ['corn', 'sugar cane', 'poplar', 'wastewater', 'wheat']
        for sub in sub_ex:
            self.assertEqual(dicts.get('SUBSTRATES').get(sub)['name'],
                             sub)
        for mat in mat_ex:
            self.assertEqual(dicts.get('MATERIALS').get(mat)['name'],
                             mat)

    def test_user_build(self):
        dicts = bb.call_json()
        output = bl.user_build('ethanol', dicts)
        currentMods = output[1]
        product = currentMods['product']['name']
        self.assertEqual(product, 'ethanol')

        mainFlow = output[0][0]
        sideFlow1 = output[0][1]
        sideFlow2 = output[0][2]
        # bl.print_bioprocess(mainFlow, sideFlow1, sideFlow2)

        return output

    def test_user_change(self):
        dicts = bb.call_json()
        output = bl.user_build('ethanol', dicts)
        currentMods = output[1]
        product = currentMods['product']['name']
        self.assertEqual(product, 'ethanol')

        print('BASE')
        mainFlow = output[0][0]
        sideFlow1 = output[0][1]
        sideFlow2 = output[0][2]
        bl.print_bioprocess(mainFlow, sideFlow1, sideFlow2)
        print('CASE1')
        changingMod, newVal = 'product', 'shch_fattyacids'
        output = bl.user_change(changingMod, currentMods, newVal, dicts)
        mainFlow = output[0][0]
        sideFlow1 = output[0][1]
        sideFlow2 = output[0][2]
        currentMods = output[1]
        bl.print_bioprocess(mainFlow, sideFlow1, sideFlow2)
        print('CASE2')
        changingMod, newVal = 'product', 'fertilizer'
        output = bl.user_change(changingMod, currentMods, newVal, dicts)
        mainFlow = output[0][0]
        sideFlow1 = output[0][1]
        sideFlow2 = output[0][2]
        currentMods = output[1]
        bl.print_bioprocess(mainFlow, sideFlow1, sideFlow2)
    #     print('pass')
    #     pass
    #     # dicts = bb.call_json()
    #     # output = bl.user_build('ethanol', dicts)
    #     # currentMods = output[1]
    #     # changingMod, newVal = 'process', 'anaerobic_ecoli'
    #
    # def test_get_column(self):
    #     results = bb.get_column('../covid_hw/test_data.csv',
    #                             [1, 2],
    #                             ['Boulder', 'Qolorado'],
    #                             [0, 4])
    #     self.assertEqual(results[0], ['2020-03-14', 1])
    #     self.assertEqual(len(results), 1)


if __name__ == '__main__':
    unittest.main()
