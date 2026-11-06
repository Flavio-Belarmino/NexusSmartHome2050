"""NEXUS | ExpoTech - dimensionamento esquematico de um cenario academico.
Sem medidas de campo: hipoteses estao explicitadas e sao verificadas por codigo.
Nao e projeto de execucao/ligacao de residencia nem circuito de potencia da maquete.
"""
from pathlib import Path
import json,csv,math,cmath,itertools,importlib.util
OUT=Path(__file__).resolve().parent;REPO=OUT.parents[1]
def loadmod(name,path):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
h=loadmod('hydro_base',REPO/'03_Hidraulica/Residencial_R01/Gerar_Estudo.py')
e=loadmod('electric_base',REPO/'02_Eletrica/Residencial_R01/Gerar_Previsao.py')
F=20;RHO=.0225;IZ={1.5:17.5,2.5:24,4:32,6:41,10:57,16:76,25:101,35:125,50:151}
# Potencias de estudo, nao fichas de modelos comprados. Comprimentos de projeto de ida.
BASE=[('C1','Iluminacao social',620,1,127,24,1.5,10),('C2','Iluminacao intima',620,1,127,26,1.5,10),('C3','TUG social/circulacao/apoio',1000,1,127,28,2.5,16),('C4','TUG quartos',800,1,127,30,2.5,16),('C5','TUG cozinha',1900,1,127,14,2.5,16),('C6','TUG servico',1900,1,127,22,4,16),('C7','TUG banhos',1200,1,127,25,2.5,16),('C8','Cooktop inducao',7400,1,220,14,6,40),('C9','Forno eletrico',3000,1,220,15,2.5,16),('C10','Micro-ondas',1500,.95,127,14,2.5,16),('C11','Geladeira',350,.85,127,14,2.5,10),('C12','Lavadora',1000,.9,127,22,2.5,16),('C13','Aquecedor central 200 L',3000,1,220,20,2.5,16),('C14','Ar-condicionado quarto 1',900,.95,220,25,2.5,10),('C15','Ar-condicionado quarto 2',900,.95,220,30,2.5,10),('C16','Depurador',200,.8,127,15,2.5,10),('C17','Central rede/automacao',400,.9,127,27,2.5,10),('C18','Portao - reserva',500,.8,220,35,2.5,10),('C19','Pressurizacao NP (1 ativa)',370,.75,220,28,2.5,10),('C20','Pressurizacao AF (1 ativa)',1100,.8,220,25,2.5,10)]
# TV e pequenos aparelhos ficam nas TUG; C17 reserva central com margem de estudo.
CIRCUITS=[]
for id,use,p,pf,v,l,s,br in BASE:
 va=p/pf;ib=va/v;du=2*RHO*l*ib/s;icc=v/((.1 if v==127 else .2)+2*RHO*5/50+2*RHO*l/s)
 CIRCUITS.append({'id':id,'uso':use,'p_w_hipotese':p,'fp_hipotese':pf,'s_va':round(va,3),'u_v':v,'ib_a':round(ib,4),'L_ida_m':l,'fase':'','s_fase_mm2':s,'s_neutro_mm2':s if v==127 else 0,'s_pe_mm2':s,'iz_corrigida_a':IZ[s],'disjuntor_a':br,'curva':'C','DR':'A, 30 mA','icn_ka':10,'queda_terminal_pct':round(100*du/v,4),'icc_min_modelo_a':round(icc,2),'limite_i2t_a2s':round((115*s)**2),'eletroduto':'DE25, DI>=19mm' if s==6 else 'DE20, DI>=15,5mm','estado':'DIMENSIONADO NO CENARIO'})
# Equilibrio com correntes fasoriais. Circuitos 220V entre fases.
V={ph:127*cmath.exp(1j*math.radians(a)) for ph,a in [('A',0),('B',-120),('C',120)]}
I={ph:0j for ph in V}
for c in sorted(CIRCUITS,key=lambda c:-c['s_va']):
 opts=list(V) if c['u_v']==127 else ['AB','BC','CA'];best=None
 for ph in opts:
  currents=I.copy();ss=complex(c['p_w_hipotese'],c['p_w_hipotese']*math.tan(math.acos(c['fp_hipotese'])))
  if len(ph)==1:currents[ph]+=(ss/V[ph]).conjugate()
  else:
   a,b=ph;j=(ss/(V[a]-V[b])).conjugate();currents[a]+=j;currents[b]-=j
  score=(max(abs(j) for j in currents.values()),sum(abs(j)**2 for j in currents.values()))
  if best is None or score<best[0]:best=(score,ph,currents)
 c['fase']=best[1];I=best[2]
