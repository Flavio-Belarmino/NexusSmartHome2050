# CASA INTELIGENTE | NEXUS | ExpoTech
# Fonte editavel do gerador de documentacao do projeto.
# Gera PDF, DXF, CSV, JSON e ZIP a partir de uma geometria comum.
# Anteprojeto: arquitetura, maquete e sugestoes de automacao.
# Dimensoes e distribuicao serao compatibilizadas no detalhamento.
# Inclui planta eletrica da maquete, circuitos e automacoes propostas.
#
# COMO ATUALIZAR: ajuste os parametros e coordenadas abaixo.
# Todas as coordenadas de CASA, PAREDES e ABERTURAS sao em mm da MAQUETE.
# A vista arquitetonica multiplica essas medidas por 20, sem substituir
# o MDF por uma espessura de parede convencional inventada.

import sys, subprocess, importlib.util, math, csv, json, zipfile, hashlib, shutil
from pathlib import Path
from datetime import datetime

def dependencias():
    falta = [p for p in ('reportlab', 'ezdxf') if importlib.util.find_spec(p) is None]
    if falta:
        subprocess.check_call([sys.executable, '-m', 'pip', '-q', 'install', *falta])

# Parametros gerais e escolhas editaveis.
PROJETO = 'Casa Inteligente | NEXUS | ExpoTech'
REVISAO = 'R02 - ANTEPROJETO'
PARAM = dict(escala_maquete=20.0, piso_L=717.5, piso_W=308.0,
             parede_H=130.0, altura_total=159.0, faixa_cobertura=23.0,
             mdf=3.0, margem_piso=10.0, base_L=1200.0, base_W=900.0,
             base_espessura=18.0, casa_x=100.0, casa_y=340.0,
             central_x=60.0, central_y=70.0, central_L=740.0,
             central_W=170.0, agua_x=900.0, agua_y=360.0,
             agua_L=230.0, agua_W=230.0)
# Parametros de estudo em mm, editaveis para compatibilizacao.

# Paredes em coordenadas locais da CASA, excluindo margem do piso.
# Cada registro: identificacao, eixo, posicao, inicio, fim.
# As coordenadas internas sao preliminares para o anteprojeto.
PAREDES = [
 ('R01','V',1.5,0,288), ('R02','V',696,0,288),
 ('R03','H',1.5,0,297), ('R04','H',1.5,297,697.5),
 ('R05','H',286.5,0,304), ('R06','H',286.5,304,697.5),
 ('R07','H',148,103,214), ('R08','V',214,148,288),
 ('R09','V',214,0,92), ('R10','H',92,214,297),
 ('R11','V',297,0,92), ('R12','V',304,148,288),
 ('R13','H',148,304,511), ('R14','V',511,94,288),
 ('R15','V',487,0,94), ('R16','V',583,0,94),
 ('R17','H',94,365,697.5),
]
# Programa de ambientes proposto para discussao com a equipe.
AMBIENTES = [
 ('AM01','SALA / SOCIAL',[(1.5,1.5),(212.5,1.5),(212.5,146.5),
                         (101.5,146.5),(101.5,286.5),(1.5,286.5)]),
 ('AM02','COZINHA',[(104.5,149.5),(212.5,149.5),(212.5,286.5),(104.5,286.5)]),
 ('AM03','BANHO 1',[(215.5,1.5),(295.5,1.5),(295.5,90.5),(215.5,90.5)]),
 ('AM04','SERVICO / APOIO',[(298.5,1.5),(485.5,1.5),(485.5,92.5),(298.5,92.5)]),
 ('AM05','CIRCULACAO',[(215.5,95.5),(509.5,95.5),(509.5,146.5),(215.5,146.5)]),
 ('AM06','QUARTO 1',[(305.5,149.5),(509.5,149.5),(509.5,286.5),(305.5,286.5)]),
 ('AM07','QUARTO 2',[(512.5,95.5),(696,95.5),(696,286.5),(512.5,286.5)]),
 ('AM08','BANHO 2',[(488.5,1.5),(581.5,1.5),(581.5,92.5),(488.5,92.5)]),
 ('AM09','APOIO',[(584.5,1.5),(696,1.5),(696,92.5),(584.5,92.5)]),
 ('AM10','HALL',[(215.5,149.5),(302.5,149.5),(302.5,286.5),(215.5,286.5)]),
]
# Aberturas: id, parede, tipo, inicio, largura, peitoril, altura, classe.
# Coordenada inicio acompanha o eixo longitudinal da parede.
# Posicoes e alturas das aberturas: anteprojeto.
ABERTURAS = [
 ('P01','R01','porta',12,45,0,105,'Anteprojeto'),
 ('J01','R01','janela',75,60,45,55,'Anteprojeto'),
 ('J02','R01','janela',185,60,45,55,'Anteprojeto'),
 ('J03','R05','janela',110,50,45,55,'Anteprojeto'),
 ('P02','R05','porta',162,45,0,105,'Anteprojeto'),
 ('V01','R05','veneziana',235,25,75,25,'Anteprojeto'),
 ('J04','R06','janela',385,60,45,55,'Anteprojeto'),
 ('J05','R06','janela',565,75,45,55,'Anteprojeto'),
 ('P03','R08','porta',213,40,0,105,'Anteprojeto'),
 ('P04','R10','porta',252,35,0,105,'Anteprojeto'),
 ('P05','R13','porta',450,45,0,105,'Anteprojeto'),
 ('P06','R14','porta',100,45,0,105,'Anteprojeto'),
 ('P07','R17','porta',390,40,0,105,'Anteprojeto'),
 ('P08','R17','porta',535,35,0,105,'Anteprojeto'),
 ('P09','R17','porta',625,35,0,105,'Anteprojeto'),
 ('V02','R11','veneziana',30,25,75,25,'Anteprojeto'),
 ('V03','R16','veneziana',30,25,75,25,'Anteprojeto'),
]

# Cobertura: limites preliminares e editaveis para compatibilizacao.
COBERTURA = dict(divisao_T1=255.0, divisao_T2=365.0, recuo=60.0)

# Componentes: reservas de espaco P, nao dimensoes verificadas dos modulos.
COMPONENTES = [
 ('MEGA','Arduino Mega',45,95,115,65),
 ('PROTO','Protoboard 830',180,95,180,70),
 ('ESP','ESP32',385,95,65,45),
 ('RELE','Modulo de rele',475,95,65,45),
 ('DRIVERS','Acionadores a identificar',565,95,130,70),
]
# x/y das reservas acima sao locais da central, incluindo margem para fios.
# Ajuste para caber no tampo: local y sera reposicionado na faixa util.

SISTEMAS = [
 ('IL01','Iluminacao','LEDs brancos','Proposta'),
 ('LU01','Luminosidade','LDR KY-018','Proposta'),
 ('BR01','Brise em J04','Microservo 9 g','Proposta'),
 ('PR01','Presenca','PIR SR-501','Proposta'),
 ('TH01','Temperatura e umidade','DHT22','Proposta'),
 ('AC01','Acesso','RFID RC522 e solenoide 6 V','Proposta'),
 ('AG01','Agua em recirculacao','Bomba 12 V e sensor de vazao','Proposta'),
 ('FV01','Experimento solar','Placa 115 x 85 mm e controlador','Proposta'),
 ('NI01','Nivel do reservatorio','HC-SR04','Proposta'),
 ('BT01','Comandos locais','Modulo touch de 4 canais / botoes','Proposta'),
]

# Retornos internos das paredes externas, para cotas livres dos ambientes.
AMBIENTES = [(code,nome,[(3.0 if x==1.5 else 694.5 if x==696 else x,
                           3.0 if y==1.5 else 285.0 if y==286.5 else y)
                          for x,y in poly]) for code,nome,poly in AMBIENTES]

# Um LED por ponto e um resistor por LED. Valores respeitam o inventario.
PONTOS_LUZ = [
 ('L01','AM01',65,80,470),('L02','AM01',65,210,470),
 ('L03','AM02',155,215,470),('L04','AM03',255,45,470),
 ('L05','AM04',390,45,470),('L06','AM06',405,210,560),
 ('L07','AM07',600,210,560),('L08','AM08',535,45,560),
 ('L09','AM09',640,45,560),('L10','AM05',430,120,560),
 ('L11','AM10',260,215,1000),
]
SENSORES = [('PR01','PIR',65,120),('TH01','DHT22',600,255),
            ('LU01','LDR',415,305),('AC01','RFID',-18,35),
            ('BR01','SERVO',415,288)]

