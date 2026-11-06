"""Casa Inteligente | NEXUS | ExpoTech: estudo inicial da eletrica residencial.

Le a geometria publicada na R02 sem modifica-la. Produz plantas de pontos,
previsao de cargas e circuitos propostos. Nao dimensiona protecoes/condutores.
"""
from pathlib import Path
import csv, json, math, hashlib
from collections import defaultdict
import ezdxf
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph, Table, TableStyle
from reportlab.lib.styles import ParagraphStyle

OUT=Path(__file__).resolve().parent
REPO=OUT.parents[1]
BASE=REPO/'01_Arquitetura/R02/DADOS'
MODEL=json.loads((BASE/'NEXUS_Casa_Inteligente_ExpoTech.json').read_text(encoding='utf-8-sig'))
ROOMS=MODEL['ambientes'];WALLS=MODEL['paredes'];OPENINGS=MODEL['aberturas']
FACTOR=MODEL['parametros']['escala_maquete']
WALL={w['id']:w for w in WALLS}
DIM={r['id']:r['C_x_L_arquitetura_mm'] for r in csv.DictReader((BASE/'Dimensoes_Ambientes_mm.csv').open(encoding='utf-8-sig'),delimiter=';')}

def area(poly):return abs(sum(a[0]*b[1]-b[0]*a[1] for a,b in zip(poly,poly[1:]+poly[:1])))/2
def perimeter(poly):return sum(math.hypot(a[0]-b[0],a[1]-b[1]) for a,b in zip(poly,poly[1:]+poly[:1]))
def luz_va(a):return 100 if a<=6 else 100+60*math.floor((a-6)/4+1e-10)
def tug_minimo(room,a,p):
    if room in ('AM03','AM08'):return 1
    if room in ('AM02','AM04'):return math.ceil(p/3.5-1e-10)
    if room in ('AM01','AM06','AM07') or a>6:return math.ceil(p/5-1e-10)
    return 1
def tug_va(room,n):return min(n,3)*600+max(0,n-3)*100 if room in ('AM02','AM03','AM04','AM08') else n*100
def il_circuito(room):return 'C1' if int(room[-2:])<=5 else 'C2'
def tug_circuito(room):
    return {'AM01':'C3','AM05':'C3','AM09':'C3','AM10':'C3','AM06':'C4','AM07':'C4','AM02':'C5','AM04':'C6','AM03':'C7','AM08':'C7'}[room]
LABEL={'AM01':(65,130),'AM02':(155,248),'AM03':(254,65),'AM04':(390,70),'AM05':(360,128),'AM06':(405,247),'AM07':(600,252),'AM08':(535,69),'AM09':(640,69),'AM10':(260,255)}
META={}
for r in ROOMS:
    a=area(r['poligono'])*FACTOR**2/1e6;p=perimeter(r['poligono'])*FACTOR/1000
    META[r['id']]={'id':r['id'],'ambiente':r['nome'],'dimensoes_mm':DIM[r['id']],'area_m2':round(a,6),'perimetro_m':round(p,6),'iluminacao_va':luz_va(a),'tug_minimo':tug_minimo(r['id'],a,p)}

POINTS=[]
def free_point(id,room,kind,x,y,z,va=0,circuit='',note=''):
    p={'id':id,'ambiente':room,'tipo':kind,'parede':'','x_maquete_mm':x,'y_maquete_mm':y,'z_maquete_mm':z/FACTOR,'x_arquitetura_mm':x*FACTOR,'y_arquitetura_mm':y*FACTOR,'z_arquitetura_mm':z,'previsao_va':va,'circuito_proposto':circuit,'observacao':note}
    POINTS.append(p);return p
def wall_point(id,room,kind,wall,a,z,va=0,circuit='',note=''):
    w=WALL[wall];x,y=(a,w['u']) if w['eixo']=='H' else (w['u'],a)
    p=free_point(id,room,kind,x,y,z,va,circuit,note);p['parede']=wall;return p

LIGHTS=[('AM01',65,80),('AM01',65,210),('AM02',155,215),('AM03',255,45),('AM04',390,45),('AM06',405,210),('AM07',600,210),('AM08',535,45),('AM09',640,45),('AM05',430,120),('AM10',260,215)]
for i,(r,x,y) in enumerate(LIGHTS,1):free_point(f'L{i:02}',r,'ILUMINACAO',x,y,2600,META[r]['iluminacao_va']/(2 if r=='AM01' else 1),il_circuito(r),'Previsao de iluminacao; modelo/fluxo de luminaria a definir')