TOTAL_VA=sum(c['s_va'] for c in CIRCUITS);TOTAL_W=sum(c['p_w_hipotese'] for c in CIRCUITS)
IP={k:abs(v) for k,v in I.items()};NEUTRAL=abs(sum(I.values()))
# Alimentador B1, 3 carregados 134A para 50mm2; 0,80 e margem adotada para neutral/harmonicas.
FEEDER={'L_m':5,'fase_neutro_mm2':50,'PE_mm2':25,'In_a':100,'Iz_base_a':134,'margem_adotada':.8,'Iz_a':107.2,'Id_max_a':max(IP.values()),'neutro_fundamental_a':NEUTRAL,'queda_conservadora_pct':100*2*RHO*5*100/(50*127),'eletroduto':'DE63 DI>=50mm','ocupacao_pct':100*(4*13.8**2+10.5**2)/(50**2),'Icc_max_QD_hipotese_ka':6.35,'Z_fonte_max_ohm':.1}
FEEDER['neutro_limite_hipotese_h3_a']=NEUTRAL+.15*sum(IP.values())
EL_HARMONICS='Modelo senoidal com FP de deslocamento; hipotese adicional de3a harmonica<=15% da fundamental por fase. Neutro verificado por soma limite, sem reduzir secao.'
for c in CIRCUITS:c['queda_total_modelo_pct']=round(c['queda_terminal_pct']+FEEDER['queda_conservadora_pct'],4)
# Equipamentos adicionais nao se somam novamente as tomadas de previsao? Aqui somam: conservador.
EL_NOTES={'carga':'TUG previstas e circuitos exclusivos somados integralmente; nenhum fator de demanda. Nao somar de novo TV/pequenos aparelhos nas TUG.','metodo':'B1, cobre/PVC70, ar30C; um circuito por eletroduto, sem agrupamento/isolacao termica; se mudar, recalcular.','alimentacao':'Cenario trifasico127/220V60Hz, TT, entrada100A. Nao e fornecimento aprovado pela concessionaria.','comprimentos':'Comprimentos de ida adotados como envelope de projeto; conferir se rotas/instalacao permanecem dentro deles.','protecao':'RCBO por circuito, polos conforme quadro,10kA,30mA tipoA; curvaC. Motopartida/inverter e I2t exigem fabricante compativel.','neutro':'N separado de PE, sem neutros compartilhados apos RCBO; PE continuo.','TT':'BEP, equipotencializacao principal/suplementar. RA objetivo<=20ohm: RA*0,03<=0,6V; RA nao foi medida.','DPS':'TipoII 3+1 proprio paraTT127/220, Uc175V F-N, In>=20kA Imax>=40kA Up<=1,5kV. N-PE por centelhador; coordenar respaldo100A/distancias conforme fabricante.','harmonicas':EL_HARMONICS,
'curto':'Zfonte max0,1ohm e Iccmax6,35kA hipoteses. Exigir Icn10kA e energia passante<=k2S2 por circuito; a verificacao I2t de produto nao esta feita.','quadros':'Prever quadro com capacidade fisica >=72 modulos DIN, recalcular pelo dispositivo selecionado; esta escolha nao fecha dissipacao termica.','solar':'6modulos550Wp,2MPPT independentes,3modulos/MPPT; on-grid3kW220V. Correntes/Voc sao hipoteses de compatibilidade a conferir por ficha.','maquete':'Nenhuma destas tensoes/cargas e instrucao de ligacao da maquete DC.'}
PV={'n_modulos':6,'p_modulo_wp':550,'p_dc_wp':3300,'p_ac_w':3000,'serie_por_mppt':3,'mppt':2,'vmp_mod_v':42,'voc_mod_v':50,'isc_mod_a':14.2,'imp_mod_a':550/42,'temperatura_min_hipotese_c':10,'coef_voc_por_c':-.003,'voc_string_corrigida_v':3*50*(1+.003*(25-10)),'vmp_string_v':126,'corrente_projeto_a':1.25*14.2,'cabo_dc_mm2':6,'iz_dc_min_corrigida_a':25,'L_dc_ida_m':15,'fuse_gPV_a':20,'isolador_dc':'2P32A600Vcc por MPPT','DPS_dc':'TipoII PV600V, conforme inversor','inversor_requisito':'2MPPT independentes; MPPT90-450V; Vccmax>=600V; Ientrada>=15A e Isc_admissivel>=18A porMPPT; certificacao/anti-ilhamento e protecao residual compativeis','circuito_ac':'C21: 2P C20A, DRtipoB30mA bidirecional conforme inversor; 2F+PE4mm2,20m,Iz32A; Icn10kA','queda_dc_pct':100*2*.0225*15*(550/42)/(6*126),'queda_ac_pct':100*2*.0225*20*(3000/220)/(4*220),'limite_geracao':'Sem subtrair PV da demanda; nao pressupor geracao durante falta de rede.','area_modulos_m2':6*2.3*1.15}
# ------------------ HIDRAULICA ------------------
# Qnominal de projeto escolhido, sem simultaneidade estatistica.
FIX=[('H01',.10,.10,0,.6,50,3),('H02',.05,.05,0,.6,40,1),('H03',0,0,.15,.2,100,6),('H04',.075,.075,0,2.2,40,2),('H05',.05,.05,0,.6,40,1),('H06',0,0,.15,.2,100,6),('H07',.075,.075,0,2.2,40,2),('H08',.25,0,0,1.0,50,3),('H09',.20,0,0,1.0,50,3)]
FIXTURES=[]
for id,af,aq,np,z,dn,uhc in FIX:
 p=h.P[id];FIXTURES.append({'id':id,'uso':p['aparelho'],'x_maquete_mm':p['x_maquete_mm'],'y_maquete_mm':p['y_maquete_mm'],'AF_ls':af,'AQ_ls':aq,'NP_ls':np,'z_conexao_m':z,'ES_DN_mm':dn,'UHC':uhc})