# Reservas de pinos do Mega; cargas de potencia usam acionadores externos.
PINAGEM = [(code,f'D{22+i}','LED individual',f'1 resistor de {res} ohm em serie')
           for i,(code,room,x,y,res) in enumerate(PONTOS_LUZ)] + [
 ('VAZAO','D2','Entrada de pulsos','Confirmar tensao e tipo de saida do sensor'),
 ('EMERGENCIA','D3','Leitura de contato','Corte fisico dos atuadores independente do software'),
 ('SERVO','D6','Sinal do brise','Alimentacao 5 V externa; GND comum'),
 ('SOLENOIDE','D7','Comando de driver','Driver + diodo; alimentacao regulada 6 V'),
 ('BOMBA','D8','Comando de driver','Driver + diodo; alimentacao 12 V'),
 ('FITA LED','D9','Comando de driver','Confirmar tensao e corrente antes de conectar'),
 ('HC-SR04 TRIG','D10','Saida de disparo','Leitura do nivel no reservatorio'),
 ('HC-SR04 ECHO','D11','Entrada de eco','Sensor alimentado em 5 V'),
 ('RELE','D12','Reserva de comando','Confirmar numero de canais e logica do modulo'),
 ('DHT22','D34','Dados','Verificar resistor de pull-up no modulo'),
 ('PIR','D35','Entrada digital','Confirmar pinagem da placa'),
 ('TOUCH 1-4','D36 / D37 / D38 / D39','Entradas digitais','Confirmar modelo e nivel das quatro saidas'),
 ('BOTOES 1-4','D40 / D41 / D42 / D43','Comandos locais','Contato para GND; INPUT_PULLUP'),
 ('LDR','A0','Entrada analogica','Confirmar conexoes do modulo KY-018'),
 ('RFID RST','D49','Reset','Conversao de nivel para 3,3 V'),
 ('RFID MISO','D50','SPI / CIPO','Interface de nivel compativel com Mega'),
 ('RFID MOSI','D51','SPI / COPI','Conversao de nivel para 3,3 V'),
 ('RFID SCK','D52','SPI / clock','Conversao de nivel para 3,3 V'),
 ('RFID SS','D53','SPI / selecao','Conversao de nivel para 3,3 V'),
 ('ESP32 UART','D18 TX1 / D19 RX1','Comunicacao serial','Interface 5 V / 3,3 V; pinos ESP a definir'),
]

ADJACENCIAS = [
 ('Exterior','AM01','P01'),('Exterior','AM02','P02'),
 ('AM01','AM02','Vao aberto'),('AM01','AM05','Vao aberto'),
 ('AM02','AM10','P03'),('AM10','AM05','Vao aberto'),
 ('AM03','AM05','P04'),('AM04','AM05','P07 / trecho aberto'),
 ('AM06','AM05','P05'),('AM07','AM05','P06'),
 ('AM08','AM07','P08'),('AM09','AM07','P09'),
]

CIRCUITOS = [
 ('C01','11 LEDs de ambientes','5 V','D22-D32','470 / 560 / 1000 ohm por LED'),
 ('C02','LDR / PIR / DHT / HC / touch','Conforme modulo','A0 / D10-D11 / D34-D39','Conferir placa e pinagem'),
 ('C03','RFID RC522','3,3 V','SPI D49-D53','Regulador e conversores de nivel'),
 ('C04','Microservo do brise','5 V externo','D6','Corrente de pico a medir'),
 ('C05','Bomba de recirculacao','12 V','D8 -> driver','0,5-0,7 A em regime; medir partida'),
 ('C06','Solenoide da porta','6 V regulado','D7 -> driver','Corrente e ciclo de uso a medir'),
 ('C07','Fita LED','A identificar','D9 -> driver','Tensao, corrente e trecho a definir'),
 ('C08','ESP32 / comunicacao','Entrada da placa','UART D18-D19','Interface logica 5 V / 3,3 V'),
 ('C09','Experimento fotovoltaico','12 V nominal','Circuito independente','1,5 W nominal; controlador a identificar'),
]
COMPLEMENTOS = [
 ('Drivers de potencia','3 canais propostos','MOSFET logic level, Vgs 5 V; dimensionar corrente'),
 ('Diodos de roda livre','Bomba e solenoide','Dimensionar corrente e tensao reversa'),
 ('Regulador 6 V','1 ramal','Dimensionar pela corrente da solenoide'),
 ('Regulador 3,3 V','RFID / interface','Dimensionar com consumo dos modulos'),
 ('Conversores de nivel','SPI e UART','Interface adequada a direcao e frequencia dos sinais'),
 ('Fusiveis e porta-fusiveis','Por ramal de potencia','Definir apos medir consumo e corrente de partida'),
 ('Cabos e conectores','Por comprimento dos ramais','Bitola por corrente, queda de tensao e montagem'),
 ('Corte de emergencia','Acionamento fisico','Conferir contatos do botao e dispositivo de corte'),
 ('Fixacoes e bandeja','Eletronica / agua','Separar umidade, cargas e terminais energizados'),
]
RESERVAS = [
 ('OV7670','2 cameras','Posicao e interface em etapa posterior; placas a identificar'),
 ('Modulo rele','1 modulo','Numero de canais e logica a confirmar; reserva D12'),
 ('Fontes 12 V / 5 A','2 unidades','Uma no ramal da bomba; segunda como reserva'),
 ('Fontes 5 V / 3 A','2 unidades','Uma principal; segunda disponivel para ramal auxiliar'),
 ('Bateria / controlador','1 de cada','Ensaio solar separado ate validar carregamento e protecoes'),
 ('LEDs e botoes restantes','Saldo do inventario','Disponiveis para sinalizacao e comandos adicionais'),
]

def geometria(p):
    L=p['piso_L']-2*p['margem_piso']; W=288.0
    # As fracoes permitem atualizar o envelope sem manter comprimento antigo.
    fx=L/697.5; fy=W/288.0
    walls=[]
    for code,axis,u,a,b in PAREDES:
        walls.append(dict(id=code,eixo=axis,u=u*(fy if axis=='H' else fx),
                          a=a*(fx if axis=='H' else fy),
                          b=b*(fx if axis=='H' else fy),classe='Anteprojeto'))
    openings=[]
    for code,wall,kind,a,w,z,h,cl in ABERTURAS:
        axis=next(k['eixo'] for k in walls if k['id']==wall)
        f=fx if axis=='H' else fy
        openings.append(dict(id=code,parede=wall,tipo=kind,a=a*f,w=w*f,z=z,h=h,classe=cl))
    rooms=[dict(id=c,nome=n,poligono=[(x*fx,y*fy) for x,y in poly],classe='Anteprojeto')
           for c,n,poly in AMBIENTES]
    return L,W,walls,openings,rooms

def area(poly):
    return abs(sum(poly[i][0]*poly[(i+1)%len(poly)][1]-
                   poly[(i+1)%len(poly)][0]*poly[i][1] for i in range(len(poly))))/2

def numero(n):
    return f'{n:.2f}'.rstrip('0').rstrip('.').replace('.',',')

def medidas_ambiente(room,fator=1):
    pts=room['poligono']
    dx=max(x for x,y in pts)-min(x for x,y in pts)
    dy=max(y for x,y in pts)-min(y for x,y in pts)
    if room['id']=='AM01':
        return (f'{numero(dx*fator)} x {numero(143.5*fator)} + '
                f'{numero(98.5*fator)} x {numero(138.5*fator)}')
    return f'{numero(dx*fator)} x {numero(dy*fator)}'

def quadro(headers,rows,widths=None):
    c=Cena();widths=widths or [1100/len(headers)]*len(headers)
    xs=[0]
    for w in widths:xs.append(xs[-1]+w)
    h=40;top=h*(len(rows)+1)
    c.ret(0,0,xs[-1],top,'DESENHO')
    for x in xs[1:-1]:c.linha((x,0),(x,top),'COTAS')
    for j in range(1,len(rows)+1):c.linha((0,j*h),(xs[-1],j*h),'COTAS')
    for i,title in enumerate(headers):c.texto(xs[i]+8,top-20,title,7,'TEXTO','left')
    for j,values in enumerate(rows):
        for i,value in enumerate(values):c.texto(xs[i]+8,top-(j+1.5)*h,str(value),7,'TEXTO','left')
    return c

def quadro_ambientes(p,model):
    rows=[]
    for r in model[4]:
        rows.append([r['id'],r['nome'],medidas_ambiente(r),
                     medidas_ambiente(r,p['escala_maquete']),
                     numero(area(r['poligono'])*p['escala_maquete']**2/1e6)])
    return quadro(['ID','AMBIENTE','MAQUETE: C x L (mm)','ARQUITETURA: C x L (mm)','AREA (m2)'],
                  rows,[65,215,310,350,110])

