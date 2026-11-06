"""Gera os dois memoriais/pranchas e os CADs a partir de Calcular.py."""
from pathlib import Path
import math,json,csv,hashlib
import ezdxf
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
import Calcular as d
h=d.h;e=d.e;OUT=d.OUT;BLUE=h.BLUE;NAVY=h.NAVY;GRAY=h.GRAY
N=6

def num(v,n=2):return f'{v:,.{n}f}'.replace(',','@').replace('.',',').replace('@','.')
def text(c,t,x,y,w=380,size=9):return h.paragraph(c,t,x,y,w,size)
def table(c,y,heads,rows,widths,size=7.8):return h.table(c,y,heads,rows,widths,size)
def frame(c,code,n,title,sub):
 c.setFillColor(NAVY);c.setFont('NexusBold',15);c.drawString(16*mm,281*mm,'CASA INTELIGENTE | NEXUS | ExpoTech')
 c.setFont('NexusBold',11.5);c.drawString(16*mm,267*mm,title);c.setFillColor(GRAY);c.setFont('Nexus',8);c.drawString(16*mm,260*mm,sub)
 c.setStrokeColor(BLUE);c.setLineWidth(.8);c.line(16*mm,255*mm,404*mm,255*mm);c.setLineWidth(.5);c.line(16*mm,28*mm,404*mm,28*mm)
 text(c,'R02 | 06/11/2026 | DIMENSIONAMENTO ESQUEMATICO ACADEMICO | Valido para as hipoteses declaradas; sem liberacao para execucao.',16,23,365,7)
 c.setFont('NexusBold',8);c.setFillColor(NAVY);c.drawRightString(403*mm,15*mm,f'{code}-{n:02} / {N:02}')

def boxes(c,items,y,color=BLUE):
 for x,w,ti,de in items:h.box(c,x,y,w,28,ti,de,color)
 for a,b in zip(items,items[1:]):h.arrow(c,(a[0]+a[1],y+14),(b[0],y+14),color)

def poly(c,xy,pts,col=BLUE,dash=False):
 c.setStrokeColor(col);c.setLineWidth(.7);c.setDash(2,2) if dash else c.setDash();p=c.beginPath();p.moveTo(*xy(*pts[0]))
 for q in pts[1:]:p.lineTo(*xy(*q))
 c.drawPath(p);c.setDash()
def label(c,xy,x,y,s,col=BLUE,dx=2,dy=2):
 xx,yy=xy(x,y);c.setFillColor(col);c.setFont('NexusBold',7);c.drawString(xx+dx*mm,yy+dy*mm,s)