FP={p['id']:p for p in FIXTURES}
def darcy(q_ls,di_mm,L_m):
 if q_ls<0 or di_mm<=0 or L_m<0:raise ValueError('Parametros hidraulicos invalidos')
 if q_ls==0:return (0.,0.,0.,0.)
 d=di_mm/1000;q=q_ls/1000;v=q/(math.pi*d*d/4);re=v*d/1e-6
 f=64/re if re<2300 else .25/(math.log10(1.5e-6/(3.7*d)+5.74/re**.9)**2)
 hf=f*(1.5*L_m)/d*v*v/(2*9.80665) # Leq=1,5L: provisao explicita de 50% para conexoes.
 return v,re,f,hf
SEG=[]
def seg(id,net,fr,to,q,de,di,pts,z1,z2):
 L=sum(math.dist(a,b) for a,b in zip(pts,pts[1:]))*.02+abs(z2-z1);v,re,f,hf=darcy(q,di,L)
 r={'id':id,'rede':net,'origem':fr,'destino':to,'Q_ls':q,'DE_mm':de,'DI_min_calculo_mm':di,'vertices_maquete_mm':pts,'z1_m':z1,'z2_m':z2,'L_real_m':round(L,4),'Leq_m':round(1.5*L,4),'v_ms':round(v,4),'f':round(f,5),'hf_m':round(hf,5)};SEG.append(r);return id