def quadro_aberturas(p,model):
    return quadro(['ID','TIPO','L x H / MAQUETE (mm)','L x H / ARQUITETURA (mm)','PEITORIL / MAQUETE (mm)'],
          [[o['id'],o['tipo'].upper(),f'{numero(o["w"])} x {numero(o["h"])}',
            f'{numero(o["w"]*p["escala_maquete"])} x {numero(o["h"]*p["escala_maquete"])}',numero(o['z'])]
           for o in model[3]],[65,180,270,310,225])

def validar(p,model):
    L,W,walls,ops,rooms=model
    if p['piso_L']<=2*p['margem_piso'] or p['piso_W']<W:
        raise ValueError('Envelope do piso incompativel com as paredes.')
    ids={w['id'] for w in walls}
    if len(ids)!=len(walls):raise ValueError('Codigo de parede repetido.')
    for op in ops:
        if op['parede'] not in ids:raise ValueError('Abertura sem parede.')
        wall=next(w for w in walls if w['id']==op['parede'])
        if not(wall['a']<=op['a'] and op['a']+op['w']<=wall['b']):
            raise ValueError('Abertura fora da parede: '+op['id'])
        if op['z']<0 or op['z']+op['h']>p['parede_H']:
            raise ValueError('Altura de abertura invalida: '+op['id'])
    for room in rooms:
        if area(room['poligono'])<=0:raise ValueError('Ambiente sem area.')
    if p['casa_x']+p['piso_L']>p['base_L'] or p['casa_y']+p['piso_W']>p['base_W']:
        raise ValueError('A casa nao cabe na base proposta.')
    boxes=[(p['casa_x'],p['casa_y'],p['piso_L'],p['piso_W']),
           (p['central_x'],p['central_y'],p['central_L'],p['central_W']),
           (p['agua_x'],p['agua_y'],p['agua_L'],p['agua_W'])]
    for x,y,w,h in boxes:
        if min(x,y)<0 or x+w>p['base_L'] or y+h>p['base_W']:
            raise ValueError('Uma reserva de espaco ultrapassa a base.')
    for i,a in enumerate(boxes):
        for b in boxes[i+1:]:
            if not(a[0]+a[2]<=b[0] or b[0]+b[2]<=a[0] or
                   a[1]+a[3]<=b[1] or b[1]+b[3]<=a[1]):
                raise ValueError('Sobreposicao entre casa, central e area de agua.')

# Motor vetorial comum: PDF e DXF recebem as mesmas primitivas.
class Cena:
    def __init__(self):self.itens=[]
    def linha(self,a,b,layer='DESENHO'):self.itens.append(('linha',a,b,layer))
    def poli(self,pts,layer='DESENHO',fill=None,fechar=True):
        self.itens.append(('poli',pts,layer,fill,fechar))
    def ret(self,x,y,w,h,layer='DESENHO',fill=None):
        self.poli([(x,y),(x+w,y),(x+w,y+h),(x,y+h)],layer,fill)
    def texto(self,x,y,text,pt=8,layer='TEXTO',align='center'):
        self.itens.append(('texto',x,y,str(text),pt,layer,align))
    def circulo(self,x,y,r,layer='SISTEMAS'):self.itens.append(('circulo',x,y,r,layer))
    def cota(self,a,b,off=18,vertical=False,label=None,classe='Anteprojeto'):
        x1,y1=a;x2,y2=b
        if vertical:
            x=min(x1,x2)-off;lo,hi=sorted((y1,y2))
            self.linha((x1,y1),(x-3,y1),'COTAS');self.linha((x2,y2),(x-3,y2),'COTAS')
            self.linha((x,lo),(x,hi),'COTAS')
            for yy in [lo,hi]:self.linha((x-2,yy-2),(x+2,yy+2),'COTAS')
            self.texto(x-5,(lo+hi)/2,label or f'{hi-lo:g}',7,'COTAS','right')
        else:
            y=min(y1,y2)-off;lo,hi=sorted((x1,x2))
            self.linha((x1,y1),(x1,y-3),'COTAS');self.linha((x2,y2),(x2,y-3),'COTAS')
            self.linha((lo,y),(hi,y),'COTAS')
            for xx in [lo,hi]:self.linha((xx-2,y-2),(xx+2,y+2),'COTAS')
            self.texto((lo+hi)/2,y+4,label or f'{hi-lo:g}',7,'COTAS')
    def bloco(self,other,dx=0,dy=0,f=1):
        for it in other.itens:
            k=it[0]
            if k=='linha':self.linha((it[1][0]*f+dx,it[1][1]*f+dy),(it[2][0]*f+dx,it[2][1]*f+dy),it[3])
            elif k=='poli':self.poli([(x*f+dx,y*f+dy) for x,y in it[1]],it[2],it[3],it[4])
            elif k=='texto':self.texto(it[1]*f+dx,it[2]*f+dy,it[3],it[4],it[5],it[6])
            elif k=='circulo':self.circulo(it[1]*f+dx,it[2]*f+dy,it[3]*f,it[4])

def partes(a,b,aberturas):
    cursor=a
    for op in sorted(aberturas,key=lambda q:q['a']):
        if op['a']>cursor:yield cursor,op['a']
        cursor=max(cursor,op['a']+op['w'])
    if cursor<b:yield cursor,b

def planta(p,model,nomes=True,codigos=False):
    L,W,walls,ops,rooms=model;c=Cena();t=p['mdf']
    for wall in walls:
        own=[o for o in ops if o['parede']==wall['id']]
        for a,b in partes(wall['a'],wall['b'],own):
            if wall['eixo']=='H':c.ret(a,wall['u']-t/2,b-a,t,'PAREDES','#e5e7eb')
            else:c.ret(wall['u']-t/2,a,t,b-a,'PAREDES','#e5e7eb')
        if codigos:
            x,y=((wall['a']+wall['b'])/2,wall['u']) if wall['eixo']=='H' else (wall['u'],(wall['a']+wall['b'])/2)
            c.texto(x,y+7,wall['id'],6,'PAREDES')
        for op in own:
            a,b=op['a'],op['a']+op['w'];u=wall['u']
            if op['tipo']=='porta':
                if wall['eixo']=='H':
                    direction=-1 if wall['id'] in ('R05','R06','R10','R17') else 1
                    c.linha((a,u),(a,u+direction*op['w']),'ABERTURAS')
                    pts=[(a+op['w']*math.cos(j*math.pi/40),u+direction*op['w']*math.sin(j*math.pi/40)) for j in range(21)]
                else:
                    c.linha((u,a),(u+op['w'],a),'ABERTURAS')
                    pts=[(u+op['w']*math.cos(j*math.pi/40),a+op['w']*math.sin(j*math.pi/40)) for j in range(21)]
                c.poli(pts,'ABERTURAS',fechar=False)
            elif wall['eixo']=='H':
                c.linha((a,u),(b,u),'ABERTURAS')
                c.linha((a,u-1),(b,u-1),'ABERTURAS')
            else:
                c.linha((u,a),(u,b),'ABERTURAS')
                c.linha((u-1,a),(u-1,b),'ABERTURAS')
    if nomes:
        for room in rooms:
            pts=room['poligono'];x=(min(q[0] for q in pts)+max(q[0] for q in pts))/2
            y=(min(q[1] for q in pts)+max(q[1] for q in pts))/2
            # Texto da sala colocado fora do recuo da cozinha.
            if room['id']=='AM01':x=65;y=130
            c.texto(x,y+5,room['id'],6,'PROPOSTO')
            c.texto(x,y-5,room['nome'],6,'PROPOSTO')
    return c

def planta_cotada(p,model,fator=1):
    c=planta(p,model,nomes=False);L,W,walls,ops,rooms=model
    for r in rooms:
        pts=r['poligono'];x=(min(q[0] for q in pts)+max(q[0] for q in pts))/2
        y=(min(q[1] for q in pts)+max(q[1] for q in pts))/2
        if r['id']=='AM01':x=62;y=100
        if r['id'] in ('AM03','AM04','AM08','AM09'):y=28
        if r['id']=='AM05':y=132
        if r['id']=='AM10':y=177
        c.texto(x,y+11,r['id']+' - '+r['nome'],6,'TEXTO')
        if r['id']=='AM01':
            a,b=medidas_ambiente(r,fator).split(' + ')
            c.texto(x,y,a+' mm',6,'TEXTO');c.texto(x,y-11,'+ '+b+' mm',6,'TEXTO')
        else:c.texto(x,y-2,medidas_ambiente(r,fator)+' mm',6,'TEXTO')
    for a,b in zip([0,214,304,511],[214,304,511,L]):
        c.cota((a,0),(b,0),28,label=numero((b-a)*fator))
    c.cota((0,0),(L,0),57,label=numero(L*fator)+' mm')
    for a,b in [(0,94),(94,148),(148,W)]:
        c.cota((0,a),(0,b),32,True,label=numero((b-a)*fator))
    c.cota((0,0),(0,W),75,True,label=numero(W*fator)+' mm')
    c.linha((-12,120),(L+12,120),'CORTES')
    c.texto(-20,120,'A',7,'CORTES');c.texto(L+20,120,'A',7,'CORTES')
    c.linha((320,-8),(320,W+8),'CORTES')
    c.texto(320,W+17,'B',7,'CORTES');c.texto(320,-16,'B',7,'CORTES')
    return c

