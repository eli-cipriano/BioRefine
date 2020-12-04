import unittest
import bioreflib as brf
import os

# os.system('clear')


class TestBioRefine(unittest.TestCase):

    def test_dicts(self):
        brf.write_json()  # sometimes germ comes out as a biogas side...
        dicts = brf.call_json()
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
        output = brf.user_build('ethanol')
        currentMods = output[1]
        product = currentMods['product']['name']
        self.assertEqual(product, 'ethanol')

        mainFlow = output[0][0]
        sideFlow1 = output[0][1]
        sideFlow2 = output[0][2]
        # brf.print_bioprocess(mainFlow, sideFlow1, sideFlow2)

        return output

    def test_user_change(self):
        output = brf.user_build('ethanol')
        currentMods = output[1]
        product = currentMods['product']['name']
        self.assertEqual(product, 'ethanol')

        print('BASE')
        mainFlow = output[0][0]
        sideFlow1 = output[0][1]
        sideFlow2 = output[0][2]
        brf.print_bioprocess(mainFlow, sideFlow1, sideFlow2)
        print('CASE1')
        changingMod, newVal = 'material', 'sugar cane'
        output = brf.user_change(changingMod, newVal, currentMods)
        mainFlow = output[0][0]
        sideFlow1 = output[0][1]
        sideFlow2 = output[0][2]
        currentMods = output[1]
        brf.print_bioprocess(mainFlow, sideFlow1, sideFlow2)
        print('CASE2')
        changingMod, newVal = 'sub1', 'methane'
        output = brf.user_change(changingMod, newVal, currentMods)
        mainFlow = output[0][0]
        sideFlow1 = output[0][1]
        sideFlow2 = output[0][2]
        currentMods = output[1]
        brf.print_bioprocess(mainFlow, sideFlow1, sideFlow2)
        print('CASE3')
        changingMod, newVal = 'product', 'methanol'
        output = brf.user_change(changingMod, newVal, currentMods)
        mainFlow = output[0][0]
        sideFlow1 = output[0][1]
        sideFlow2 = output[0][2]
        currentMods = output[1]
        brf.print_bioprocess(mainFlow, sideFlow1, sideFlow2)

    def test_get_column(self):
        results = brf.get_column('../covid_hw/test_data.csv',
                                 query_column=[1, 2],
                                 query_value=['Boulder', 'Qolorado'],
                                 result_column=[0, 4])
        self.assertEqual(results[0], ['2020-03-14', 1])
        self.assertEqual(len(results), 1)

    def test_build_subprods(self):
        processes = brf.build_processes()
        # os.system('clear')
        a = processes['methanotroph']['subprods']
        key = list(a.keys())[0]
        self.assertEqual(a[key]['strains'][0][0], 'wt')


if __name__ == '__main__':
    unittest.main()