# AF de reservatorio atmosferico no piso: conjunto com duas bombas alternadas, uma ativa.
seg('AF0','AF','PAF','CAF',1.15,40,35.2,[(330,-50),(330,110)],.3,2.4)
seg('AFN','AF','PAF','ReposicaoNP',.30,20,17,[(330,-50),(700,-50)],.3,1.2)
seg('AFL','AF','CAF','Esquerda',.225,25,21.6,[(330,110),(202,110)],2.4,2.4)
seg('AFR','AF','CAF','Direita',.675,32,27.8,[(330,110),(580,110)],2.4,2.4)
seg('AFA','AF','Direita','AQ1',.35,25,21.6,[(455,110),(455,60)],2.4,1.0)
seg('AQT','AQ','AQ1','AQcentro',.35,28,22,[(455,60),(455,101)],1.0,2.4)
seg('AQL','AQ','AQcentro','AQesquerda',.225,28,22,[(455,101),(202,101)],2.4,2.4)
seg('AQR','AQ','AQcentro','AQdireita',.125,28,22,[(455,101),(580,101)],2.4,2.4)
seg('NP0','NP','PNP','NPbarrilete',.30,25,21.6,[(720,-18),(235,-18)],.3,.3)
for p in FIXTURES:
 x,y=p['x_maquete_mm'],p['y_maquete_mm'];z=p['z_conexao_m']
 if p['AF_ls']:
  bx=202 if p['id']=='H01' else x
  seg('AF_'+p['id'],'AF','Barrilete',p['id'],p['AF_ls'],20,17,[(bx,110),(bx,y),(x,y)],2.4,z)
 if p['AQ_ls']:
  bx=205 if p['id']=='H01' else x+3
  seg('AQ_'+p['id'],'AQ','BarrileteAQ',p['id'],p['AQ_ls'],22,17.5,[(bx,101),(bx,y),(x,y)],2.4,z)
 if p['NP_ls']:seg('NP_'+p['id'],'NP','NPbarrilete',p['id'],p['NP_ls'],20,17,[(x,-18),(x,y)],.3,z)
SS={r['id']:r for r in SEG};PRESSURES=[]
for p in FIXTURES:
 for net in ('AF','AQ','NP'):
  if not p[net+'_ls']:continue
  id=p['id'];left=id in ('H01','H02','H04')
  path=['AF0']+(['AFL'] if left else (['AFR'] if id!='H08' else []))+['AF_'+id] if net=='AF' else ['AF0','AFR','AFA','AQT','AQL' if left else 'AQR','AQ_'+id] if net=='AQ' else ['NP0','NP_'+id]
  hf=sum(SS[s]['hf_m'] for s in path);extra=70 if net=='AQ' else 25 if net=='NP' else 0;source=150 if net=='NP' else 250
  pressure=source-9.80665*(p['z_conexao_m']-.3+hf)-extra
  PRESSURES.append({'aparelho':id,'rede':net,'caminho':path,'hf_total_m':round(hf,4),'perdas_equipamentos_kpa':extra,'pressao_disponivel_kpa':round(pressure,3),'pressao_min_especificar_kpa':50 if net=='NP' else 100,'resultado':'ATENDE_CENARIO' if pressure>=(50 if net=='NP' else 100) else 'REVER'})
# Esgoto revisto: pia segue pela cozinha ao exterior; rota anterior sob sala retirada.
NODES={'CG1':(105,310),'CS1':(252,50),'CS2':(544,59),'CI1':(285,-60),'CI2':(520,-60),'CI3':(730,310),'CIE':(730,-60),'DS1':(760,-60),'VT1':(292,72),'VT2':(578,72),'VK':(202,186),'VS1':(335,25),'VS2':(470,25)}
ES=[]
def es(id,fr,to,dn,i,uhc,pts,zstart):
 L=sum(math.dist(a,b) for a,b in zip(pts,pts[1:]))*.02;end=zstart-L*i
 ES.append({'id':id,'origem':fr,'destino':to,'DN_mm':dn,'declividade_pct':i*100,'UHC':uhc,'vertices_maquete_mm':pts,'L_m':round(L,3),'cota_inicio_m':zstart,'cota_chegada_m':round(end,5)})
es('ES_H01','H01','CG1',50,.02,3,[(194,186),(105,186),(105,310)],-.10)
es('ES_CG','CG1','CI3',100,.01,3,[NODES['CG1'],NODES['CI3']],-.25)
es('ES_CI3','CI3','CIE',100,.01,3,[NODES['CI3'],NODES['CIE']],-.375)
for id,cs in [('H02','CS1'),('H04','CS1'),('H05','CS2'),('H07','CS2')]:
 p=FP[id];x,y=p['x_maquete_mm'],p['y_maquete_mm'];cx,cy=NODES[cs];es('ES_'+id,id,cs,p['ES_DN_mm'],.02,p['UHC'],[(x,y),(x,cy),(cx,cy)],-.03)
