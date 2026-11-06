"""Conferencias de unidades e entradas do calculo de volume de chuva."""
import unittest
from Gerar_Estudo import volume_chuva_l, AREA, validar

class CalculoChuva(unittest.TestCase):
    def test_unidades(self):
        self.assertEqual(volume_chuva_l(1,1),1)
        self.assertAlmostEqual(volume_chuva_l(10,AREA),857.56)
        self.assertAlmostEqual(volume_chuva_l(10,AREA,.8,.9),617.4432)
    def test_evento_seco_e_perdas_totais(self):
        self.assertEqual(volume_chuva_l(0,AREA),0)
        self.assertEqual(volume_chuva_l(10,AREA,0,1),0)
        self.assertEqual(volume_chuva_l(10,AREA,1,0),0)
    def test_invalidos(self):
        for args in [(-1,10),(10,0),(10,-1),(10,10,1.1),(10,10,1,-.1),(float('nan'),10),(10,float('inf'))]:
            with self.subTest(args=args),self.assertRaises(ValueError):volume_chuva_l(*args)
    def test_geometria_e_separacao(self):validar()

if __name__=='__main__':unittest.main(verbosity=2)