def planta_eletrica(p,model,modo='luz'):
    c=planta(p,model,nomes=False)
    for r in model[4]:
        pts=r['poligono'];x=sum(a for a,b in pts)/len(pts);y=sum(b for a,b in pts)/len(pts)
        c.texto(x,y-24,r['id'],6,'COTAS')
    if modo in ('luz','rotas'):
        for i,(code,room,x,y,res) in enumerate(PONTOS_LUZ):
            c.circulo(x,y,5,'ILUMINACAO')
            c.linha((x-3,y-3),(x+3,y+3),'ILUMINACAO');c.linha((x-3,y+3),(x+3,y-3),'ILUMINACAO')
            label_y=y-14 if room in ('AM03','AM04','AM08','AM09') else y+13
            c.texto(x,label_y,f'{code} / D{22+i}',6,'ILUMINACAO')
            if modo=='rotas':
                c.linha((x,y),(x,120),'CABOS');c.linha((x,120),(280,120),'CABOS')
        if modo=='luz':
            c.ret(20,-90,400,45,'SISTEMAS')
            c.texto(220,-62,'B1 LUZ | B2 BRISE | B3 AGUA | B4 ACESSO',7,'SISTEMAS')
            c.texto(220,-106,'COMANDOS LOCAIS NA CENTRAL',6,'SISTEMAS')
    if modo in ('sensores','rotas'):
        for code,name,x,y in SENSORES:
            c.ret(x-4,y-4,8,8,'SISTEMAS');c.texto(x,y+17,code+' '+name,6,'SISTEMAS')
            if modo=='rotas':
                c.linha((x,y),(x,112),'SINAIS');c.linha((x,112),(280,112),'SINAIS')
    if modo=='rotas':
        c.linha((280,120),(280,-35),'CABOS');c.linha((288,112),(288,-35),'SINAIS')
        c.texto(280,-50,'J1 - CENTRAL / SAIDA SOB O PISO',7,'SISTEMAS')
        c.texto(350,340,'LARANJA: LED | ROXO: RETORNOS | VERDE: SINAIS',7,'TEXTO')
    c.cota((0,0),(697.5,0),135,label='697,5 mm')
    return c

def diagrama_alimentacao():
    c=Cena()
    def box(x,y,w,h,lines):
        c.ret(x,y,w,h,'SISTEMAS','#f0f5f8')
        for i,line in enumerate(lines):c.texto(x+w/2,y+h/2+12*(len(lines)-1)/2-i*12,line,7,'TEXTO')
    box(0,260,170,70,['FONTE 12 V / 5 A','EXTERNA A MAQUETE'])
    box(0,110,170,70,['FONTE 5 V / 3 A','EXTERNA A MAQUETE'])
    box(230,260,190,70,['FUSIVEL / SECCIONAMENTO','CORTE DOS ATUADORES'])
    c.linha((170,295),(230,295),'POTENCIA')
    box(490,310,240,65,['12 V -> DRIVER -> BOMBA','DIODO EM PARALELO'])
    box(490,225,240,65,['12 V -> REGULADOR 6 V','DRIVER -> SOLENOIDE + DIODO'])
    for y in [342.5,257.5]:
        c.linha((420,295),(455,295),'POTENCIA');c.linha((455,295),(455,y),'POTENCIA');c.linha((455,y),(490,y),'POTENCIA')
    box(230,110,190,70,['DISTRIBUICAO 5 V','RETORNOS SEPARADOS'])
    c.linha((170,145),(230,145),'POTENCIA')
    box(490,125,240,65,['SENSORES / LEDS','MEGA POR USB REGULADO'])
    box(490,35,240,65,['REGULADOR 3,3 V -> RFID','ESP32: ENTRADA DA PLACA'])
    for y in [157.5,67.5]:
        c.linha((420,145),(455,145),'POTENCIA');c.linha((455,145),(455,y),'POTENCIA');c.linha((455,y),(490,y),'POTENCIA')
    box(800,140,240,90,['MEGA: CONTROLE 5 V','INTERFACE 5 V / 3,3 V','RFID / ESP32'])
    c.linha((730,157.5),(800,157.5),'SINAIS')
    box(800,35,240,65,['5 V -> CORTE -> SERVO','CONTATO DE EMERGENCIA'])
    for a,b in [((420,145),(440,145)),((440,145),(440,20)),((440,20),(780,20)),((780,20),(780,67.5)),((780,67.5),(800,67.5))]:c.linha(a,b,'POTENCIA')
    c.texto(520,-25,'GND EM ESTRELA: LOGICA, SENSORES E DRIVERS COM REFERENCIA COMUM',7,'TEXTO')
    c.texto(520,-48,'FONTES DC NAO SAO LIGADAS EM PARALELO; REDE AC FICA FORA DA MAQUETE',7,'TEXTO')
    c.texto(520,410,'FITA LED: RAMAL E DRIVER SOMENTE APOS CONFIRMAR TENSAO E CONSUMO',7,'TEXTO')
    return c

def diagrama_driver():
    c=Cena()
    # Driver MOSFET de lado baixo, sem atribuir componente nao identificado.
    c.linha((30,230),(420,230),'POTENCIA');c.texto(100,248,'+V DA CARGA',8,'POTENCIA')
    c.ret(225,140,100,50,'POTENCIA');c.texto(275,165,'BOMBA / BOBINA',7,'TEXTO')
    c.linha((275,230),(275,190),'POTENCIA');c.linha((275,140),(275,90),'POTENCIA')
    c.ret(225,40,100,50,'SISTEMAS');c.texto(275,65,'MOSFET / DRIVER',7,'TEXTO')
    c.linha((275,40),(275,0),'POTENCIA');c.texto(275,-15,'GND COMUM',7,'TEXTO')
    c.texto(25,65,'PINO MEGA',7,'TEXTO');c.linha((70,65),(120,65),'SINAIS')
    c.ret(120,59,50,12,'SINAIS');c.linha((170,65),(225,65),'SINAIS')
    c.texto(145,88,'100 ohm',6,'TEXTO')
    c.linha((195,65),(195,35),'SINAIS');c.ret(189,15,12,20,'SINAIS')
    c.linha((195,15),(195,0),'SINAIS');c.linha((195,0),(275,0),'SINAIS')
    c.texto(165,25,'10k',6,'TEXTO')
    c.linha((275,120),(420,120),'POTENCIA');c.linha((420,120),(420,166),'POTENCIA')
    c.linha((420,184),(420,230),'POTENCIA')
    c.ret(410,166,20,18,'POTENCIA');c.linha((405,190),(435,190),'POTENCIA')
    c.texto(420,175,'D1',6,'TEXTO')
    c.texto(460,190,'DIODO: CATODO EM +V',7,'TEXTO','left')
    c.texto(460,168,'ANODO NO LADO DO DRIVER',7,'TEXTO','left')
    c.texto(275,285,'TOPOLOGIA DE ACIONAMENTO EM CORRENTE CONTINUA',9,'TEXTO')
    c.texto(275,-48,'Dimensionar MOSFET, diodo e fusivel pela corrente de partida e regime.',7,'TEXTO')
    return c

def implantacao(p,model,sistemas=False):
    c=Cena();c.ret(0,0,p['base_L'],p['base_W'],'PROPOSTO','#fafafa')
    x,y=p['casa_x'],p['casa_y'];m=p['margem_piso']
    c.ret(x,y,p['piso_L'],p['piso_W'],'PISO','#ffffff')
    c.bloco(planta(p,model,nomes=False),x+m,y+m)
    c.texto(x+p['piso_L']/2,y+p['piso_W']+30,f'CASA INTELIGENTE - PISO {p["piso_L"]:g} x {p["piso_W"]:g} mm',8,'PISO')
    c.ret(p['central_x'],p['central_y'],p['central_L'],p['central_W'],'PROPOSTO','#edf4fa')
    c.texto(p['central_x']+p['central_L']/2,p['central_y']+p['central_W']/2,'CENTRAL DE CONTROLE',8,'PROPOSTO')
    c.ret(p['agua_x'],p['agua_y'],p['agua_L'],p['agua_W'],'AGUA','#e9f7fa')
    c.texto(p['agua_x']+p['agua_L']/2,p['agua_y']+p['agua_W']/2,'AGUA',8,'AGUA')
    c.ret(930,700,115,85,'SOLAR','#e7edf5');c.texto(987.5,805,'PAINEL SOLAR',7,'SOLAR')
    c.texto(600,850,'FRENTE / ORIENTACAO DE EXPOSICAO A DEFINIR',7,'PROPOSTO')
    c.cota((0,0),(p['base_L'],0),35,classe='P')
    c.cota((0,0),(0,p['base_W']),35,True,classe='P')
    if sistemas:
        spots=[('AC01',20,200),('PR01',90,140),('TH01',565,235),
               ('LU01',415,285),('BR01',415,305)]
        for label,sx,sy in spots:
            px,py=x+m+sx,y+m+sy
            c.circulo(px,py,9);c.texto(px,py+18,label,7,'SISTEMAS')
        c.texto(1015,330,'AG01 - CIRCUITO EXTERNO',7,'AGUA')
        c.texto(987.5,675,'FV01',8,'SOLAR')
    return c