SWITCHES=[('S01','AM01','R01',62,['L01','L02'],'simples'),('S02','AM02','R05',211,['L03'],'simples'),('S03','AM03','R10',246,['L04'],'simples, face circulacao'),('S04','AM04','R17',382,['L05'],'simples'),('S05A','AM05','R10',236,['L10'],'paralelo'),('S05B','AM05','R17',478,['L10'],'paralelo'),('S06','AM06','R13',442,['L06'],'simples'),('S07','AM07','R14',151,['L07'],'simples'),('S08','AM08','R17',528,['L08'],'simples, face quarto'),('S09','AM09','R17',617,['L09'],'simples'),('S10','AM10','R08',260,['L11'],'simples')]
for id,r,w,a,lamps,kind in SWITCHES:
    p=wall_point(id,r,'INTERRUPTOR',w,a,1100,0,il_circuito(r),kind);p['comanda']=lamps

# Quantidade proposta e posicoes simbolicas na linha da parede; conferir mobiliario.
TUGS={
'AM01':[('R03',30,300),('R09',50,300),('R05',65,300),('R01',150,300)],
'AM02':[('R08',170,1100),('R08',200,1100),('R07',200,300),('R05',140,300)],
'AM03':[('R10',223,1100)],
'AM04':[('R04',315,300),('R04',375,1100),('R04',450,1100),('R15',65,300)],
'AM05':[('R10',250,300),('R17',478,300)],
'AM06':[('R12',180,300),('R13',345,300),('R13',430,300),('R06',480,300)],
'AM07':[('R17',600,300),('R02',180,300),('R06',550,300),('R06',670,300)],
'AM08':[('R17',496,1100)],
'AM09':[('R02',65,300),('R16',65,300)],
'AM10':[('R08',180,300),('R05',280,300)]}
k=1
for r,positions in TUGS.items():
    META[r]['tug_proposto']=len(positions);META[r]['tug_previsao_va']=tug_va(r,len(positions))
    for j,(w,a,z) in enumerate(positions):
        va=600 if r in ('AM02','AM03','AM04','AM08') and j<3 else 100
        note='Locacao proposta; compatibilizar mobiliario'
        if r=='AM02' and j<2:note='Duas tomadas acima de bancada proposta; conferir pia e mobiliario'
        if r in ('AM03','AM08'):note='Proximo a lavatorio proposto; posicao condicionada a volumes do chuveiro'
        wall_point(f'T{k:02}',r,'TUG',w,a,z,va,tug_circuito(r),note);k+=1

RESERVAS=[('R01','AM02','R07',190,650,'Coccao eletrica',220),('R02','AM02','R07',175,300,'Forno',220),('R03','AM04','R04',465,300,'Lavadora',127),('R04','AM04','R15',40,1800,'Aquecimento de agua',220),('R05','AM06','R13',330,2200,'Climatizacao quarto 1',220),('R06','AM07','R02',180,2200,'Climatizacao quarto 2',220),('R07','AM09','R02',70,1300,'Central de automacao/rede',127)]
for id,r,w,a,z,use,v in RESERVAS:
    p=wall_point(id,r,'RESERVA_EQUIPAMENTO',w,a,z,None,'',use+'; potencia/circuito apos escolha');p['tensao_estudo_v']=v
wall_point('QD1','AM01','QUADRO_PROPOSTO','R09',75,1500,None,'','Face da sala; capacidade e protecoes ainda nao dimensionadas')

CIRCUITS=[]
DESCS={'C1':'Iluminacao social, cozinha, banho 1, servico e circulacao','C2':'Iluminacao quartos, banho 2, apoio e hall','C3':'TUG sala, circulacao, apoio e hall','C4':'TUG quartos 1 e 2','C5':'TUG cozinha','C6':'TUG servico','C7':'TUG banhos 1 e 2'}
for c,desc in DESCS.items():
    pts=[p for p in POINTS if p['circuito_proposto']==c and p['tipo'] in ('ILUMINACAO','TUG')]
    s=sum(p['previsao_va'] for p in pts)
    CIRCUITS.append({'circuito':c,'uso':desc,'pontos':len(pts),'previsao_va':s,'tensao_hipotese_v':127,'corrente_inicial_a':round(s/127,4),'condutores_mm2':'A dimensionar','protecao':'A dimensionar'})