def electrical():
 c=canvas.Canvas(str(OUT/'NEXUS_Eletrica_Dimensionada_R02.pdf'),pagesize=(420*mm,297*mm));c.setTitle('NEXUS | ExpoTech - Eletrica dimensionada R02');c.setAuthor('Projeto NEXUS')
 frame(c,'ED',1,'Programa de cargas, fases e demanda adotada','Programa aprovado: 4 moradores, cozinha eletrica, dois ares-condicionados, aquecimento central e garagem automatizada.')
 rows=[[x['id'],x['uso'],num(x['p_w_hipotese'],0),num(x['fp_hipotese']),num(x['s_va'],1),str(x['u_v']),x['fase']] for x in d.CIRCUITS]
 y=table(c,246,['CIRC.','USO / EQUIPAMENTO','P eq. estudo (W)','FP estudo','S (VA)','U (V)','FASE(S)'],rows,[19,132,48,32,48,32,34],7.8)-6
 text(c,f'<b>TOTAIS:</b> {num(d.TOTAL_W,0)} W equivalentes e {num(d.TOTAL_VA,1)} VA. Demanda adotada = 100% da soma, sem desconto por simultaneidade ou geracao solar. Correntes fasoriais: A {num(d.IP["A"])} A; B {num(d.IP["B"])} A; C {num(d.IP["C"])} A. Neutro fundamental: {num(d.NEUTRAL)} A.',20,y,382,8.6)
 text(c,'P/FP dos equipamentos sao hipoteses de estudo, nao fichas de aparelhos comprados. Nos C1-C7, a previsao em VA foi representada com FP=1; nao e consumo real de LEDs ou eletrodomesticos. TUG e cargas exclusivas foram somadas conservadoramente. Pequenos aparelhos/TV nas TUG nao recebem nova parcela. Bombas: duas por conjunto com intertravamento, uma ativa; a reserva nao opera junto.',20,y-15,382,8.2)
 c.showPage()
 frame(c,'ED',2,'Diagrama unifilar do quadro e entrada','Esquema funcional com F/N/PE identificados. Distribuicao127/220V trifasica e aterramentoTT sao hipoteses, sem aceite da distribuidora.')
 # entrada e barramento
 h.box(c,22,205,100,35,'REDE / MEDICAO BIDIRECIONAL','3F+N127/220V60Hz; entrada de estudo100A. Ramal/padrao externo a validar.',BLUE)
 h.box(c,22,151,100,36,'GERAL / ALIMENTADOR','3P+N100A10kA; 4x50mm2 + PE25mm2; 5m; B1 com margem0,80; Iz107,2A.',BLUE)
 h.arrow(c,(72,205),(72,187));poly(c,lambda x,y:(x*mm,y*mm),[(122,169),(149,169),(149,241)],BLUE)
 c.setStrokeColor(BLUE);c.setLineWidth(2);c.line(149*mm,241*mm,149*mm,48*mm)
 text(c,'BARRAMENTO 3F+N >=125A | PE SEPARADO',154,246,225,8)
 for i,x in enumerate(d.CIRCUITS+[{'id':'C21','fase':'AB','disjuntor_a':20,'s_fase_mm2':4,'uso':'Inversor fotovoltaico','u_v':220}]):
  y=235-i*8.6;c.setStrokeColor(BLUE);c.setLineWidth(.6);c.line(149*mm,y*mm,170*mm,y*mm);c.rect(170*mm,(y-2)*mm,8*mm,4*mm,fill=0,stroke=1)
  typ='B bidirecional' if x['id']=='C21' else 'A';poles='1P+N' if x['u_v']==127 else '2P'
  text(c,f'<b>{x["id"]}</b> | {x["fase"]} | {poles} C{x["disjuntor_a"]}A | DR {typ} 30mA | {x["s_fase_mm2"]}mm2 | {x["uso"]}',182,y+2.6,217,7.4)
 h.box(c,22,94,100,38,'DPS / BEP / TT','DPS TipoII3+1 proprio paraTT; Uc175V F-N, In20kA/Imax40kA, Up<=1,5kV; N-PE por centelhador. Respaldo conforme fabricante.',h.GREEN)
 h.box(c,22,43,100,36,'PROTECAO CONTRA CHOQUES','BEP+PE continuo; equipotencializacao; RA objetivo<=20ohm. RA x30mA<=0,6V. N separado de PE; nao compartilhar N aposRCBO.',h.GREEN)
 poly(c,lambda x,y:(x*mm,y*mm),[(122,113),(149,113)],h.GREEN)
 text(c,'Cada ramo inclui RCBO10kA. Nao ha seccionamento do PE. Todos os dispositivos devem admitir a ligacao/polaridade e energia passante do modelo. Barramento125A considera100A da entrada +20A do ramo gerador. Reservar quadro>=72modulos, depois conferir ocupacao e dissipacao do produto.',20,38,380,7.4)
 c.showPage()
 frame(c,'ED',3,'Distribuicao, rotas de referencia e volumes de banho','Pontos R01 preservados; equipamentos adicionais ganham circuitos proprios. Planta em mm; escala1:50 na impressaoA3 a100%.')
 xy,s=h.base(c);h.LABEL['AM01']=(65,145);h.LABEL['AM05']=(320,130);h.room_labels(c,xy)
 # Representacao das rotas por ambiente; individualizar eletrodutos, nao agrupar circuitos.
 for pts in [[(214,75),(214,120),(65,120),(65,80)],[(214,120),(600,120),(600,210)],[(214,120),(194,120),(194,186)],[(214,120),(464,120),(464,22)],[(214,120),(455,120),(455,60)],[(214,120),(640,120),(640,45)]]:poly(c,xy,pts,BLUE)
 for p in e.POINTS:
  if p['tipo'] not in ('ILUMINACAO','TUG','QUADRO_PROPOSTO'):continue
  x,y=xy(p['x_maquete_mm'],p['y_maquete_mm']);c.setStrokeColor(BLUE);c.setFillColor(colors.white);c.circle(x,y,1.1*mm,stroke=1,fill=1)
 for x,y,w,hh in [(255.5,3,40,40),(541.5,3,40,40)]:
  xx,yy=xy(x,y);c.setStrokeColor(h.RED);c.setDash(2,2);c.rect(xx,yy,w*s,hh*s,fill=0,stroke=1);c.setDash();label(c,xy,x+1,y+17,'BOX800x800',h.RED,0,0)
 for x,y,t in [(214,75,'QD'),(194,186,'COZINHA C8-11/C16'),(464,22,'C12'),(455,60,'C13'),(405,210,'C14'),(600,210,'C15'),(640,45,'C17')]:label(c,xy,x,y,t,BLUE)
 text(c,'<b>ROTAS</b><br/><br/>Linhas indicam corredores de distribuicao. Cada circuito tem eletroduto independente; uma linha comum na planta nao significa cabos agrupados.<br/><br/>Comprimentos de ida usados no calculo: quadroED-05. Percurso real deve ficar dentro desse envelope.<br/><br/>BombaAF/NP e portao: reservas de percurso25/28/35m, sem definir a garagem.<br/><br/>DE20 DI>=15,5mm: circuitos ate4mm2. DE25 DI>=19mm: C8. AlimentadorDE63 DI>=50mm.',326,239,75,8.5)
 text(c,'<b>BANHOS:</b> boxes800x800mm adotados para compatibilizacao. T09 e T24 ficam a mais de600mm da projecao do box; manter fora dos volumes0/1/2, assim como os comandos. Luminarias a2600mm, IP44 como escolha de projeto; verificar volumes/aparelhos e equipotencializacao na execucao. As linhas nao autorizam passagem sobre zonas proibidas.',20,68,383,8.7)
 text(c,'As posicoes exatas de luz/TUG/interruptores continuam nas pranchas EPR01/EPR02 e no CSV R01, integrantes desta revisao por referencia. Pontos exclusivos R01 vinculam R01->C8, R02->C9, R03->C12, R04->C13, R05->C14, R06->C15, R07->C17; garagemR08->C18. C10/C11/C16 e bombas sao novos ramos.',20,49,383,8.4)
 c.showPage()
 frame(c,'ED',4,'Geracao fotovoltaica e interface com a rede','Layout de entrada e protecoes de estudo. Nenhuma geracao, bateria ou conexao da maquete e interligada a rede publica.')
 # cobertura 1:100
 sc=.2*mm;ox=25*mm;oy=166*mm
 def rx(x,y):return ox+x*sc,oy+y*sc
 poly(c,rx,d.h.ROOF+[d.h.ROOF[0]],NAVY)
 for j,(x,y) in enumerate([(10,110),(75,110),(140,110),(400,150),(465,150),(530,150)],1):
  c.setStrokeColor(BLUE);c.setFillColor(colors.HexColor('#edf5fa'));c.rect(*rx(x,y),57.5*sc,115*sc,fill=1,stroke=1);label(c,rx,x+5,y+50,'M'+str(j),BLUE,0,0)
 text(c,'<b>6 x550Wp =3,30kWp | inversor3,00kW</b><br/>DoisMPPT independentes, tres modulos em serie porMPPT; sem paralelizar strings. Envelope por modulo2,30x1,15m; area total15,87m2. Verificar massa, estrutura, ventilacoes, sombras e acesso. Nao e fabricante/modelo selecionado.',185,235,212,9)
 pv=d.PV
 text(c,f'Vmp string126V; Voc corrigido a10C={num(pv["voc_string_corrigida_v"])}V. Imp={num(pv["imp_mod_a"])}A; Isc14,2A; Iprojeto1,25Isc={num(pv["corrente_projeto_a"])}A. Exigir inversor2MPPT90-450V, Vccmax>=600V, Ientrada>=15A e Isc admissivel>=18A/MPPT. Vmp calculado a70C com coef.-0,35%/C:106,16V>90V. Modulo deve admitir fusivel20A. Parametros sao requisitos de estudo a conferir por ficha.',185,205,212,8.7)
 boxes(c,[(20,80,'POR STRING','6mm2,15m; Iz corrigida>=25A; gPV20A se modulo admitir; isolador2P32A600Vcc'),(120,80,'DPS / INVERSOR','DPSPV TipoII600V; inversor certificado, anti-ilhamento e interfaces conforme distribuidora'),(220,80,'RAMO AC C21','220V,13,64A; 2F+PE4mm2,20m; C20A/DRtipoB30mA bidirecional'),(320,79,'QD / MEDICAO','Conexao noQD, barramento125A; geracao nao reduz demanda de dimensionamento')],111)
 text(c,f'QuedaDC={num(pv["queda_dc_pct"])}%; AC={num(pv["queda_ac_pct"])}%. A verificacao DC exige curvas termicas dos cabos e temperatura de operacao; foi fixada Iz minima corrigida25A. Projeto nao comprova autonomia, energia anual, desempenho em sombra ou reserva durante falta de rede. Sem bateria no on-grid adotado.',20,99,380,9)
 text(c,'<b>LIBERACAO EXTERNA:</b> o padrao de entrada, inversor, protecoes, aterramento/SPDA e conexao requerem compatibilidade e aceite da distribuidora, documentacao/certificados e responsavel habilitado. A referencia de conexao consultada e a pagina de GD da EnelSP e sua normaGRI-EDBR-CNC-GRI-0005. Este esquema nao solicita ou aprova acesso.',20,74,380,8.7)
 c.showPage()
 frame(c,'ED',5,'Condutores, protecoes e verificacoes por circuito','Calculo: Ib=S/U; queda conservadora2rhoLI/S, rho=0,0225ohm.mm2/m. Limite adotado4% incluindo alimentador.')
 rows=[[x['id'],x['fase'],num(x['ib_a']),str(x['s_fase_mm2']),str(x['disjuntor_a']),num(x['iz_corrigida_a'],1),str(x['L_ida_m']),num(x['queda_total_modelo_pct']),num(x['icc_min_modelo_a'],0)] for x in d.CIRCUITS]
 y=table(c,246,['CIRC.','FASES','Ib(A)','S F/N/PE*','In(A)','Iz(A)','L(m)','DUtotal(%)','Iccmin(A)'],rows,[21,24,39,55,36,39,34,51,51],7.6)-7
 text(c,'*Circuitos127V: F,N ePE da secao indicada;220V:2F ePE, semN, salvo necessidade do equipamento que exige revisao. C1/C2 usam1,5mm2; todos os demais pelo menos2,5mm2. C6 foi elevado a4mm2 pela queda. Maior queda: '+num(max(x['queda_total_modelo_pct'] for x in d.CIRCUITS))+'%. Todos atendemIb<=In<=Iz nas hipoteses adotadas.',20,y,380,8.3)
 text(c,'B1/PVC70/cobre/ar30C, eletroduto independente por circuito. Alimentador:3F+N50mm2 ePE25mm2; Iz=134x0,80=107,2A>=100A. O fator0,80 e uma margem de estudo, nao um substituto para avaliar harmonicas/agrupamento. Ocupacao com4cabosDext<=13,8mm ePE Dext<=10,5mm emDI50mm: '+num(d.FEEDER['ocupacao_pct'])+'%.',20,y-18,380,8.2)
 c.showPage()
 frame(c,'ED',6,'Memoria, especificacoes e verificacoes de entrega','Fechamento dos calculos internos do cenario; condicoes externas e selecao dos produtos explicitadas.')
 y=246
 blocks=[('Coordenacao termica e curto-circuito','Icn10kA superaIccmax hipotetica6,35kA. Para a curvaC, Iccmin no modelo supera10In em todos os circuitos. Isso nao valida um produto: exigir energia passante I2t <=(115S)^2, compatibilidade de partida/inverter e temposTT na ficha do RCBO. A selecao/curvaI2t do fabricante, medicao de loop e ensaiosDR permanecem verificacoes antes da execucao.'),('Demanda e balanceamento',f'Potencia aparente de estudo{num(d.TOTAL_VA,1)}VA. Cargas a100%; nenhuma promessa de simultaneidade. Balanceamento por correntes complexas, considerandoFPs indutivos declarados e tensoes fasoriais127V. Os220V nominais correspondem a219,97V no modelo vetorial; diferenca de arredondamento. Maximo de fase{num(max(d.IP.values()))}A <100A.'),('Especificacao dos equipamentos','Nao sao marcas compradas. Cada equipamento real deve ter potencia/corrente/FP e modo de ligacao compativeis com a tabela; se exceder, recalcular. Bombas: conjuntos com reserva intertravada, protecao individual de motor e contra falta de agua. Reservas de portao, central e aquecimento nao acionam as cargas da maquete.'),('Aterramento e sobretensoes','TT com eletrodo eBEP, N/PE separados, PE sem seccionamento e equipotencializacao. RA20ohm e alvo, nao medicao. DPS3+1 e sua protecao de respaldo devem admitir100A da entrada e a corrente presumida. Avaliar necessidade deTipoI eSPDA conforme exposicao; isso nao foi certificado pelo esquema.'),('Memoria reproduzivel e referencias','O CSV eJSON registram as contas, fases e hipoteses. Calcular.py reproduz cada resultado; testes acompanham limites. Referencia principal: ABNT NBR5410:2004VC2008, tabelas36/PE e itens de queda/protecao/banhos, consulta via copia academica PUCGoias. A norma nao e redistribuida. Conexao solar: documentacao oficial EnelSP deGD. Links no README.'),('O que esta entregue / o que depende do local','Entregues: cargas, demanda de estudo, fases, circuito/condutor/protecao, queda, modelo de curto, quadro/unifilar, rotas e entrada renovavel. Antes de obra/energizacao real: concessionaria/fornecimento, rotas medidas, Icc/loop/RA, produtoI2t/partida, memoriaSPDA e responsabilidade tecnica. Esta R02 e o projeto esquematico dimensionado academico, sem declarar essas medicoes executadas.')]
 for title,body in blocks:
  y-=text(c,'<b>'+title.upper()+'</b><br/>'+body,20,y,380,9)+8
 c.save()