def fachada(p,model,axis,side,fator=1):
    L,W,walls,ops,rooms=model;c=Cena();length=L if axis=='H' else W
    c.ret(0,-6,length,6,'PAREDES','#dddfe3')
    c.ret(0,0,length,p['parede_H'],'PAREDES')
    c.ret(-10,130,length+20,3,'PAREDES')
    c.ret(-10,133,length+20,20,'PAREDES')
    for wall in walls:
        if wall['eixo']!=axis or abs(wall['u']-side)>p['mdf']/2+0.01:continue
        for op in [o for o in ops if o['parede']==wall['id']]:
            c.ret(op['a'],op['z'],op['w'],op['h'],'ABERTURAS')
            c.texto(op['a']+op['w']/2,op['z']+op['h']+7,op['id'],6,'ABERTURAS')
            if op['tipo']=='janela':
                c.linha((op['a']+op['w']/2,op['z']),(op['a']+op['w']/2,op['z']+op['h']),'ABERTURAS')
    c.cota((0,0),(length,0),20,label=numero(length*fator))
    c.cota((length,0),(length,130),-25,True,label=numero(130*fator))
    return c

def corte(p,model,transversal=False,fator=1):
    L,W,walls,ops,rooms=model;c=Cena();length=W if transversal else L
    pos=320 if transversal else 120
    c.ret(0,-6,length,6,'PAREDES','#dddfe3')
    c.ret(-10,130,length+20,3,'PAREDES','#dddfe3')
    c.ret(-10,150,length+20,3,'PAREDES','#dddfe3')
    c.linha((-10,133),(-10,153),'PAREDES');c.linha((length+10,133),(length+10,153),'PAREDES')
    for w in walls:
        crossing=(w['eixo']=='H') if transversal else (w['eixo']=='V')
        if crossing and w['a']<=pos<=w['b']:
            own=[o for o in ops if o['parede']==w['id'] and o['a']<=pos<=o['a']+o['w']]
            if own:
                op=own[0]
                if op['z']>0:c.ret(w['u']-1.5,0,3,op['z'],'PAREDES','#bbbbbb')
                c.ret(w['u']-1.5,op['z']+op['h'],3,130-op['z']-op['h'],'PAREDES','#bbbbbb')
            else:c.ret(w['u']-1.5,0,3,130,'PAREDES','#bbbbbb')
    c.cota((0,0),(length,0),20,label=numero(length*fator))
    c.cota((length,0),(length,130),-25,True,label=numero(130*fator))
    c.texto(length/2,175,'LAJE E COBERTURA',7,'PAREDES')
    return c

def cobertura(p):
    L,W=p['piso_L'],p['piso_W'];a=COBERTURA['divisao_T1'];b=COBERTURA['divisao_T2'];d=COBERTURA['recuo']
    c=Cena();c.poli([(0,0),(a,0),(a,d),(b,d),(b,0),(L,0),(L,W),(0,W)],'PAREDES','#f4f4f4')
    for xx in [a,b]:c.linha((xx,d),(xx,W),'PAREDES')
    for name,x in [('T1',a/2),('T2',(a+b)/2),('T3',(b+L)/2)]:c.texto(x,180,name+'',12,'PAREDES')
    c.texto(L/2,-35,'COBERTURA EM TRES PAINEIS',8,'PAREDES')
    c.texto(L/2,-55,'PREVER ACESSO PARA MANUTENCAO DOS SISTEMAS',7,'PISO')
    return c

def automacao_sugerida():
    c=Cena();width=1150;row=48;top=432
    cols=[0,85,330,650,width]
    c.ret(0,0,width,top,'SISTEMAS')
    for x in cols[1:-1]:c.linha((x,0),(x,top),'SISTEMAS')
    for y in range(48,433,48):c.linha((0,y),(width,y),'SISTEMAS')
    for x,label in [(8,'ID'),(93,'FUNCAO SUGERIDA'),(338,'COMPONENTES'),(658,'DEFINICAO COM A EQUIPE')]:
        c.texto(x,408,label,7,'SISTEMAS','left')
    rows=[
      ('IL01','Iluminacao automatica','LEDs brancos','Definir ambientes, pontos e modos de uso.'),
      ('LU01','Leitura de luminosidade','LDR KY-018','Definir limiar e relacao com a iluminacao.'),
      ('BR01','Movimento do brise','Microservo 9 g','Definir suporte, curso e janela de instalacao.'),
      ('PR01','Deteccao de presenca','PIR SR-501','Definir area de deteccao e tempo de resposta.'),
      ('TH01','Temperatura e umidade','DHT22','Definir local e forma de apresentar as leituras.'),
      ('AC01','Controle de acesso','RFID RC522 / solenoide 6 V','Definir fixacao e demonstracao da abertura.'),
      ('AG01','Recirculacao de agua','Bomba 12 V / sensor de vazao','Definir retorno, reservatorio e mangueiras.'),
      ('FV01','Demonstracao solar','Painel / controlador / bateria','Definir experimento e compatibilidade do conjunto.')]
    for i,values in enumerate(rows):
        y=360-i*row
        for x,value in zip([8,93,338,658],values):c.texto(x,y,value,7,'TEXTO','left')
    return c

def central(p):
    c=Cena();W,D=p['central_L'],p['central_W'];c.ret(0,0,W,D,'PROPOSTO')
    for code,name,x,y,w,h in COMPONENTES:
        yy=60
        c.ret(x,yy,w,h,'SISTEMAS','#edf4fa');c.texto(x+w/2,yy+h/2,code,8,'SISTEMAS')
    for x,label in [(50,'EMERG'),(160,'LUZ'),(240,'BRISE'),(320,'AGUA'),(400,'ACESSO')]:
        c.circulo(x,25,8);c.texto(x,7,label,6,'SISTEMAS')
    c.texto(W/2,D+20,'RESERVAS DE ESPACO; MEDIR PLACAS, BORNES E CONECTORES',8,'PROPOSTO')
    c.cota((0,0),(W,0),20,classe='P');c.cota((0,0),(0,D),20,True,classe='P')
    return c

def hidraulica():
    c=Cena()
    for x,y,w,h,label in [(0,0,170,130,'RESERVATORIO'),(210,30,95,65,'BOMBA'),(350,35,110,55,'VAZAO')]:
        c.ret(x,y,w,h,'AGUA','#eef9fb');c.texto(x+w/2,y+h/2,label,9,'AGUA')
    path=[(170,65),(210,65),(305,65),(350,65),(460,65),(490,65),(490,180),(80,180),(80,130)]
    for a,b in zip(path,path[1:]):c.linha(a,b,'AGUA')
    c.texto(260,205,'RECIRCULACAO EM BANDEJA SEPARADA DA ELETRONICA',8,'AGUA')
    c.texto(260,-30,'MANGUEIRAS, CONEXOES E FIXACOES A MEDIR',7,'AGUA')
    return c

CORES={'DESENHO':'#182c40','PISO':'#182c40','PAREDES':'#182c40',
        'PROPOSTO':'#365b79','COTAS':'#51606b','TEXTO':'#243747',
        'ABERTURAS':'#425568','SISTEMAS':'#17665e','ILUMINACAO':'#a87505',
        'CABOS':'#765398','AGUA':'#187898','SOLAR':'#34577b',
        'SINAIS':'#148469','POTENCIA':'#b54b2a','CORTES':'#8c9299'}