PREMISSAS={
'projeto':'Casa Inteligente | NEXUS | ExpoTech','revisao':'Eletrica residencial R01 - pontos e previsao de cargas','data':'2026-11-05','estado':'ESTUDO ACADEMICO; NAO LIBERADO PARA EXECUCAO',
'geometria':'Modelo JSON e quadros R02 preservados; fator de representacao 20; cotas internas estimadas','unidade_coordenadas':'mm','origem':'Origem local das paredes da R02; nao inclui translacao na base de exposicao',
'alimentacao_estudo':'127 V para circuitos C1-C7; reservas 127/220 V como hipoteses; fornecimento a confirmar',
'geometria_arquitetonica':'Parede grafica de 60 mm por conversao da maquete; sistema de vedacao real ainda nao especificado',
'alturas':'Luz 2600; interruptores 1100; TUG 300 ou 1100 conforme ponto; QD 1500. Alturas propostas, nao minimos normativos.',
'criterio_tug':'Aplicado criterio conservador de 600 VA nos primeiros tres pontos dos ambientes pertinentes, sem reducao facultativa.',
'reservas':'Equipamentos ainda sem potencia/modelo; nao entram na soma base. R08 garagem sem locacao por geometria ainda nao definida.',
'fora_do_escopo_desta_revisao':['Dimensionamento de condutores e protecoes','Demanda do alimentador e padrao de entrada','Esquema de aterramento/DR/DPS','Volumetria de banhos e mobiliario definitivo','Projeto luminotecnico','Garagem/area externa','Integracao fotovoltaica predial'],
'maquete':'Permanece em circuitos DC; este desenho residencial nao autoriza ligacoes de rede na maquete',
'referencias':[{'documento':'ABNT NBR 5410:2004, versao corrigida 2008','itens':'9.5.2.1, 9.5.2.2, 9.5.3','catalogo':'https://abntcatalogo.com.br/default.aspx','consulta':'2026-11-05'},{'documento':'NEXUS R02','arquivo':'01_Arquitetura/R02/DADOS/NEXUS_Casa_Inteligente_ExpoTech.json','sha256':hashlib.sha256((BASE/'NEXUS_Casa_Inteligente_ExpoTech.json').read_bytes()).hexdigest()}]}

def validar():
    assert len({p['id'] for p in POINTS})==len(POINTS)
    areas_csv={r['id']:float(r['area_equivalente_m2']) for r in csv.DictReader((BASE/'Ambientes_Areas_Estimadas.csv').open(encoding='utf-8-sig'),delimiter=';')}
    for r,m in META.items():
        assert abs(m['area_m2']-areas_csv[r])<.0006,(r,'area divergente')
        assert m['tug_proposto']>=m['tug_minimo'],r
    for p in POINTS:
        if not p['parede']:continue
        w=WALL[p['parede']];a=p['x_maquete_mm'] if w['eixo']=='H' else p['y_maquete_mm']
        assert w['a']<=a<=w['b'],p['id']
        z=p['z_maquete_mm']
        for op in OPENINGS:
            if op['parede']==w['id'] and op['a']<=a<=op['a']+op['w'] and op['z']<=z<=op['z']+op['h']:
                raise ValueError('Ponto intercepta abertura: '+p['id']+'/'+op['id'])
    assert len([p for p in POINTS if p['tipo']=='TUG'])==28
    assert sum(m['iluminacao_va'] for m in META.values())==1240
    assert sum(m['tug_previsao_va'] for m in META.values())==6800
    assert sum(c['previsao_va'] for c in CIRCUITS)==8040
    assert all(abs(c['corrente_inicial_a']-c['previsao_va']/127)<.0001 for c in CIRCUITS)
    assert luz_va(6)==100 and luz_va(9.999)==100 and luz_va(10)==160 and luz_va(14)==220

def csv_out(name,rows):
    keys=list(dict.fromkeys(k for row in rows for k in row))
    with (OUT/name).open('w',newline='',encoding='utf-8-sig') as f:
        w=csv.DictWriter(f,fieldnames=keys,delimiter=';');w.writeheader()
        for row in rows:w.writerow({k:json.dumps(v,ensure_ascii=False) if isinstance(v,list) else v for k,v in row.items()})

def salvar_dados():
    csv_out('Ambientes_Cargas.csv',list(META.values()));csv_out('Pontos_Residenciais_mm.csv',POINTS);csv_out('Circuitos_Propostos.csv',CIRCUITS)
    reserves=[{k:p.get(k,'') for k in ['id','ambiente','observacao','tensao_estudo_v','previsao_va','circuito_proposto']} for p in POINTS if p['tipo']=='RESERVA_EQUIPAMENTO']
    reserves.append({'id':'R08','ambiente':'GARAGEM','observacao':'Atuacao e pontos externos; geometria/modelos a definir','tensao_estudo_v':'A definir','previsao_va':None,'circuito_proposto':''})
    csv_out('Reservas_Equipamentos.csv',reserves)
    data={'premissas':PREMISSAS,'ambientes':list(META.values()),'pontos':POINTS,'circuitos':CIRCUITS,'reservas':reserves}
    (OUT/'Modelo_Eletrico_Residencial_R01.json').write_text(json.dumps(data,ensure_ascii=False,indent=2))
    return reserves

