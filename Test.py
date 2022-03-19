import unittest

from DataBase import DataBase

class TestDataBase(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.dataBase=DataBase()

    def test_save_and_load(self):
        self.dataBase.Na={"2022/01/02 23:20:11":0.123}
        self.dataBase.K={"2022/01/02 23:20:11":0.123}
        self.dataBase.Glucose={"2022/01/02 23:20:11":0.123}
        self.dataBase.CRP={"2022/01/02 23:20:11":0.123}
        self.dataBase.ILBeta={"2022/01/02 23:20:11":0.123}
        self.dataBase.save()
        self.dataBase.load()
        self.assertEqual(self.dataBase.getNa(),{"2022/01/02 23:20:11":0.123},"Wrong Na")
        self.assertEqual(self.dataBase.getK(),{"2022/01/02 23:20:11":0.123},"Wrong K")
        self.assertEqual(self.dataBase.getGlucose(),{"2022/01/02 23:20:11":0.123},"Wrong Glucose")
        self.assertEqual(self.dataBase.getCRP(),{"2022/01/02 23:20:11":0.123},"Wrong CRP")
        self.assertEqual(self.dataBase.getILBeta(),{"2022/01/02 23:20:11":0.123},"Wrong ILBeta")

    def test_sort(self):
        test={"2022/11/02 23:20:11":0.123,"2021/11/02 23:20:11":0.123,"2021/01/02 23:20:11":0.123}
        self.dataBase.Na=test
        self.dataBase.K=test
        self.dataBase.Glucose=test
        self.dataBase.CRP=test
        self.dataBase.ILBeta=test
        self.dataBase.sort()
        self.assertEqual(self.dataBase.getNa(),{"2021/01/02 23:20:11":0.123,"2021/11/02 23:20:11":0.123,"2022/11/02 23:20:11":0.123},"Wrong Na")
        self.assertEqual(self.dataBase.getK(),{"2021/01/02 23:20:11":0.123,"2021/11/02 23:20:11":0.123,"2022/11/02 23:20:11":0.123},"Wrong K")
        self.assertEqual(self.dataBase.getGlucose(),{"2021/01/02 23:20:11":0.123,"2021/11/02 23:20:11":0.123,"2022/11/02 23:20:11":0.123},"Wrong Glucose")
        self.assertEqual(self.dataBase.getCRP(),{"2021/01/02 23:20:11":0.123,"2021/11/02 23:20:11":0.123,"2022/11/02 23:20:11":0.123},"Wrong CRP")
        self.assertEqual(self.dataBase.getILBeta(),{"2021/01/02 23:20:11":0.123,"2021/11/02 23:20:11":0.123,"2022/11/02 23:20:11":0.123},"Wrong ILBeta")
    
    def test_update(self):
        test={"2022/11/02 23:20:11":0.123,"2021/11/02 23:20:11":0.123,"2021/01/02 23:20:11":0.123}
        self.dataBase.Na=test
        self.dataBase.K=test
        self.dataBase.Glucose=test
        self.dataBase.CRP=test
        self.dataBase.ILBeta=test
        self.dataBase.update()
        self.assertEqual(self.dataBase.getNa(),{"2022/11/02 23:20:11":0.123},"Wrong Na")
        self.assertEqual(self.dataBase.getK(),{"2022/11/02 23:20:11":0.123},"Wrong K")
        self.assertEqual(self.dataBase.getGlucose(),{"2022/11/02 23:20:11":0.123},"Wrong Glucose")
        self.assertEqual(self.dataBase.getCRP(),{"2022/11/02 23:20:11":0.123},"Wrong CRP")
        self.assertEqual(self.dataBase.getILBeta(),{"2022/11/02 23:20:11":0.123},"Wrong ILBeta")

unittest.main()        