def exportar_dxf(cena,path,scale_dxf=1,paper_scale=1):
    import ezdxf
    from ezdxf.enums import TextEntityAlignment
    doc=ezdxf.new('R2010');doc.units=ezdxf.units.MM;doc.header['$MEASUREMENT']=1
    for name in CORES:
        doc.layers.new(name,dxfattribs={'color':7 if name=='DESENHO' else 8})
    m=doc.modelspace();f=scale_dxf
    for it in cena.itens:
        k=it[0]
        if k=='linha':m.add_line((it[1][0]*f,it[1][1]*f),(it[2][0]*f,it[2][1]*f),dxfattribs={'layer':it[3]})
        elif k=='poli':m.add_lwpolyline([(x*f,y*f) for x,y in it[1]],close=it[4],dxfattribs={'layer':it[2]})
        elif k=='circulo':m.add_circle((it[1]*f,it[2]*f),it[3]*f,dxfattribs={'layer':it[4]})
        elif k=='texto':
            align={'center':TextEntityAlignment.MIDDLE_CENTER,'left':TextEntityAlignment.MIDDLE_LEFT,'right':TextEntityAlignment.MIDDLE_RIGHT}[it[6]]
            m.add_text(it[3],dxfattribs={'height':it[4]*0.352778/max(paper_scale,0.001)*f,'layer':it[5]}).set_placement((it[1]*f,it[2]*f),align=align)
    doc.saveas(path)