PAGE_W,PAGE_H=420*mm,297*mm
NAVY=colors.HexColor('#183a57');BLUE=colors.HexColor('#096a9d');GREEN=colors.HexColor('#168364');ORANGE=colors.HexColor('#b56617');GRAY=colors.HexColor('#5d6d7e')
def num(n,d=0):return f'{n:,.{d}f}'.replace(',','@').replace('.',',').replace('@','.')

def setup_fonts():
    for name,file in [('Nexus','DejaVuSans.ttf'),('NexusBold','DejaVuSans-Bold.ttf')]:
        pdfmetrics.registerFont(TTFont(name,'/usr/share/fonts/truetype/dejavu/'+file))

def paragraph(c,text,x,top,width,size=8.5,color=NAVY):
    st=ParagraphStyle('p',fontName='Nexus',fontSize=size,leading=size*1.42,textColor=color)
    p=Paragraph(text,st);_,h=p.wrap(width*mm,400*mm);p.drawOn(c,x*mm,top*mm-h);return h/mm

def frame(c,number,title,subtitle):
    c.setFillColor(NAVY);c.setFont('NexusBold',15);c.drawString(16*mm,281*mm,'CASA INTELIGENTE | NEXUS | ExpoTech')
    c.setFont('NexusBold',12);c.drawString(16*mm,267*mm,title)
    c.setFont('Nexus',8.5);c.setFillColor(GRAY);c.drawString(16*mm,260*mm,subtitle)
    c.setStrokeColor(BLUE);c.setLineWidth(1);c.line(16*mm,255*mm,404*mm,255*mm)
    c.setLineWidth(.5);c.line(16*mm,35*mm,404*mm,35*mm)
    paragraph(c,'ESTUDO ACADEMICO | R01 | 05/11/2026 | Pontos e previsao de cargas; sem dimensionamento final.',16,30,350,7.2)
    paragraph(c,'Cotas em mm. Base geometrica R02. Alturas e usos propostos precisam de compatibilizacao.',16,24,350,7.2)
    c.setFont('NexusBold',9);c.setFillColor(NAVY);c.drawRightString(403*mm,23*mm,f'EPR-{number:02} / 04')

def segments(w):
    cursor=w['a']
    for op in sorted([o for o in OPENINGS if o['parede']==w['id']],key=lambda x:x['a']):
        if op['a']>cursor:yield cursor,op['a']
        cursor=max(cursor,op['a']+op['w'])
    if cursor<w['b']:yield cursor,w['b']