for rid,cs in [('H10','CS1'),('H11','CS2')]:
 pp=h.P[rid];x,y=pp['x_maquete_mm'],pp['y_maquete_mm'];cx,cy=NODES[cs];es('ES_'+rid,rid,cs,40,.02,0,[(x,y),(cx,y),(cx,cy)],-.03)
# Ralos nao acrescentam UHC: recebem agua dos mesmos usos; fecho hidrico na caixa, sem dupla sifonagem.
for cs,ci in [('CS1','CI1'),('CS2','CI2')]:
 x,y=NODES[cs];cx,cy=NODES[ci];es('ES_'+cs,cs,ci,75,.02,3,[(x,y),(x,cy),(cx,cy)],-.12)
for id,ci in [('H03','CI1'),('H06','CI2'),('H08','CI2'),('H09','CI2')]:
 p=FP[id];x,y=p['x_maquete_mm'],p['y_maquete_mm'];cx,cy=NODES[ci];es('ES_'+id,id,ci,p['ES_DN_mm'],.01 if p['ES_DN_mm']>=100 else .02,p['UHC'],[(x,y),(x,cy),(cx,cy)],-.12)
es('ES_CI1','CI1','CI2',100,.01,9,[NODES['CI1'],NODES['CI2']],-.30)
es('ES_CI2','CI2','CIE',100,.01,24,[NODES['CI2'],NODES['CIE']],-.40)
es('ES_OUT','CIE','DS1',100,.01,27,[NODES['CIE'],NODES['DS1']],-.50)
INVERT_OUT={'CG1':-.25,'CS1':-.12,'CS2':-.12,'CI1':-.30,'CI2':-.40,'CI3':-.375,'CIE':-.50,'DS1':-.60}
VENT=[{'id':'V1','origem':'CS1','DN_mm':50,'terminal':'VT1','L_limite_projeto_m':10,'topo_m':5.30},{'id':'V2','origem':'CS2','DN_mm':50,'terminal':'VT2','L_limite_projeto_m':10,'topo_m':5.30},{'id':'V3','origem':'H01','DN_mm':50,'terminal':'VK','L_limite_projeto_m':10,'topo_m':5.30},{'id':'V4','origem':'H08','DN_mm':50,'terminal':'VS1','L_limite_projeto_m':10,'topo_m':5.30},{'id':'V5','origem':'H09','DN_mm':50,'terminal':'VS2','L_limite_projeto_m':10,'topo_m':5.30}]
RES_EXP={'volume_boiler_l':200,'rho20_kgm3':998.2,'rho60_kgm3':983.2,'expansao_agua_l':200*(998.2/983.2-1),'vaso_expansao_potavel_l':18,'pre_carga_manometrica_kpa':250,'pressao_operacao_limite_kpa':350,'capacidade_expansao_entre_250_350_l':18*(1-350/450),'alivio_max_kpa':400,'nota':'Grupo de seguranca, alivio, vaso e PMTA dependem de conjunto homologado pelo fabricante; sem bloqueio entre boiler e seguranca.'}
VENT+= [{'id':'V6','origem':'H03','DN_mm':50,'terminal':'VT1','L_limite_projeto_m':10,'topo_m':5.30},{'id':'V7','origem':'H06','DN_mm':50,'terminal':'VT2','L_limite_projeto_m':10,'topo_m':5.30}]
# VTs independentes, incluindo conexao das bacias a ventilar antes da CI; total local<=17UHC.
# Ventilacao de bacias DN50 e tomadas a <=0,8m dos desconectores; nao e linha de agua.
RES={'pessoas':4,'q_total_lpd':150,'demanda_total_l_dia':600,'descargas_por_pessoa_dia':5,'volume_descarga_l':6,'demanda_NP_l_dia':120,'potavel_rotina_l_dia':480,'potavel_backup_l_dia':600,'reservatorio_AF_nominal_l':1000,'AF_util_l':800,'AF_reserva_dias_backup':800/600,'cisterna_NP_nominal_l':1000,'NP_util_l':800,'NP_alvo_dias_sem_chuva':6,'NP_dias_com_cheio_sem_entrada':800/120,'boiler_l':200,'boiler_kw':3,'T_fria_C':20,'T_acum_C':60,'T_uso_C':40,'T_limite_seguranca_C':45,'agua_misturada_por_pessoa_dia_l':50,'agua_quente_necessaria_l_dia':100,'energia_boiler_kwh':200*4.186*40/3600,'tempo_recuperacao_h':200*4.186*40/(3600*3),'pressurizacao_AF':'2 bombas alternadas (1 ativa), Q>=1,45L/s e H>=28mca; potencia eletrica de estudo1,1kW por bomba, intertravamento','pressurizacao_NP':'2 bombas alternadas (1 ativa), Q>=0,30L/s e H>=18mca; estudo370W por bomba','pressao_AF_kpa':250,'pressao_NP_kpa':150,'pressao_max_controle_kpa':300,'AQ_grupo_e_misturador_perda_kpa':70,'isolamento_AQ':'CPVC classe de servico compativel60C/600kPa; isolamento termico20mm como premissa; dimensionar suportes/dilatacao','seguranca_boiler':'Termostato60C, limitador termico independente, misturadores termostaticos40C com limite45C; alivio, expansao e ausencia de bloqueio conforme fabricante; conjunto certificado','reposicao_NP':'AF por valvula de boia/solenoide com separacao atmosferica minima de estudo50mm acima extravasor para bocal<=20mm, acesso e identificacao; ensaio contra retorno','tratamento_chuva':'Tela, desvio inicial, sedimentacao/filtracao e desinfeccao dimensionada por vazao/qualidade; qualidade nao comprovada; sem uso corporal/alimentos','aplicacao':'Reservatorios e bombas no nivel do solo, em area tecnica proposta; apoio estrutural e lote a conferir'}
# Calha semicircular DE200, lamina80mm e i0,5%; Manning e dimensoes hidraulicas de projeto.
r=.1;depth=.08;angle=2*math.acos((r-depth)/r);Ac=r*r/2*(angle-math.sin(angle));Pr=r*angle
MANNING=(1/.011)*Ac*(Ac/Pr)**(2/3)*(.005**.5)*1000
STORM={'area_m2':h.AREA,'intensidade_hipotese_mm_h':180,'Q_ls':h.AREA*180/3600,'Q_com_margem20_ls':1.2*h.AREA*180/3600,'calha_semi_DE_mm':200,'lamina_max_mm':80,'declividade_pct':.5,'capacidade_Manning_ls':MANNING,'comprimento_calha_total_m':14.35,'duas_aguas_calha':'Do ponto alto central para duas saidas; comprimento de cada meia-calha7,175m, queda35,875mm','n_descidas':2,'DN_descidas_mm':100,'Q_por_descida_ls':h.AREA*180/3600/2,'area_por_descida_m2':h.AREA/2,'area_condutor_cm2':math.pi*5**2,'criterio_descida':'Preselecao pela regra simplificada do Manual Tigre1cm2/m2:78,54cm2>42,878m2/descida; confirmar abaco NBR10844 e bocais no projeto executivo','coletor_pluvial_DN_mm':150,'coletor_declividade_pct':1,'coletor_capacidade_ls':(1/.011)*(math.pi*.15**2/8)*(.15/4)**(2/3)*(.01**.5)*1000,'desvio_inicial_hipotese_mm':2,'desvio_l':2*h.AREA,'reservatorio_desvio_adotado_l':200,'exemplo_evento_10mm_l_apos_desvio':max(0,10*h.AREA*.8*.9-2*h.AREA),'clima':'180mm/h e premissa, nao IDF medida/validada. Series locais/recorrencia, extravasor de seguranca e destino pluvial exigem verificacao antes da execucao.'}