def gerar(p=None,pasta=None):
    dependencias()
    from reportlab.pdfgen import canvas
    from reportlab.lib.colors import HexColor
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    p=dict(PARAM if p is None else p);model=geometria(p);validar(p,model)
    root=Path(pasta or ('/content/NEXUS_CASA_INTELIGENTE_EXPOTECH_R02' if Path('/content').exists() else 'NEXUS_CASA_INTELIGENTE_EXPOTECH_R02'))
    root.mkdir(parents=True,exist_ok=True)
    for name in ['PDF','DXF','DADOS']:(root/name).mkdir(exist_ok=True)
    font='Helvetica'
    for fp in ['/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf','/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf']:
        if Path(fp).exists():pdfmetrics.registerFont(TTFont('Nexus',fp));font='Nexus';break
    mm=72/25.4;pw,ph=420*mm,297*mm
    pdf=canvas.Canvas(str(root/'PDF'/'NEXUS_Casa_Inteligente_ExpoTech_Plantas.pdf'),pagesize=(pw,ph))
    pdf.setTitle(PROJETO+' - Plantas')
    def cabecalho(code,title,scale,unit):
        pdf.setFillColor(HexColor('#182c40'))
        pdf.setStrokeColor(HexColor('#1b3c53'));pdf.setLineWidth(.8)
        pdf.rect(10*mm,10*mm,400*mm,277*mm)
        title_pt=min(16,375*mm/max(pdfmetrics.stringWidth(title,font,16),1)*16)
        pdf.setFont(font,title_pt);pdf.drawString(17*mm,275*mm,title)
        pdf.setFont(font,8);pdf.drawString(17*mm,267*mm,PROJETO+' | '+code+' | '+REVISAO)
        pdf.line(10*mm,258*mm,410*mm,258*mm)
        pdf.setFont(font,7)
        for yy,txt in [(26,'Anteprojeto | Dimensoes e distribuicao sujeitas a compatibilizacao no detalhamento.'),
                       (21,PROJETO),
                       (16,f'{unit} | {scale}')]:
            pdf.drawString(17*mm,yy*mm,txt)
        pdf.setFont(font,9);pdf.drawRightString(402*mm,16*mm,code)
    def render(cena,box):
        # box em mm de papel: esquerda, inferior, largura, altura.
        xs=[];ys=[]
        for it in cena.itens:
            if it[0]=='linha':pts=[it[1],it[2]]
            elif it[0]=='poli':pts=it[1]
            elif it[0]=='circulo':pts=[(it[1]-it[3],it[2]-it[3]),(it[1]+it[3],it[2]+it[3])]
            else:pts=[(it[1],it[2])]
            xs.extend(q[0] for q in pts);ys.extend(q[1] for q in pts)
        lo,bo,hi,to=min(xs),min(ys),max(xs),max(ys)
        bx,by,bw,bh=box
        s=min((bw-16)/(hi-lo or 1),(bh-16)/(to-bo or 1))
        initial=(lo,bo,hi,to)
        for _ in range(12):
            lo,bo,hi,to=initial
            for it in cena.itens:
                if it[0]!='texto':continue
                w=pdfmetrics.stringWidth(it[3],font,it[4])/(s*mm)
                x,y=it[1],it[2]
                left=x if it[6]=='left' else x-w if it[6]=='right' else x-w/2
                lo=min(lo,left);hi=max(hi,left+w)
                bo=min(bo,y-it[4]*.35/(s*mm));to=max(to,y+it[4]/(s*mm))
            new=min((bw-16)/(hi-lo or 1),(bh-16)/(to-bo or 1))
            if abs(new-s)<1e-7:break
            s=new
        ox=(bx+bw/2-(hi+lo)*s/2)*mm;oy=(by+bh/2-(to+bo)*s/2)*mm
        def point(q):return ox+q[0]*s*mm,oy+q[1]*s*mm
        for it in cena.itens:
            k=it[0];layer=it[3] if k=='linha' else it[2] if k=='poli' else it[4] if k=='circulo' else it[5]
            pdf.setStrokeColor(HexColor(CORES.get(layer,'#182c40')));pdf.setFillColor(HexColor(CORES.get(layer,'#182c40')))
            pdf.setLineWidth(.65 if layer=='PAREDES' else .4)
            if k=='linha':pdf.line(*point(it[1]),*point(it[2]))
            elif k=='poli':
                path=pdf.beginPath();path.moveTo(*point(it[1][0]))
                for q in it[1][1:]:path.lineTo(*point(q))
                if it[4]:path.close()
                if it[3]:pdf.setFillColor(HexColor(it[3]))
                pdf.drawPath(path,stroke=1,fill=bool(it[3]))
            elif k=='circulo':pdf.circle(*point((it[1],it[2])),it[3]*s*mm,stroke=1,fill=0)
            else:
                pdf.setFont(font,it[4]);x,y=point((it[1],it[2]))
                {'center':pdf.drawCentredString,'left':pdf.drawString,'right':pdf.drawRightString}[it[6]](x,y-2,it[3])
        return s
    sheets=[]
    def folha(code,title,cena,unit='mm da maquete',f=1,notas=()):
        cabecalho(code,title,'Escala grafica de ajuste a folha; CAD em tamanho real',unit)
        s=render(cena,(20,78,380,168))
        pdf.setFont(font,7);pdf.setFillColor(HexColor('#243747'))
        for i,txt in enumerate(notas):pdf.drawString(22*mm,(66-i*5)*mm,txt)
        if unit=='esquematico':
            scale_note='Diagrama / quadro sem escala. Dimensoes somente onde indicadas.'
        else:
            scale_note=f'Escala desta vista: 1:{f/s:.2f} | Imprimir A3 a 100% | Cotas em mm.'
            cota_mm=100 if f==1 else 2000
            pdf.line(22*mm,47*mm,(22+cota_mm/f*s)*mm,47*mm)
            for xx in [22,22+cota_mm/f*s]:pdf.line(xx*mm,45*mm,xx*mm,49*mm)
            pdf.setFont(font,6);pdf.drawString(22*mm,51*mm,f'{numero(cota_mm)} mm')
        pdf.setFont(font,7);pdf.drawString(22*mm,39*mm,scale_note)
        exportar_dxf(cena,root/'DXF'/f'{code}.dxf',f,s)
        sheets.append(dict(codigo=code,titulo=title,unidades=unit,escala_impressao=f/s))
        pdf.showPage()
    L,W,walls,ops,rooms=model;f=p['escala_maquete']
    folha('A01','PLANTA BAIXA ARQUITETONICA - COTAS EM mm',planta_cotada(p,model,f),
          'mm da representacao arquitetonica',f,notas=[
          'Cotas livres indicadas nos ambientes; cadeias externas referem-se a posicao das paredes.',
          'Circulacao: 5880 x 1020 mm. Hall: 1740 x 2710 mm. Sala em L: duas parcelas cotadas.',
          'Escala dimensional 1:20 entre arquitetura e maquete; paredes de 3 mm equivalem a 60 mm.'])
    folha('M01','PLANTA DA MAQUETE - COTAS EM mm',planta_cotada(p,model),notas=[
          'Medidas livres dos comodos em milimetros da maquete.',
          'Circulacao: 294 x 51 mm. Hall: 87 x 135,5 mm. A01 apresenta a conversao arquitetonica.'])
    folha('M02','IMPLANTACAO DA CASA E DO CONJUNTO',implantacao(p,model),notas=[
          'Base de exposicao proposta: 1200 x 900 x 18 mm. Piso da casa: 717,5 x 308 mm.',
          'Central frontal; circuito de agua e experimento solar externos a casa. Fontes e bateria sob a mesa.',
          'Espessura e reforcos da base serao compatibilizados com o peso total e os pontos de apoio.'])
    roof=cobertura(p)
    roof.cota((0,0),(p['piso_L'],0),85,label=numero(p['piso_L']*f))
    roof.cota((0,0),(0,p['piso_W']),30,True,label=numero(p['piso_W']*f))
    folha('A02','PLANTA DE COBERTURA',roof,'mm da representacao arquitetonica',f,notas=[
          'Cobertura dividida em tres paineis; acesso aos equipamentos e a laje inferior.',
          'Divisoes, recuo e acesso de manutencao em compatibilizacao.'])
    for code,title,views in [
      ('A03','FACHADAS PRINCIPAL E LATERAL A',[(fachada(p,model,'V',0,f),'FACHADA PRINCIPAL'),(fachada(p,model,'H',288,f),'FACHADA LATERAL A')]),
      ('A04','FACHADAS POSTERIOR E LATERAL B',[(fachada(p,model,'V',L,f),'FACHADA POSTERIOR'),(fachada(p,model,'H',0,f),'FACHADA LATERAL B')]),
      ('A05','CORTES LONGITUDINAL E TRANSVERSAL',[(corte(p,model,False,f),'CORTE A-A'),(corte(p,model,True,f),'CORTE B-B')])]:
        cabecalho(code,title,'Escalas indicadas por vista','mm da representacao arquitetonica')
        scales=[]
        for i,(view,label) in enumerate(views):
            box=(22,155 if i==0 else 57,376,88);scale=render(view,box);scales.append(f/scale)
            pdf.setFillColor(HexColor('#182c40'));pdf.setFont(font,8)
            pdf.drawString(25*mm,(249 if i==0 else 151)*mm,label+f' | 1:{f/scale:.2f} | mm')
            exportar_dxf(view,root/'DXF'/f'{code}_{i+1}.dxf',f,scale)
        pdf.setFont(font,7);pdf.drawString(22*mm,40*mm,'Alturas e aberturas em milimetros; linhas dos cortes A-A e B-B indicadas nas plantas baixas.')
        sheets.append(dict(codigo=code,titulo=title,unidades='mm da representacao arquitetonica',escala_impressao=scales))
        pdf.showPage()
    folha('A06','QUADRO DE DIMENSOES E AREAS',quadro_ambientes(p,model),'esquematico',notas=[
          'C x L: dimensoes livres no sistema de eixos da planta. Sala em L: soma de duas parcelas retangulares.',
          'Areas calculadas pelos poligonos dos ambientes; nao incluem espessuras das paredes.',
          'Todas as dimensoes lineares estao em mm. Areas da representacao arquitetonica em m2.'])
    folha('A07','QUADRO DE PORTAS, JANELAS E VENEZIANAS',quadro_aberturas(p,model),'esquematico',notas=[
          'L x H: largura e altura. Peitoril medido a partir do piso.',
          'Codigos das aberturas repetidos nas fachadas; posicoes e dimensoes em compatibilizacao.'])
    names={r['id']:r['nome'] for r in rooms}
    folha('A08','ADJACENCIAS E CIRCULACAO ENTRE AMBIENTES',quadro(
          ['ORIGEM','DESTINO','LIGACAO'],
          [[a+' '+names.get(a,''),b+' '+names.get(b,''),op] for a,b,op in ADJACENCIAS],
          [420,420,310]),'esquematico',notas=[
          'Relacoes de acesso consideradas na distribuicao dos ambientes e das automacoes.',
          'Os usos dos ambientes podem ser ajustados sem alterar os codigos de identificacao.'])
    folha('M03','CENTRAL DE CONTROLE - DISTRIBUICAO FISICA',central(p),notas=[
          'Tampo proposto: 740 x 170 mm. Reservas incluem margens para placas e conexoes.',
          'Medir placas, bornes e conectores antes de definir furacoes. Separar retornos de cargas e sinais.'])
    folha('S01','AUTOMACAO - FUNCOES E DISCUSSAO COM A EQUIPE',quadro(
          ['ID','FUNCAO','COMPONENTES','DECISAO DE INTEGRACAO'],
          [[code,fun,comp,{
          'IL01':'Pontos e modos de comando em E01 / E02',
          'LU01':'Limiar e relacao com luz e brise',
          'BR01':'Suporte independente; janela J04',
          'PR01':'Cobertura de deteccao na sala',
          'TH01':'Local de leitura e exibicao de dados',
          'AC01':'RFID e solenoide na porta P01',
          'AG01':'Recirculacao fora da eletronica',
          'FV01':'Ensaio solar independente',
          'NI01':'HC-SR04 acima do reservatorio',
          'BT01':'Comandos locais na central'}[code]] for code,fun,comp,cl in SISTEMAS],
          [65,225,360,450]),'esquematico',notas=[
          'Mega como controlador principal; ESP32 reservado para comunicacao e supervisao.',
          'Funcoes propostas para desenvolvimento com a equipe. Ver circuitos e reservas em E04 a E08.'])
    folha('S02','CIRCUITO DEMONSTRATIVO DE AGUA',hidraulica(),'esquematico',notas=[
          'Reservatorio, bomba RS-385, sensor de vazao e retorno em bandeja independente.',
          'HC-SR04 proposto sobre o reservatorio para leitura de nivel; nao identifica vazamentos.',
          'Volume, tubulacoes, conexoes e fixacoes serao definidos conforme as pecas reais.'])
    folha('E01','PLANTA ELETRICA - ILUMINACAO E COMANDOS',planta_eletrica(p,model,'luz'),notas=[
          'Simbolo circular com cruz: LED. L01-L11: pontos individuais; D22-D32: comandos do Mega.',
          'Cotas e coordenadas em mm da maquete. Cada LED tem resistor individual; sem cargas de potencia nos pinos.',
          'B1-B4: comandos locais na central. Esta planta representa os circuitos DC da maquete.'])
    folha('E02','PLANTA ELETRICA - SENSORES E ATUADORES',planta_eletrica(p,model,'sensores'),notas=[
          'PR01: PIR. TH01: DHT22. LU01: LDR. AC01: RFID e solenoide. BR01: microservo.',
          'AG01 e NI01 ficam na bandeja de agua externa a casa. Touch e botoes ficam na central.',
          'Coordenadas de locacao e alturas de referencia constam nas tabelas do pacote.'])
    folha('E03','PLANTA ELETRICA - PERCURSOS E CONEXOES',planta_eletrica(p,model,'rotas'),notas=[
          'Percursos de estudo no piso e sob a laje. Prever conectores para partes removiveis.',
          'Linhas representam trajetos de feixes, sem unir os canais individuais. J1: saida para a central.',
          'Comprimentos de cabo: estimativas com folga de 30%; bitolas dependem de corrente e queda de tensao.'])
    folha('E04','DISTRIBUICAO ELETRICA E ALIMENTACAO',diagrama_alimentacao(),'esquematico',notas=[
          'Arquitetura funcional DC: fontes externas, ramais protegidos e referencia comum de GND.',
          'Bomba e solenoide com driver e diodo; servo com alimentacao externa. Nao alimentar cargas pelos GPIO.',
          'Reguladores, fusivel e corte de atuadores precisam ser dimensionados com as correntes reais.'])
    folha('E05','QUADRO DE CIRCUITOS E TENSAO',quadro(
          ['CIRC.','CARGA / FUNCAO','ALIMENTACAO','COMANDO','CONSIDERACAO'],CIRCUITOS,
          [70,290,190,220,410]),'esquematico',notas=[
          'C09 e um ensaio independente: nao se presume que o painel solar alimente as demais cargas.',
          'Consumos nao informados no inventario dependem de medicao antes do dimensionamento final.'])
    folha('E06','MAPA DE PINOS - ILUMINACAO E ATUADORES',quadro(
          ['FUNCAO','PINO MEGA','TIPO','LIGACAO / INTERFACE'],PINAGEM[:20],
          [170,190,260,550]),'esquematico',notas=[
          'Reservas de pinos propostas sem repeticao de canais. Pinos de controle nao fornecem a potencia das cargas.',
          'LEDs: cinco resistores de 470 ohm, cinco de 560 ohm e um de 1000 ohm, um por ponto.'])
    folha('E07','MAPA DE PINOS - SENSORES E COMUNICACAO',quadro(
          ['FUNCAO','PINO MEGA','TIPO','LIGACAO / INTERFACE'],PINAGEM[20:],
          [170,190,260,550]),'esquematico',notas=[
          'RFID e ESP32 usam interfaces de nivel compativeis com logica de 3,3 V.',
          'Mega opera com logica de 5 V. Nao ligar diretamente sinais de 5 V em entradas de 3,3 V.'])
    folha('E08','ACIONAMENTO DE CARGAS E PROTECAO',diagrama_driver(),'esquematico',notas=[
          'Topologia de driver de lado baixo: MOSFET logic level adequado a Vgs de 5 V.',
          'Bomba: carga em 12 V. Solenoide: carga em 6 V. Catodo do diodo no positivo da carga.',
          'Fita LED requer identificacao previa; o driver do diagrama nao substitui modulo enderecavel, se houver.'])
    folha('E09','COMPLEMENTOS PARA A MONTAGEM ELETRICA',quadro(
          ['ITEM','APLICACAO / QUANTIDADE','DEFINICAO'],COMPLEMENTOS,
          [245,300,605]),'esquematico',notas=[
          'Os itens deste quadro ainda nao estao confirmados no inventario detalhado.',
          'Identificar o conteudo do lote de componentes antes de comprar complementos.'])
    folha('E10','RESERVAS E COMPONENTES A INTEGRAR',quadro(
          ['COMPONENTE','DISPONIBILIDADE','ENCAMINHAMENTO'],RESERVAS,
          [230,270,650]),'esquematico',notas=[
          'As cameras OV7670 permanecem reservadas ate definir captura, memoria e interface com o controlador.',
          'O botao de emergencia deve atuar no corte fisico das cargas; a leitura D3 e somente monitoramento.'])
    pdf.save()
    dados=dict(projeto=PROJETO,revisao=REVISAO,parametros=p,paredes=walls,
               aberturas=ops,ambientes=rooms,cobertura=COBERTURA,
               sistemas=SISTEMAS,pranchas=sheets,
               etapa='Anteprojeto',
               projeto_eletrico='Anteprojeto dos circuitos DC da maquete', pinagem=PINAGEM, circuitos=CIRCUITOS, adjacencias=ADJACENCIAS,
               estado='Dimensoes e distribuicao sujeitas a compatibilizacao no detalhamento')
    (root/'DADOS'/'NEXUS_Casa_Inteligente_ExpoTech.json').write_text(json.dumps(dados,ensure_ascii=False,indent=2),encoding='utf8')
    def tabela(name,heads,rows):
        with (root/'DADOS'/name).open('w',encoding='utf-8-sig',newline='') as f:
            writer=csv.writer(f,delimiter=';');writer.writerow(heads);writer.writerows(rows)
    tabela('Ambientes_Areas_Estimadas.csv',['id','uso_proposto','area_maquete_mm2','area_equivalente_m2','estado'],
           [(r['id'],r['nome'],round(area(r['poligono']),2),round(area(r['poligono'])*f*f/1e6,3),'Anteprojeto') for r in rooms])
    tabela('Dimensoes_Ambientes_mm.csv',
           ['id','ambiente','C_x_L_maquete_mm','C_x_L_arquitetura_mm','estado'],
           [(r['id'],r['nome'],medidas_ambiente(r),medidas_ambiente(r,f),'Anteprojeto') for r in rooms])
    tabela('Aberturas.csv',['id','parede','tipo','inicio_mm','largura_mm','peitoril_mm','altura_mm','estado'],
           [(o['id'],o['parede'],o['tipo'],o['a'],o['w'],o['z'],o['h'],o['classe']) for o in ops])
    tabela('Pranchas.csv',['codigo','titulo','unidades','escala_impressao'],
           [(s['codigo'],s['titulo'],s['unidades'],s['escala_impressao']) for s in sheets])
    tabela('Circuitos.csv',['id','funcao','alimentacao','comando','consideracao'],CIRCUITOS)
    tabela('Pinagem_Mega.csv',['funcao','pino','tipo','interface'],PINAGEM)
    tabela('Adjacencias.csv',['origem','destino','ligacao'],ADJACENCIAS)
    tabela('Complementos_Eletricos.csv',['item','aplicacao','definicao'],COMPLEMENTOS)
    tabela('Reservas_Componentes.csv',['componente','disponibilidade','encaminhamento'],RESERVAS)
    pontos=[(code,room,x,y,130,'LED / teto') for code,room,x,y,res in PONTOS_LUZ]
    pontos += [(code,name,x,y,z,'Altura proposta') for (code,name,x,y),z in zip(SENSORES,[90,85,100,55,120])]
    tabela('Locacao_Pontos_mm.csv',['id','ambiente_ou_funcao','x_maquete_mm','y_maquete_mm','z_maquete_mm','observacao'],pontos)
    cabos=[]
    for code,room,x,y,res in PONTOS_LUZ:
        route=abs(y-120)+abs(x-280)+150+120+130
        cabos.append((code,route,math.ceil(route*1.3),2,'Retorno individual; valor por cabo de duas vias'))
    tabela('Estimativa_Cabos_mm.csv',['ramal','trajeto_mm','comprimento_com_folga_30pct_mm','vias','observacao'],cabos)
    tabela('Conferencias_Necessarias.csv',['item','verificacao'],[
        ('Envelope','Medir comprimento e largura externos das paredes e margens do piso.'),
        ('Planta','Conferir coordenadas das divisorias e localizar portas e janelas.'),
        ('Cobertura','Conferir laje, divisoes T1/T2/T3, recuo e forma de retirar conjunto.'),
        ('Brise','Medir janela J04, microservo, suporte e curso; ainda sem pecas de corte.'),
        ('Base','Definir material, espessura e reforcos conforme peso, apoio e transporte.'),
        ('Central','Medir modulos, bornes, botoes e conexoes antes do corte do expositor.'),
        ('Potencia','Identificar fontes, controlador solar, rele e drivers necessarios.'),
        ('Agua','Medir bomba, sensor, conexoes e mangueiras; definir bandeja e retorno.')])
    (root/'LEIA-ME.txt').write_text(
        PROJETO+'\n'+REVISAO+'\n\n'
        'Conteudo: 23 pranchas A3, desenhos CAD DXF em mm, tabelas CSV e modelo JSON.\n'
        'A01-A08: arquitetura, cobertura, fachadas, cortes, dimensoes, aberturas e adjacencias.\n'
        'M01-M03: planta da maquete, implantacao e central. S01-S02: automacoes e agua.\n'
        'E01-E10: planta eletrica DC, percursos, alimentacao, circuitos, pinos e acionamentos.\n\n'
        'As cotas representam dimensoes de trabalho do anteprojeto. As internas, aberturas e camadas '
        'ainda dependem de compatibilizacao fisica antes de fabricar complementos.\n'
        'O programa de ambientes e a locacao dos equipamentos sao propostas do projeto.\n'
        'O desenho arquitetonico converte a geometria da maquete por 20. As paredes de 3 mm '
        'aparecem como 60 mm na representacao arquitetonica.\n'
        'Base 1200 x 900 x 18 mm: proposta; reforcos e apoio dependem do peso total.\n'
        'A planta eletrica representa a maquete DC, sem distribuicao residencial em 127/220 V.\n'
        'Pinagem e interfaces propostas. Correntes desconhecidas precisam ser medidas. '
        'Componentes ainda nao confirmados estao listados em Complementos_Eletricos.csv.\n'
        'O mapa de pinos nao e firmware. Cameras, fita LED, rele e circuito solar '
        'dependem da identificacao das placas.\n\n'
        'Impressao: papel A3 a 100%. Escala indicada por vista; conferir a barra grafica.\n'
        'DXF: geometria 1:1 nas unidades indicadas. Quadros e diagramas sao esquematicos.\n'
        'Coordenadas dos pontos: origem no canto (0,0) da casa, conforme a planta; Z a partir do piso.\n'
        'Cabos: trajetos aproximados, acrescidos de 30%; nao constituem definicao de bitola.\n\n'
        'Documentacao tecnica consultada para interfaces eletricas:\n'
        'Arduino Mega: https://docs.arduino.cc/resources/pinouts/A000067-full-pinout.pdf\n'
        'Arduino, acionamento: https://docs.arduino.cc/learn/electronics/transistor-motor-control/\n'
        'NXP MFRC522: https://www.nxp.com/docs/en/data-sheet/MFRC522.pdf\n'
        'Espressif ESP32: https://documentation.espressif.com/esp32_datasheet_en.html\n',encoding='utf8')
    if '__file__' in globals():
        (root/'FONTE').mkdir(exist_ok=True)
        shutil.copyfile(Path(__file__),root/'FONTE'/'NEXUS_Gerador_Documentacao.py')
    package=root.with_suffix('.zip')
    with zipfile.ZipFile(package,'w',zipfile.ZIP_DEFLATED) as z:
        for f in sorted(root.rglob('*')):
            if f.is_file():z.write(f,f.relative_to(root))
    print(f'Concluido: {len(sheets)} pranchas no PDF; DXF em mm; dados e listas em CSV/JSON.')
    print('Arquivo:',package)
    print(PROJETO+' | '+REVISAO)
    print('Inclui planta eletrica DC, circuitos, pinagem e automacoes.')
    return root,package

if __name__=='__main__':
    gerar()