def plot(c,kind):
    # O fator converte coordenadas da maquete em arquitetura; impressao 1:50.
    x0,y0=30*mm,106*mm;s=FACTOR*mm/50
    def xy(x,y):return x0+x*s,y0+y*s
    c.setLineWidth(.5);c.setStrokeColor(colors.HexColor('#b8c9d6'));c.setDash(3,2)
    c.rect(*xy(-10,-10),717.5*s,308*s,fill=0,stroke=1);c.setDash()
    for r in ROOMS:
        path=c.beginPath();pts=r['poligono'];path.moveTo(*xy(*pts[0]))
        for q in pts[1:]:path.lineTo(*xy(*q))
        path.close();c.setFillColor(colors.HexColor('#f5f8fb'));c.setStrokeColor(colors.HexColor('#e1e8ee'));c.drawPath(path,fill=1,stroke=0)
    for w in WALLS:
        c.setFillColor(colors.HexColor('#dae0e5'));c.setStrokeColor(GRAY);c.setLineWidth(.45)
        for a,b in segments(w):
            if w['eixo']=='H':c.rect(*xy(a,w['u']-1.5),(b-a)*s,3*s,fill=1,stroke=1)
            else:c.rect(*xy(w['u']-1.5,a),3*s,(b-a)*s,fill=1,stroke=1)
    for op in OPENINGS:
        w=WALL[op['parede']];a=op['a'];b=a+op['w'];u=w['u'];c.setStrokeColor(colors.HexColor('#8e9eac'));c.setLineWidth(.5)
        if op['tipo']=='porta':
            side=-1 if w['id'] in ('R05','R06','R10','R17') else 1
            if w['eixo']=='H':
                hinge=(a,u);end=(a,u+side*op['w']);c.line(*xy(*hinge),*xy(*end))
                path=c.beginPath();path.moveTo(*xy(b,u))
                for j in range(1,17):path.lineTo(*xy(a+op['w']*math.cos(j*math.pi/32),u+side*op['w']*math.sin(j*math.pi/32)))
            else:
                c.line(*xy(u,a),*xy(u+op['w'],a));path=c.beginPath();path.moveTo(*xy(u,b))
                for j in range(1,17):path.lineTo(*xy(u+op['w']*math.sin(j*math.pi/32),a+op['w']*math.cos(j*math.pi/32)))
            c.drawPath(path)
        elif w['eixo']=='H':c.line(*xy(a,u),*xy(b,u));c.line(*xy(a,u-1),*xy(b,u-1))
        else:c.line(*xy(u,a),*xy(u,b));c.line(*xy(u-1,a),*xy(u-1,b))
    # Relacoes de comando nao representam eletrodutos.
    if kind=='IL':
        byid={p['id']:p for p in POINTS};c.setStrokeColor(GREEN);c.setLineWidth(.55);c.setDash(2,2)
        for p in POINTS:
            for lid in p.get('comanda',[]):
                q=byid[lid];c.line(*xy(p['x_maquete_mm'],p['y_maquete_mm']),*xy(q['x_maquete_mm'],q['y_maquete_mm']))
        c.setDash()
    for r in ROOMS:
        x,y=xy(*LABEL[r['id']]);name=r['nome'].replace('SERVICO','SERVIÇO').replace('CIRCULACAO','CIRCULAÇÃO')
        width=max(pdfmetrics.stringWidth(name,'Nexus',6.8),pdfmetrics.stringWidth(r['id'],'NexusBold',7))+5*mm
        c.setFillColor(colors.white);c.roundRect(x-width/2,y-3*mm,width,8*mm,1*mm,fill=1,stroke=0)
        c.setFillColor(GRAY);c.setFont('NexusBold',7);c.drawCentredString(x,y+1.5*mm,r['id']);c.setFont('Nexus',6.8);c.drawCentredString(x,y-1.7*mm,name)
    for p in POINTS:
        typ=p['tipo']
        if kind=='IL' and typ not in ('ILUMINACAO','INTERRUPTOR'):continue
        if kind=='TUG' and typ not in ('TUG','RESERVA_EQUIPAMENTO','QUADRO_PROPOSTO'):continue
        x,y=xy(p['x_maquete_mm'],p['y_maquete_mm']);color=ORANGE if typ=='RESERVA_EQUIPAMENTO' else BLUE
        c.setStrokeColor(color);c.setFillColor(colors.white);c.setLineWidth(.8)
        if p['id'] in ('R06','R07'):
            ax,ay=x,y;x-=7*mm;y+=8*mm
            c.setLineWidth(.4);c.line(ax,ay,x,y);c.circle(ax,ay,.45*mm,fill=1,stroke=1)
        if typ=='ILUMINACAO':
            c.circle(x,y,2*mm,fill=1,stroke=1);c.line(x-1.4*mm,y-1.4*mm,x+1.4*mm,y+1.4*mm);c.line(x-1.4*mm,y+1.4*mm,x+1.4*mm,y-1.4*mm)
            tx,ty=x+3*mm,y+1.6*mm;align='left'
        elif typ=='QUADRO_PROPOSTO':
            c.setFillColor(BLUE);c.rect(x-8*mm,y-2.5*mm,8*mm,5*mm,fill=1,stroke=0);c.setFillColor(colors.white);c.setFont('NexusBold',6);c.drawCentredString(x-4*mm,y-.8*mm,p['id']);continue
        else:
            if typ=='INTERRUPTOR':c.circle(x,y,1.1*mm,fill=1,stroke=1)
            elif typ=='TUG':
                c.circle(x,y,1.5*mm,fill=1,stroke=1);c.line(x-.5*mm,y-.7*mm,x-.5*mm,y+.7*mm);c.line(x+.5*mm,y-.7*mm,x+.5*mm,y+.7*mm)
            else:c.rect(x-1.8*mm,y-1.8*mm,3.6*mm,3.6*mm,fill=1,stroke=1)
            w=WALL[p['parede']];rx,ry=LABEL[p['ambiente']];off=6*mm if typ=='RESERVA_EQUIPAMENTO' else 3.1*mm
            if w['eixo']=='H':tx=x;ty=y+(off if ry>w['u'] else -off-1.5*mm);align='center'
            else:tx=x+(off if rx>w['u'] else -off);ty=y+1.0*mm;align='left' if rx>w['u'] else 'right'
            c.setStrokeColor(color);c.setLineWidth(.4);c.line(x,y,tx,ty)
        c.setFillColor(color);c.setFont('NexusBold',7)
        {'left':c.drawString,'right':c.drawRightString,'center':c.drawCentredString}[align](tx,ty,p['id'])
    # Cotas gerais do envelope de paredes.
    c.setStrokeColor(GRAY);c.setFillColor(GRAY);c.setLineWidth(.45)
    xa,ya=xy(0,-32);xb,_=xy(697.5,-32)
    c.line(xa,ya,xb,ya)
    for x in (xa,xb):c.line(x,xy(0,0)[1],x,ya-2*mm);c.line(x-1*mm,ya-1*mm,x+1*mm,ya+1*mm)
    c.setFont('Nexus',8);c.drawCentredString((xa+xb)/2,ya+2*mm,'13.950 mm')
    xx=16*mm;_,yl=xy(0,0);_,yh=xy(0,288);c.line(xx,yl,xx,yh)
    for yy in (yl,yh):c.line(xx-1*mm,yy-1*mm,xx+1*mm,yy+1*mm)
    c.saveState();c.translate(xx-2*mm,(yl+yh)/2);c.rotate(90);c.drawCentredString(0,0,'5.760 mm');c.restoreState()
    c.setFont('Nexus',7);c.drawString(30*mm,239*mm,'ARQUITETURA: mm | 1:50 em A3 a 100% | Origem local do modelo R02')
    c.setFont('Nexus',7);c.drawString(30*mm,76*mm,'Envelope de paredes: 13.950 x 5.760 mm. Piso representado: 14.350 x 6.160 mm.')