PV['coef_vmp_por_c']=-.0035
PV['temperatura_max_celula_hipotese_c']=70
PV['vmp_string_quente_v']=126*(1-.0035*(70-25))
PV['fusivel_admissivel_modulo_min_a']=20
RES['tratamento_NP']='Tela/desvio com capacidade>=5,146L/s; filtracao/desinfeccao de saidaNP validadas para>=1,10m3/h, perda total<=25kPa, intertravamento por falha. Qualidade e manutencao conforme usoNP; sem comprovacao laboratorial.'

def validar():
 for c in CIRCUITS:
  assert c['ib_a']<=c['disjuntor_a']<=c['iz_corrigida_a'],c['id']
  assert c['queda_total_modelo_pct']<4,c['id']
  assert c['icc_min_modelo_a']>10*c['disjuntor_a'],c['id']
 assert max(IP.values())<FEEDER['In_a']<=FEEDER['Iz_a'],IP
 assert FEEDER['ocupacao_pct']<40
 assert FEEDER['neutro_limite_hipotese_h3_a']<FEEDER['Iz_a']
 for s in SEG:assert s['v_ms']<2,s['id']
 for p in PRESSURES:assert p['resultado']=='ATENDE_CENARIO',p
 assert RES_EXP['expansao_agua_l']<RES_EXP['capacidade_expansao_entre_250_350_l']
 assert abs(sum(p['AF_ls']+p['AQ_ls'] for p in FIXTURES)-1.15)<1e-8
 assert sum(p['UHC'] for p in FIXTURES)==27
 for r in ES:
  assert r['cota_chegada_m']>=INVERT_OUT.get(r['destino'],-999)-1e-5,r
 assert STORM['capacidade_Manning_ls']>=STORM['Q_com_margem20_ls']
 assert STORM['coletor_capacidade_ls']>STORM['Q_com_margem20_ls']
 assert PV['corrente_projeto_a']<PV['fuse_gPV_a']<PV['iz_dc_min_corrigida_a']
 assert PV['vmp_string_quente_v']>=90
 assert PV['queda_dc_pct']<3 and PV['queda_ac_pct']<2


