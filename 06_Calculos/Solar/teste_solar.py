import unittest
from solar import estimar
class TesteSolar(unittest.TestCase):
    def test_energia_sem_bateria(self):
        d=estimar(1.5,4,.75,1)
        self.assertAlmostEqual(d['energia_solar_wh_dia'],4.5)
        self.assertNotIn('autonomia_bateria_h_estimada',d)
    def test_bateria_somente_com_premissas(self):
        with self.assertRaises(ValueError):estimar(1.5,4,.75,bateria_ah=7)
    def test_autonomia_completa(self):
        d=estimar(1.5,4,.75,3,12,2,.5,.8)
        self.assertAlmostEqual(d['autonomia_bateria_h_estimada'],3.2)
    def test_entradas_invalidas(self):
        for args in ((0,4,.75),(1.5,0,.75),(1.5,25,.75),(1.5,4,0),(1.5,4,1.1),(float('nan'),4,.75),(float('inf'),4,.75)):
            with self.assertRaises(ValueError):estimar(*args)
        with self.assertRaises(ValueError):estimar(1.5,4,.75,carga_w=float('nan'))
if __name__=='__main__':unittest.main()