def hydraulic():
 c=canvas.Canvas(str(OUT/'NEXUS_Hidraulica_Dimensionada_R02.pdf'),pagesize=(420*mm,297*mm));c.setTitle('NEXUS | ExpoTech - Hidraulica dimensionada R02');c.setAuthor('Projeto NEXUS')
 frame(c,'HD',1,'Premissas, reservacao e aquecimento','4 moradores; AF/AQ potaveis separadas da redeNP de chuva para descargas. Reservatorios no solo, nao sobre a cobertura.')
 r=d.RES
 rows=[['Consumo de estudo','4x150=600L/dia; referencia de consumo residencial do ManualTigre, nao medicao'],['Destinacao','Descargas:4x5x6=120L/dia; rotina potavel480L/dia; reserva potavel verifica600L/dia com reposicaoNP'],['Reservacao potavel','1.000L nominal,800L uteis;800/600='+num(800/600)+'dias sem reposicao. Carga de agua cheia ~9,81kN, apoio a dimensionar'],['Reservacao nao potavel','1.000L nominal,800L uteis; alvo6diasx120=720L; capacidade util800L. Nao e confiabilidade anual baseada em chuva'],['PressurizacaoAF','2bombas alternadas, uma ativa. Q>=1,45L/s (inclui reposicaoNP0,30); H>=28mca; estudo1,1kW/bomba; controle250kPa'],['PressurizacaoNP','2bombas alternadas, uma ativa. Q>=0,30L/s; H>=18mca; estudo370W/bomba; controle150kPa'],['Aquecimento','Acumulador200L; resistencia3kW; acumulacao60C; mistura40C; limitador de uso corporal45C'],['Volume quente diario','4x50L de agua misturada40C =200L; fracao quente(40-20)/(60-20)=0,5 ->100L/dia a60C'],['Recuperacao integral',f'200x4,186x40/3600={num(r["energia_boiler_kwh"])}kWh; /3kW={num(r["tempo_recuperacao_h"])}h; sem perdas termicas'],['Expansao e seguranca',f'Expansao termica{num(d.RES_EXP["expansao_agua_l"])}L. Vaso potavel18L: capacidade entre250/350kPa=4,00L; alivio<=400kPa, compativel com fabricante/PMTA'],['Fontes/modelos','Vazoes nominais de projeto, capacidade e rendimento das bombas/aquecedor devem ser satisfeitos pelas fichas dos produtos.']]
 y=table(c,246,['PREMISSA','DIMENSIONAMENTO ADOTADO'],rows,[65,315],8.4)-8
 text(c,'Reposicao potavel da cisternaNP por bocal<=20mm com separacao atmosferica de estudo50mm acima do extravasor; sem interligacao direta ou valvula de bypass entre redes. Identificar tubulacoes/pontosNP, impedir consumo corporal/alimentos e prever limpeza, extravasor, acesso e bloqueio manual.',20,y,380,8.8)
 c.showPage()
 frame(c,'HD',2,'Distribuicao dimensionada AF/AQ/NP','Planta1:50A3. Colunas/ramais em projecao; CAD3D registra as alturas e diametros de calculo.')
 xy,s=h.base(c);h.room_labels(c,xy)
 for rr in d.SEG:poly(c,xy,rr['vertices_maquete_mm'],h.COL[rr['rede']],rr['rede']=='AQ')
 h.fixtures(c,xy,[p['id'] for p in h.POINTS if p['abastecimento']])
 for x,y,t,col in [(330,-50,'PAF1/2 AF40',BLUE),(720,-18,'PNP1/2 NP25',h.GREEN),(330,110,'CAF40',BLUE),(205,110,'AF25',BLUE),(585,110,'AF32',BLUE),(455,60,'AQ1 200L/3kW',h.RED),(400,101,'AQ28',h.RED),(400,-18,'NP25',h.GREEN)]:label(c,xy,x,y,t,col,dy=-4 if y==101 else 2)
 text(c,'<b>DIAMETROS DE PROJETO</b><br/><br/>AF: PVC soldavel DE40/32/25/20. DI calculo35,2/27,8/21,6/17mm.<br/><br/>AQ: CPVC DE28,DI>=22mm; ramais DE22,DI>=17,5mm; classe60C/600kPa. Isolamento termico20mm como premissa.<br/><br/>NP: PVC DE25/20; separado e identificado.<br/><br/>Plano de distribuicao2.400mm. Alturas dos aparelhos na tabelaCSV.<br/><br/>Conexoes, registros e suportes devem satisfazer a perda equivalente adotada; confirmar dilatacao/ancoragem doCPVC.',326,239,75,8.4)
 text(c,'Os locais dePAF/PNP sao nos funcionais do estudo, sem dimensionar a area tecnica do lote. Reservatorios ficam no solo com base/carga verificada; a bomba deve ter sucao afogada/condicao deNPSH conforme curva. Sensor de nivel seco, protecao contra funcionamento sem agua, isolamento para manutencao e alternancia sao requisitos do conjunto, nao automacoes ja ensaiadas.',20,68,380,8.7)
 text(c,'Termostato e limitador independentes, conjunto de alivio/retencao e vaso de expansao potavel compativeis com o aquecedor, sem registro isolando sua protecao. Misturador termostatico evita agua a60C diretamente no uso corporal. Pressurizadores com controle e alivio limitam a pressao conforme as premissas; ensaiar temperaturas/pressoes antes de uso real.',20,48,380,8.6)
 c.showPage()
 frame(c,'HD',3,'Memoria hidraulica: vazoes, perdas e pressoes','Darcy-Weisbach; Swamee-Jain; agua nu1e-6m2/s e rugosidade1,5e-6m; Leq=1,5L como provisao de conexoes.')
 rows=[[s['id'],s['rede'],num(s['Q_ls'],3),str(s['DE_mm']),num(s['DI_min_calculo_mm'],1),num(s['L_real_m']),num(s['v_ms']),num(s['hf_m'],3)] for s in d.SEG]
 y=table(c,246,['TRECHO','REDE','Q(L/s)','DE(mm)','DI min(mm)','Lreal(m)','v(m/s)','hf(mca)'],rows,[41,28,47,40,50,54,50,70],7.3)-6
 pmin=min(d.PRESSURES,key=lambda p:p['pressao_disponivel_kpa'])
 text(c,f'<b>PRESSAO CRITICA:</b> {pmin["aparelho"]}/{pmin["rede"]} ->{num(pmin["pressao_disponivel_kpa"])}kPa disponiveis; requisito de projeto100kPa potavel e50kPa NP. Todos os pontos atendem. Vazoes somadasAF+AQ1,15L/s; reposicaoNP0,30L/s leva bombaAF a1,45L/s. O fator1,5 de comprimento e premissa; confirmar perdas dos acessorios selecionados.',20,y,380,8.2)
 text(c,'Formula: Pdest=Pfonte-rhog(zdest-0,30+Somahf)-perdas de equipamentos. AF250kPa; NP150kPa. AQ acrescenta50kPa para grupo/aquecedor e20kPa para mistura; NP reserva25kPa para filtracao/desinfeccao. Velocidade alvo<2m/s em todos os trechos. Saidas reais devem requerer no maximo a pressao minima especificada; se maiores, rever o conjunto.',20,y-18,380,8.2)
 c.showPage()
 frame(c,'HD',4,'Esgoto sanitario: rotas, caixas e ventilacao','Revisao elimina a passagem da pia sob a sala. Esgoto e chuva seguem redes independentes; cotas referentes ao piso0,00m.')
 xy,s=h.base(c);h.room_labels(c,xy)
 for rr in d.ES:poly(c,xy,rr['vertices_maquete_mm'],h.BROWN,True)
 h.fixtures(c,xy)
 for id,pt in d.NODES.items():
  x,y=xy(*pt);c.setFillColor(colors.white);c.setStrokeColor(h.TEAL if id.startswith('V') else NAVY);c.rect(x-1.5*mm,y-1.5*mm,3*mm,3*mm,fill=1,stroke=1);label(c,xy,*pt,id,h.TEAL if id.startswith('V') else NAVY,dy=-5 if id.startswith('CS') else 1)
 text(c,'<b>ESGOTO</b><br/>BaciasDN100.<br/>Lavatorios/chuveirosDN40.<br/>Pia/tanque/lavadoraDN50.<br/>SaidaCS DN75.<br/>ColetoresDN100.<br/><br/>DN<100:2%.<br/>DN100:1%.<br/><br/>CG1:18L uteis min., acesso externo.<br/>CI:600x600mm uteis como escolha, tampa acessivel.<br/><br/>VentilacaoDN50, tomadas apos desconectores a<=0,8m, topoa5,30m; ramais de bacia antes daCI.<br/><br/>Vertices, DN e cotas noCSV eCAD3D.',350,239,53,8)
 text(c,'CG1 passa ao exterior da cozinha, no ponto105/310mm da maquete. CS1/CS2 recebem lavatorio, chuveiro e ralo, sem dupla sifonagem em serie; fecho hidrico50mm. Bacias seguem paraCI sem atravessarCS. Tanque/lavadora/pia tem desconectores proprios. Prever ventilacao proxima a cada desconector e a ambos os ramais de bacia; os nosV indicam subidas, sem interligar agua/esgoto.',20,68,380,8.6)
 text(c,'Cada inspeção fica acessivel fora da projecao da casa. Evitar conexoes a90graus no coletor; usar juncao45graus e caixas nas mudancas propostas. O lote/solo, cobertura estrutural dos tubos, dimensoes de loucas e ligacao publica nao foram levantados. A posicaoDS1 e uma fronteira hipotetica a cota-0,60m, nao uma rede existente confirmada.',20,48,380,8.6)
 c.showPage()
 frame(c,'HD',5,'Altimetria, UHC e ventilacao','Carga total27UHC. Dimensionamento dos ramais e verificacao de chegada a caixas no cenario deimplantacao adotado.')
 rows=[[r['id'],str(r['DN_mm']),num(r['declividade_pct'],1),str(r['UHC']),num(r['L_m']),num(r['cota_inicio_m'],3),num(r['cota_chegada_m'],3),num(d.INVERT_OUT.get(r['destino'],0),3)] for r in d.ES]
 y=table(c,246,['TRECHO','DN(mm)','i(%)','UHC','L(m)','ZI(m)','Zchegada(m)','Zsaida caixa(m)'],rows,[55,35,35,30,43,55,55,72],7.5)-7
 text(c,'Cota de chegada>=cota de saida da caixa em todos os trechos. CI1saida-0,300; CI2-0,400; CI3-0,375; CIE-0,500m. Saida final chega a-'+num(abs(next(r for r in d.ES if r['id']=='ES_OUT')['cota_chegada_m']),3)+'m antes da fronteira-0,600m. Recalcular se a cota publica/terreno mudar. RalosH10/H11 nao acrescentamUHC de uso; coletam no sistema do mesmo banho.',20,y,380,8.6)
 text(c,'<b>VENTILACAO:</b> ramaisDN50, comprimentos de projeto<=10m, pontos por grupo e bacias antes daCI. TerminaisV1-V5 a5,30m, mais de2m sobre a cobertura3,18m do modelo e acima das aberturas. Especificar conexoes acima do eixo do esgoto, drenar condensado para o sistema e manter afastamento de captacoes de ar; confirmar regime de cobertura/local. Para o grupo com bacia<=17UHC, DN50 e a referencia consultada; os grupos locais sao menores.',20,y-24,380,8.4)
 text(c,'A ventilacao e o fecho hidrico sao funcoes diferentes. O esquema nao substitui o detalhamento das tomadas nos desconectores e a verificacao de distancias efetivas; oCAD indica os percursos base. Fonte tecnica: ManualTigre, quadros deUHC/ramais/coletores/ventilacao, referenciandoNBR8160. Nao se redistribuem as tabelas integrais.',20,y-49,380,8.1)
 c.showPage()
 frame(c,'HD',6,'Chuva: calhas, descidas, reservacao e qualidade','Captacao na cobertura85,756m2, sem garagem. i=180mm/h e uma hipotese de projeto, nao uma serie pluviometrica local.')
 st=d.STORM
 rows=[['Vazao de captacao',f'Q=iA/3600={num(st["Q_ls"],3)}L/s; com margem20%={num(st["Q_com_margem20_ls"],3)}L/s'],['Calha semicircular','DE200; lamina80mm; i0,5%; nManning0,011; area0,0117m2; capacidade='+num(st['capacidade_Manning_ls'],3)+'L/s'],['Caimento/saidas','Ponto alto central, duas meias-calhas7,175m; queda35,875mm por lado. Duas saidas acessiveis, sem alterar paineisR02'],['Condutores verticais',f'2xDN100; cada um{num(st["area_por_descida_m2"],3)}m2/{num(st["Q_por_descida_ls"],3)}L/s. Pre-selecaoTigre:78,54cm2>{num(st["area_por_descida_m2"],3)}m2. Verificar abaco/bocal final'],['Coletor pluvial',f'DN150 i1%; Manning a meia secao, n0,011: capacidade{num(st["coletor_capacidade_ls"],3)}L/s > Q com margem'],['Desvio inicial','Hipotese2mm x85,756=171,512L; adotar recipiente200L independente. Ajustar por qualidade e limpeza, nao e valor universal'],['Cisterna/uso','1000L nominal/800Luteis para descargas120L/d. Alvo6dias sem aporte=720L;800Lsupera o alvo. Sem garantia de eficiencia anual'],['Evento de exemplo',f'10mm,C0,80,eficiencia0,90 ->617,443L antes do desvio; apos171,512L de desvio, saldo{num(st["exemplo_evento_10mm_l_apos_desvio"],3)}L'],['Tratamento e controle','Tela/desvio>=5,146L/s; cisterna com sedimentacao. Tratamento na saidaNP>=1,10m3/h e perda<=25kPa, bloqueio por falha; desempenho/qualidade por fabricante e laboratorio, sem certificacao nesta entrega.'],['Excedentes','Extravasor e bypass com capacidade>=Q com margem; rota pluvial independente e protecao contra insetos. Destino legal do lote a definir antes da execucao.']]
 y=table(c,246,['ITEM','DIMENSIONAMENTO / CRITERIO'],rows,[67,313],8.2)-7
 text(c,'<b>LEITURA DOS RESULTADOS:</b> fechados os calculos de vazao, diametros de estudo, perdas/pressoes, reservacao, aquecimento, UHC/cotas e drenagem para estas hipoteses. Permanecem verificacoes do local/produtos: IDF/recorrencia, saidas publica/pluvial, solo/apoio, curvas de bombas, seguranca do boiler, desconectores/ventilacao detalhados, bocais e qualidadeNP. Nao declarar agua potavel, economia anual ou funcionamento real da maquete.',20,y,380,8.6)
 text(c,'Referencias: ManualTecnicoTigre (consumo, UHC/ES/VE e pluviais); PBQP-H/entidade setorial de metais sanitarios (pressao/temperatura, citandoNBR5626:2020); cartilhaSenadoVerde eCAESB para separacao conceitualNP. Critérios locais e edicoes vigentes devem ser conferidos na etapa de execucao. Formulas/hipoteses, resultados e fontes estao noCSV/JSON/README.',20,y-25,380,8)
 c.save()