def csv_write(name,rows):
 keys=list(dict.fromkeys(k for r in rows for k in r))
 with (OUT/name).open('w',encoding='utf-8-sig',newline='') as f:
  w=csv.DictWriter(f,fieldnames=keys,delimiter=';');w.writeheader()
  for r in rows:w.writerow({k:json.dumps(v,ensure_ascii=False) if isinstance(v,(dict,list,tuple)) else v for k,v in r.items()})

def exportar():
 validar()
 for name,rows in [('Circuitos_R02.csv',CIRCUITS),('Hidraulica_Trechos_R02.csv',SEG),('Hidraulica_Pressoes_R02.csv',PRESSURES),('Aparelhos_Hidraulicos_R02.csv',FIXTURES),('Esgoto_Cotas_R02.csv',ES),('Ventilacao_R02.csv',VENT)]:csv_write(name,rows)
 data={'projeto':'Casa Inteligente | NEXUS | ExpoTech','revisao':'Dimensionamento esquematico R02 - cenario academico','data':'2026-11-06','base':'Arquitetura R02 e distribuicoes R01; programa de equipamentos aprovado pelo grupo','eletrica':{'circuitos':CIRCUITS,'potencia_ativa_w':TOTAL_W,'potencia_aparente_va':TOTAL_VA,'correntes_fasoriais_a':IP,'alimentador':FEEDER,'premissas':EL_NOTES,'solar':PV},'hidraulica':{'aparelhos':FIXTURES,'trechos':SEG,'pressoes':PRESSURES,'esgoto':ES,'nos_maquete_mm':NODES,'saidas_caixas_m':INVERT_OUT,'ventilacao':VENT,'reservacao':RES,'expansao_termica':RES_EXP,'chuva':STORM}}
 csv_write('Circuito_Geracao_C21.csv',[{'id':'C21','tipo':'GERACAO - nao somar a carga','potencia_w':3000,'u_v':220,'fase':'AB','Ib_a':3000/220,'condutores':'2F+PE4mm2','Iz_a':32,'In_a':20,'DR':'B30mA bidirecional conforme inversor','Icn_ka':10,'L_ida_m':20,'queda_ac_pct':PV['queda_ac_pct']}])
 (OUT/'Modelo_Dimensionamento_R02.json').write_text(json.dumps(data,ensure_ascii=False,indent=2))
 print(json.dumps({'total_va':TOTAL_VA,'fase_a':IP,'max_queda_pct':max(c['queda_total_modelo_pct'] for c in CIRCUITS),'Pmin_kPa':min(p['pressao_disponivel_kpa'] for p in PRESSURES),'Q_chuva_ls':STORM['Q_ls'],'cap_calha_ls':MANNING,'UHC':27},ensure_ascii=False))
if __name__=='__main__':exportar()