def table(c,top,headers,rows,widths):
    st=ParagraphStyle('cell',fontName='Nexus',fontSize=8,leading=11,textColor=NAVY)
    head=ParagraphStyle('head',parent=st,fontName='NexusBold',textColor=colors.white)
    data=[[Paragraph(str(x),head) for x in headers]]+[[Paragraph(str(x),st) for x in row] for row in rows]
    t=Table(data,colWidths=[v*mm for v in widths],repeatRows=1,hAlign='LEFT')
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),NAVY),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.HexColor('#f1f6fa'),colors.white]),('VALIGN',(0,0),(-1,-1),'MIDDLE'),('LEFTPADDING',(0,0),(-1,-1),6),('RIGHTPADDING',(0,0),(-1,-1),6),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6),('LINEBELOW',(0,0),(-1,0),.6,NAVY)]))
    _,h=t.wrap(390*mm,250*mm)
    if top*mm-h<41*mm:raise ValueError('Tabela ultrapassa rodape')
    t.drawOn(c,20*mm,top*mm-h);return top-h/mm

def pdf(reserves):
    setup_fonts();c=canvas.Canvas(str(OUT/'NEXUS_Eletrica_Residencial_R01.pdf'),pagesize=(PAGE_W,PAGE_H))
    c.setTitle('Casa Inteligente | NEXUS | ExpoTech - Eletrica residencial R01');c.setAuthor('Projeto NEXUS')
    frame(c,1,'Iluminacao e comandos','Previsao residencial sobre a geometria R02. Alturas propostas; associacoes de comando sem rotas de eletrodutos.')
    plot(c,'IL')
    paragraph(c,'<b>LEGENDA DESTE ESTUDO</b><br/><br/>L01-L11: pontos de luz.<br/><br/>S01-S10: interruptores; S05A/S05B formam comando paralelo da circulacao.<br/><br/>Tracejado verde: relacao entre interruptor e ponto de luz. Nao indica eletroduto.<br/><br/>C1: 620 VA.<br/>C2: 620 VA.<br/><br/>Alturas propostas:<br/>luz: 2.600 mm;<br/>interruptores: 1.100 mm.<br/><br/>11 pontos de luz e 11 posicoes de comando.',326,241,75,8.3)
    paragraph(c,'<b>PREVISAO:</b> 1.240 VA para iluminacao. Essa potencia de previsao nao e a soma de watts das lampadas escolhidas nem um resultado luminotecnico. A selecao de luminarias e o atendimento de iluminancia serao desenvolvidos depois.',30,67,370,8.5)
    paragraph(c,'A maquete continua com alimentacao DC. As tensoes residenciais usadas no estudo nao devem ser ligadas aos sensores ou aos pinos do Mega.',30,51,370,8.3)
    c.showPage()
    frame(c,2,'Tomadas, quadro proposto e reservas','Localizacao preliminar por funcao. Os pontos de equipamentos ainda nao entram na carga total de estudo.')
    plot(c,'TUG')
    paragraph(c,'<b>LEGENDA DESTE ESTUDO</b><br/><br/>T01-T28: tomadas de uso geral.<br/><br/>R01-R07: reservas para equipamentos, sem potencia ou circuito definidos.<br/><br/>QD1: local proposto do quadro, voltado para a sala.<br/><br/>T05/T06: duas tomadas acima da bancada proposta da cozinha.<br/><br/>T09/T24: proximas a lavatorios propostos; conferir volumes de banho.<br/><br/>R08: garagem, sem localizacao nesta planta.<br/><br/>R06/R07: simbolos afastados graficamente por chamada; posicoes e alturas no CSV.',326,241,75,8.1)
    paragraph(c,'<b>ALTURAS PROPOSTAS:</b> T05, T06, T09, T11, T12 e T24 a 1.100 mm; demais TUG a 300 mm. Alturas das reservas e coordenadas completas no CSV de pontos. QD1 a 1.500 mm. Sao escolhas iniciais de locacao, nao alturas minimas normativas.',30,67,370,8.5)
    paragraph(c,'A verificacao geometrica evita pontos nas aberturas da R02. Volumes de chuveiro, lavatorios, bancadas e mobiliario ainda precisam de compatibilizacao especifica.',30,50,370,8.3)
    c.showPage()
    frame(c,3,'Ambientes e previsao de cargas','Dimensoes ampliadas da R02, sem alterar a geometria. Areas/perimetros calculados pelos poligonos do modelo.')
    rows=[[r['id'],r['ambiente'],r['dimensoes_mm'],num(r['area_m2'],3),num(r['perimetro_m'],3),num(r['iluminacao_va']),f"{r['tug_minimo']} / {r['tug_proposto']}",num(r['tug_previsao_va'])] for r in META.values()]
    bottom=table(c,247,['ID','AMBIENTE','DIMENSOES ADOTADAS<br/>C x L (mm)','AREA<br/>(m2)','PERIMETRO<br/>(m)','ILUMINACAO<br/>(VA)','TUG<br/>min. / prop.','TUG<br/>(VA)'],rows,[16,49,80,28,30,34,32,33])
    total=sum(m['area_m2'] for m in META.values())
    y=bottom-10
    y-=paragraph(c,f'<b>BASE DESTA REVISAO:</b> area dos ambientes {num(total,3)} m2; 22 pontos TUG minimos calculados e 28 propostos. Iluminacao: 1.240 VA. TUG propostas: 6.800 VA. <b>Soma base: 8.040 VA.</b>',20,y,380,10)+5
    y-=paragraph(c,'Os 8.040 VA excluem as reservas de equipamentos e a garagem. Nao representam demanda do alimentador, consumo em kWh ou potencia final instalada. As cotas sao estimativas de anteprojeto; a espessura grafica de 60 mm nao especifica a vedacao real.',20,y,380,9)+5
    y-=paragraph(c,'<b>CRITERIOS DE PREVISAO:</b> iluminacao de 100 VA ate 6 m2, com 60 VA adicionais por cada 4 m2 inteiros acima dessa area. Tomadas por destino/perimetro: salas/quartos a cada 5 m ou fracao; cozinha/servico a cada 3,5 m; banhos com ponto junto ao lavatorio; demais ambientes conforme area. Nos ambientes pertinentes, usou-se 600 VA nos tres primeiros pontos e 100 VA nos seguintes; nos demais, 100 VA por ponto. Nao foi aplicada a reducao facultativa.',20,y,380,8.6)+5
    paragraph(c,'Referencia: ABNT NBR 5410:2004, versao corrigida 2008, itens 9.5.2 e 9.5.3. Catalogo ABNT consultado em 05/11/2026. Esta folha apresenta a aplicacao ao NEXUS, sem reproduzir a norma.',20,y,380,8.2)
    c.showPage()
    frame(c,4,'Circuitos propostos e decisoes de equipamentos','Separacao funcional inicial. Correntes calculadas apenas com a hipotese de 127 V nos circuitos C1-C7.')
    rows=[[q['circuito'],q['uso'],str(q['pontos']),num(q['previsao_va']),'127',num(q['corrente_inicial_a'],2),'A dimensionar'] for q in CIRCUITS]
    bottom=table(c,247,['CIRCUITO','USO','PONTOS','S (VA)','U (V)','I = S/U (A)','CABOS / PROTECOES'],rows,[23,125,24,32,24,40,53])
    y=bottom-8
    y-=paragraph(c,'<b>RESERVAS DE EQUIPAMENTOS:</b> os usos abaixo sao propostas para decidir o programa da residencia. Tensoes sao hipoteses; potencias/modelos, necessidade de circuito dedicado e demanda serao fechados depois.',20,y,380,8.6)+4
    resrows=[[q['id'],q['ambiente'],q['observacao'].split(';')[0],str(q['tensao_estudo_v']),'A definir / fora da soma base'] for q in reserves]
    y=table(c,y,['ID','AMBIENTE','USO A CONFIRMAR','U DE ESTUDO (V)','POTENCIA / CIRCUITO'],resrows,[18,30,120,48,105])-7
    paragraph(c,'<b>PROXIMA REVISAO:</b> definir equipamentos e fornecimento; calcular demanda; dimensionar condutores, protecoes e alimentador; desenvolver unifilar, aterramento, DR/DPS e integracao renovavel. Esta revisao nao escolhe disjuntores, secoes ou padrao de entrada por suposicao.',20,y,380,8.5)
    c.save()