def cad():
 # CADs mantem unidades mm. Agua/ES sao3D; unifilar esquematico e planta solar2D.
 for name,kind in [('H02_Agua_Dimensionada_3D.dxf','agua'),('H02_Esgoto_Dimensionado_3D.dxf','esgoto'),('E02_Unifilar_Dimensionado.dxf','unifilar'),('E02_Cobertura_Fotovoltaica.dxf','solar')]:
  doc=ezdxf.new('R2010');doc.units=4;m=doc.modelspace()
  for layer,col in [('BASE',8),('AF',5),('AQ',1),('NP',3),('ES',30),('VE',6),('ELETRICA',5),('TEXTO',7)]:doc.layers.new(layer,dxfattribs={'color':col})
  if kind in ('agua','esgoto','solar'):
   for w in h.WALLS:
    for a,b in h.segments(w):
     pts=[(a,w['u']),(b,w['u'])] if w['eixo']=='H' else [(w['u'],a),(w['u'],b)]
     m.add_line(tuple(v*20 for v in pts[0]),tuple(v*20 for v in pts[1]),dxfattribs={'layer':'BASE'})
  if kind=='agua':
   for rr in d.SEG:
    pts=rr['vertices_maquete_mm'];zm=max(rr['z1_m'],rr['z2_m'])*1000;coords=[(pts[0][0]*20,pts[0][1]*20,rr['z1_m']*1000)]+[(x*20,y*20,zm) for x,y in pts]+[(pts[-1][0]*20,pts[-1][1]*20,rr['z2_m']*1000)]
    m.add_polyline3d(coords,dxfattribs={'layer':rr['rede']});x,y=pts[-1];m.add_text(rr['id']+f' DE{rr["DE_mm"]}',dxfattribs={'height':90,'insert':(x*20+90,y*20+110,rr['z2_m']*1000),'layer':'TEXTO'})
  elif kind=='esgoto':
   for rr in d.ES:
    pts=rr['vertices_maquete_mm'];cum=0;xyz=[]
    for i,(x,y) in enumerate(pts):
     if i:cum+=math.dist(pts[i-1],pts[i])*.02
     xyz.append((x*20,y*20,(rr['cota_inicio_m']-cum*rr['declividade_pct']/100)*1000))
    m.add_polyline3d(xyz,dxfattribs={'layer':'ES'});x,y=pts[0];m.add_text(rr['id']+f' DN{rr["DN_mm"]} i={rr["declividade_pct"]}%',dxfattribs={'height':90,'insert':(x*20+90,y*20+100,rr['cota_inicio_m']*1000),'layer':'TEXTO'})
   vent_pick={'V1':(252,48,-.1208),'V2':(544,57,-.1208),'V3':(190,186,-.1016),'V4':(330,17,-.1208),'V5':(464,20,-.1208),'V6':(235,12,-.123),'V7':(516,12,-.123)}
   for vv in d.VENT:
    x,y=d.NODES[vv['terminal']];a,b,z=vent_pick[vv['id']];plan=(abs(x-a)+abs(y-b))*.02;zend=3400+plan*10
    coords=[(a*20,b*20,z*1000),(a*20,b*20,3400),(x*20,b*20,3400+abs(x-a)*.2),(x*20,y*20,zend),(x*20,y*20,5300)]
    m.add_polyline3d(coords,dxfattribs={'layer':'VE'});m.add_text(vv['id']+' DN50 topo5300',dxfattribs={'height':90,'insert':(x*20+90,y*20,5300),'layer':'VE'})
  elif kind=='unifilar':
   m.add_line((0,0),(0,5000),dxfattribs={'layer':'ELETRICA'})
   for i,rr in enumerate(d.CIRCUITS):
    y=4800-i*220;m.add_line((0,y),(500,y),dxfattribs={'layer':'ELETRICA'});m.add_text(f'{rr["id"]} {rr["fase"]} C{rr["disjuntor_a"]}A DR30mA10kA {rr["s_fase_mm2"]}mm2 {rr["uso"]}',dxfattribs={'height':75,'insert':(550,y-30),'layer':'ELETRICA'})
   m.add_text('3F+N127/220V | Geral100A | 4x50+PE25 | TT | DPS3+1 | Barramento125A | C21 PV20A DRB30mA',dxfattribs={'height':95,'insert':(0,5300),'layer':'TEXTO'})
  else:
   m.add_lwpolyline([(x*20,y*20) for x,y in h.ROOF],close=True,dxfattribs={'layer':'BASE'})
   for j,(x,y) in enumerate([(10,110),(75,110),(140,110),(400,150),(465,150),(530,150)],1):
    m.add_lwpolyline([(x*20,y*20),((x+57.5)*20,y*20),((x+57.5)*20,(y+115)*20),(x*20,(y+115)*20)],close=True,dxfattribs={'layer':'ELETRICA'});m.add_text('M'+str(j)+' 550Wp',dxfattribs={'height':100,'insert':(x*20+80,y*20+100),'layer':'TEXTO'})
  m.add_text('NEXUS R02 | DIMENSIONAMENTO ESQUEMATICO ACADEMICO | mm | conferir hipoteses no memorial',dxfattribs={'height':110,'insert':(0,7000),'layer':'TEXTO'});doc.saveas(OUT/name)

def main():
 d.exportar();h.fonts();electrical();hydraulic();cad();print('Dois PDFs de6pranchas e4DXFs gerados.')
if __name__=='__main__':main()
