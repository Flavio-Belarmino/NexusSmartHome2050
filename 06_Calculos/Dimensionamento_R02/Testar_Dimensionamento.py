"""Verificacoes independentes de unidades, equilibrios e limites do cenario NEXUS."""
import unittest,math
import Calcular as d
class Dimensionamento(unittest.TestCase):
 def test_coordenacao_e_queda(self):
  for c in d.CIRCUITS:
   with self.subTest(c=c['id']):
    ib=c['p_w_hipotese']/c['fp_hipotese']/c['u_v'];self.assertAlmostEqual(ib,c['ib_a'],places=3)
    self.assertLessEqual(ib,c['disjuntor_a']);self.assertLessEqual(c['disjuntor_a'],c['iz_corrigida_a'])
    self.assertLess(c['queda_total_modelo_pct'],4);self.assertGreater(c['icc_min_modelo_a'],10*c['disjuntor_a'])
 def test_correcao_servico(self):
  c=next(c for c in d.CIRCUITS if c['id']=='C6');self.assertEqual(c['s_fase_mm2'],4)
  queda_anterior=100*2*.0225*22*c['ib_a']/(2.5*127)+d.FEEDER['queda_conservadora_pct'];self.assertGreater(queda_anterior,4)
 def test_balanceamento(self):
  self.assertEqual(len(d.CIRCUITS),20);self.assertLess(max(d.IP.values()),100);self.assertLess(max(d.IP.values())-min(d.IP.values()),2)
  self.assertGreater(d.FEEDER['Iz_a'],100);self.assertLess(d.FEEDER['ocupacao_pct'],40)
 def test_energia_quente(self):
  self.assertAlmostEqual(d.RES['energia_boiler_kwh'],9.3022222222);self.assertGreater(d.RES_EXP['capacidade_expansao_entre_250_350_l'],d.RES_EXP['expansao_agua_l'])
  self.assertGreaterEqual(d.RES['boiler_l'],d.RES['agua_quente_necessaria_l_dia'])
 def test_rede_agua(self):
  self.assertAlmostEqual(sum(p['AF_ls']+p['AQ_ls'] for p in d.FIXTURES),1.15)
  self.assertAlmostEqual(sum(p['NP_ls'] for p in d.FIXTURES),.3)
  for p in d.PRESSURES:self.assertGreaterEqual(p['pressao_disponivel_kpa'],p['pressao_min_especificar_kpa'])
 def test_darcy_unidades(self):
  v,re,f,hf=d.darcy(1,25,10);self.assertAlmostEqual(v,.001/(math.pi*.025**2/4));self.assertGreater(re,2300);self.assertGreater(hf,0)
  self.assertEqual(d.darcy(0,25,10),(0.,0.,0.,0.))
  for args in [(-1,25,10),(1,0,10),(1,25,-1)]:
   with self.assertRaises(ValueError):d.darcy(*args)
 def test_esgoto(self):
  self.assertEqual(sum(p['UHC'] for p in d.FIXTURES),27)
  for r in d.ES:
   self.assertAlmostEqual(r['cota_chegada_m'],r['cota_inicio_m']-r['L_m']*r['declividade_pct']/100,places=4)
   self.assertGreaterEqual(r['cota_chegada_m']+1e-5,d.INVERT_OUT[r['destino']])
  self.assertNotEqual(d.NODES['CG1'],d.h.NODES['CG1']);self.assertEqual(d.NODES['CG1'],(105,310))
 def test_chuva_e_reservacao(self):
  self.assertAlmostEqual(d.STORM['Q_ls'],180*85.756/3600)
  self.assertGreater(d.STORM['capacidade_Manning_ls'],d.STORM['Q_com_margem20_ls'])
  self.assertGreater(d.STORM['coletor_capacidade_ls'],d.STORM['Q_com_margem20_ls'])
  self.assertGreater(d.RES['NP_util_l'],6*d.RES['demanda_NP_l_dia'])
 def test_geracao(self):
  self.assertEqual(d.PV['n_modulos']*d.PV['p_modulo_wp'],d.PV['p_dc_wp'])
  self.assertLess(d.PV['corrente_projeto_a'],d.PV['fuse_gPV_a']);self.assertGreater(d.PV['iz_dc_min_corrigida_a'],d.PV['fuse_gPV_a'])
  self.assertLess(d.PV['queda_dc_pct'],3);self.assertLess(d.PV['queda_ac_pct'],2)
 def test_validacao_integral(self):d.validar()
if __name__=='__main__':unittest.main(verbosity=2)