def dxf(kind):
    doc=ezdxf.new('R2010');doc.units=4;m=doc.modelspace();doc.header['$MEASUREMENT']=1
    for layer,col in [('PAREDES',8),('ABERTURAS',9),('AMBIENTES',8),('ILUMINACAO',5),('COMANDOS',3),('TUG',5),('RESERVAS',30),('TEXTOS',7)]:doc.layers.new(layer,dxfattribs={'color':col})
    def line(a,b,layer):m.add_line((a[0]*FACTOR,a[1]*FACTOR),(b[0]*FACTOR,b[1]*FACTOR),dxfattribs={'layer':layer})
    for w in WALLS:
        for a,b in segments(w):
            pts=[(a,w['u']-1.5),(b,w['u']-1.5),(b,w['u']+1.5),(a,w['u']+1.5)] if w['eixo']=='H' else [(w['u']-1.5,a),(w['u']+1.5,a),(w['u']+1.5,b),(w['u']-1.5,b)]
            m.add_lwpolyline([(x*FACTOR,y*FACTOR) for x,y in pts],close=True,dxfattribs={'layer':'PAREDES'})
    for op in OPENINGS:
        w=WALL[op['parede']];a=op['a'];b=a+op['w'];u=w['u']
        if w['eixo']=='H':line((a,u),(b,u),'ABERTURAS')
        else:line((u,a),(u,b),'ABERTURAS')
    for r in ROOMS:
        x,y=LABEL[r['id']];m.add_text(r['id']+' '+r['nome'],dxfattribs={'height':100,'insert':(x*FACTOR-300,y*FACTOR),'layer':'AMBIENTES'})
    for p in POINTS:
        typ=p['tipo']
        if kind=='IL' and typ not in ('ILUMINACAO','INTERRUPTOR'):continue
        if kind=='TUG' and typ not in ('TUG','RESERVA_EQUIPAMENTO','QUADRO_PROPOSTO'):continue
        layer={'ILUMINACAO':'ILUMINACAO','INTERRUPTOR':'COMANDOS','TUG':'TUG','RESERVA_EQUIPAMENTO':'RESERVAS','QUADRO_PROPOSTO':'RESERVAS'}[typ]
        x,y=p['x_arquitetura_mm'],p['y_arquitetura_mm'];radius=100 if typ=='ILUMINACAO' else 65
        m.add_circle((x,y),radius,dxfattribs={'layer':layer})
        label=p['id'];ty=y+100
        if typ=='RESERVA_EQUIPAMENTO':
            label+=f" z={p['z_arquitetura_mm']}";ty=y+420
            m.add_line((x,y),(x+140,ty),dxfattribs={'layer':layer})
        m.add_text(label,dxfattribs={'height':100,'insert':(x+140,ty),'layer':layer})
    m.add_text('NEXUS | ELETRICA RESIDENCIAL R01 | ESTUDO ACADEMICO | UNIDADES mm',dxfattribs={'height':150,'insert':(0,6400),'layer':'TEXTOS'})
    if kind=='IL':
        lookup={p['id']:p for p in POINTS}
        for p in POINTS:
            for id in p.get('comanda',[]):q=lookup[id];line((p['x_maquete_mm'],p['y_maquete_mm']),(q['x_maquete_mm'],q['y_maquete_mm']),'COMANDOS')
    doc.saveas(OUT/('EPR01_Iluminacao.dxf' if kind=='IL' else 'EPR02_Tomadas.dxf'))

def main():
    validar();reserves=salvar_dados();pdf(reserves);dxf('IL');dxf('TUG')
    print(json.dumps({'pontos':len(POINTS),'circuitos':len(CIRCUITS),'iluminacao_va':1240,'tug_va':6800,'base_va':8040,'reservas_fora_da_soma':len(reserves),'pdf':str(OUT/'NEXUS_Eletrica_Residencial_R01.pdf')},ensure_ascii=False))
if __name__=='__main__':main()
