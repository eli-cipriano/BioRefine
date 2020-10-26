import unittest
import bioreflib as bl
import os

# os.system('clear')


class TestBioRefine(unittest.TestCase):

    def test_dicts(self):
        # bl.write_json()  # sometimes germ comes out as a biogas side...
        dicts = bl.call_json()
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
        dicts = bl.call_json()
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
        dicts = bl.call_json()
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
        changingMod, newVal = 'product', 'fertilizer'
        output = bl.user_change(changingMod, currentMods, newVal, dicts)
        mainFlow = output[0][0]
        sideFlow1 = output[0][1]
        sideFlow2 = output[0][2]
        currentMods = output[1]
        bl.print_bioprocess(mainFlow, sideFlow1, sideFlow2)
        print('CASE2')
        changingMod, newVal = 'product', 'cooking_oil'
        output = bl.user_change(changingMod, currentMods, newVal, dicts)
        mainFlow = output[0][0]
        sideFlow1 = output[0][1]
        sideFlow2 = output[0][2]
        currentMods = output[1]
        bl.print_bioprocess(mainFlow, sideFlow1, sideFlow2)

    def test_get_column(self):
        results = bl.get_column('../covid_hw/test_data.csv',
                                query_column=[1, 2],
                                query_value=['Boulder', 'Qolorado'],
                                result_column=[0, 4])
        self.assertEqual(results[0], ['2020-03-14', 1])
        self.assertEqual(len(results), 1)

    def test_build_subprods(self):
        processes = bl.build_processes()
        # os.system('clear')
        a = processes['methanotroph']['subprods']
        key = list(a.keys())[0]
        print(key)
        self.assertEqual(a[key]['strains'][0][0], 'wt')


if __name__ == '__main__':
    unittest.main()
