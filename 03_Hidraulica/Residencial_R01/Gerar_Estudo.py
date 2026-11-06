"""Casa Inteligente | NEXUS | ExpoTech. Hidraulica residencial R01.
Gera estudo de distribuicao e rotas, sem dimensionamento final de redes.
"""
from pathlib import Path
import csv, json, math
from collections import Counter
import ezdxf
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Table, TableStyle, Paragraph
from reportlab.lib.styles import ParagraphStyle

OUT=Path(__file__).resolve().parent
REPO=OUT.parents[1]
SOURCE=REPO/'01_Arquitetura/R02/DADOS/NEXUS_Casa_Inteligente_ExpoTech.json'
MODEL=json.loads(SOURCE.read_text(encoding='utf-8-sig'))
F=MODEL['parametros']['escala_maquete']; WALLS=MODEL['paredes']; OPS=MODEL['aberturas'];ROOMS=MODEL['ambientes']
WALL={w['id']:w for w in WALLS}
# Centros de referencia de aparelhos, nao eixos de conexoes ou dimensoes de loucas.
FIXTURES=[
('H01','AM02','Pia da cozinha',194,186,'AF,AQ','CG1','Bancada proposta proxima a R08; compatibilizar T05/T06'),
('H02','AM03','Lavatorio 1',229,76,'AF,AQ','CS1','Conferir aproximacao, bancada e tomada T09'),
('H03','AM03','Bacia sanitaria 1',235,27,'NP','CI1','Caixa de descarga prevista; sem ligacao AF direta'),
('H04','AM03','Chuveiro 1',275,22,'AF,AQ','CS1','Zona de banho proposta; delimitacao final pendente'),
('H05','AM08','Lavatorio 2',503,77,'AF,AQ','CS2','Conferir bancada e tomada T24'),
('H06','AM08','Bacia sanitaria 2',516,27,'NP','CI2','Caixa de descarga prevista; sem ligacao AF direta'),
('H07','AM08','Chuveiro 2',562,23,'AF,AQ','CS2','Zona de banho proposta; delimitacao final pendente'),
('H08','AM04','Tanque',330,19,'AF','CI2','Conexao de esgoto com desconexao a detalhar'),
('H09','AM04','Lavadora',464,22,'AF','CI2','Compatibilizar R03 e T12 da eletrica; sifao a detalhar'),
('H10','AM03','Ralo de piso 1',249,58,'','CS1','Fecho hidrico e conexoes a detalhar; fora do giro da porta'),
('H11','AM08','Ralo de piso 2',530,65,'','CS2','Fecho hidrico e conexoes a detalhar; fora do giro da porta')]
POINTS=[{'id':id,'ambiente':am,'aparelho':name,'x_maquete_mm':x,'y_maquete_mm':y,'x_arquitetura_mm':x*F,'y_arquitetura_mm':y*F,'abastecimento':net,'destino_esgoto':dest,'observacao':note,'altura_conexoes_mm':'A definir pelo aparelho','estado':'PROPOSTO'} for id,am,name,x,y,net,dest,note in FIXTURES]
P={p['id']:p for p in POINTS}
NODES={'CAF':(330,110),'AQ1':(455,60),'RNP':(720,-18),'CG1':(185,-30),'CS1':(252,50),'CS2':(544,59),'CI1':(285,-60),'CI2':(520,-60),'DS1':(670,-60),'VT1':(292,72),'VT2':(578,72)}
# Rotas de estudo em projecao; nao definem cota vertical, declividade ou diametro.
ROUTES=[]
def route(id,net,pts,fr,to,note=''):
    ROUTES.append({'id':id,'rede':net,'origem':fr,'destino':to,'vertices_maquete_mm':[list(p) for p in pts],'comprimento_projecao_arquitetura_mm':round(sum(math.dist(a,b) for a,b in zip(pts,pts[1:]))*F,2),'DN_mm':'A dimensionar','cota_z_mm':'A definir','observacao':note or 'Rota esquematica em projecao; nao e quantitativo de compra'})
route('AF00','AF',[(330,-50),NODES['CAF']],'Entrada/reservacao potavel','CAF')
route('AF01','AF',[(202,110),(580,110)],'CAF','Barrilete AF','Proposta de distribuicao superior; registros setoriais a detalhar')
for p in POINTS:
    if 'AF' in p['abastecimento'].split(','):
        x,y=p['x_maquete_mm'],p['y_maquete_mm'];bx=202 if p['id']=='H01' else x
        route('AF_'+p['id'],'AF',[(bx,110),(bx,y),(x,y)],'Barrilete AF',p['id'])
route('AF_AQ','AF',[(455,110),NODES['AQ1']],'Barrilete AF','AQ1','Alimentacao do aquecimento central proposto; sistema e protecoes a definir')
route('AQ00','AQ',[NODES['AQ1'],(455,101),(202,101)],'AQ1','Barrilete AQ')
route('AQ01','AQ',[(455,101),(580,101)],'AQ1','Barrilete AQ')
for p in POINTS:
    if 'AQ' in p['abastecimento'].split(','):
        x,y=p['x_maquete_mm'],p['y_maquete_mm'];bx=205 if p['id']=='H01' else x+3
        route('AQ_'+p['id'],'AQ',[(bx,101),(bx,y),(x,y)],'Barrilete AQ',p['id'])
route('NP00','NP',[NODES['RNP'],(235,-18)],'RNP','Barrilete NP','Rede independente; reposicao potavel somente com separacao atmosferica a projetar')
for id in ('H03','H06'):
    p=P[id];route('NP_'+id,'NP',[(p['x_maquete_mm'],-18),(p['x_maquete_mm'],p['y_maquete_mm'])],'Barrilete NP',id)
route('ES_H01','ES',[(194,186),(185,186),NODES['CG1']],'H01','CG1','Passagem sob o piso da sala a verificar com estrutura/fundacoes; alternativa de tracado pode ser necessaria')
route('ES_CG1','ES',[NODES['CG1'],(185,-60),NODES['CI1']],'CG1','CI1')
for id in ('H02','H04','H10','H05','H07','H11'):
    p=P[id];dest=p['destino_esgoto'];nx,ny=NODES[dest];x,y=p['x_maquete_mm'],p['y_maquete_mm']
    route('ES_'+id,'ES',[(x,y),(x,ny),(nx,ny)],id,dest,'Desconexao, niveis e conexoes a detalhar; tracejado indica percurso proposto sob piso')
for cs,ci in [('CS1','CI1'),('CS2','CI2')]:
    x,y=NODES[cs];cx,cy=NODES[ci];route('ES_'+cs,'ES',[(x,y),(x,cy),(cx,cy)],cs,ci)
for id,ci in [('H03','CI1'),('H06','CI2'),('H08','CI2'),('H09','CI2')]:
    p=P[id];x,y=p['x_maquete_mm'],p['y_maquete_mm'];cx,cy=NODES[ci]
    route('ES_'+id,'ES',[(x,y),(x,cy),(cx,cy)],id,ci,'Bacias sem passagem em caixa sifonada; desconexao de tanque/lavadora a detalhar')
route('ES_CI1','ES',[NODES['CI1'],NODES['CI2']],'CI1','CI2')
route('ES_CI2','ES',[NODES['CI2'],NODES['DS1']],'CI2','DS1','Destinacao sanitaria a definir apos caracterizacao do lote/concessionaria')
for cs,vt in [('CS1','VT1'),('CS2','VT2')]:
    x,y=NODES[cs];vx,vy=NODES[vt];route('VE_'+vt,'VE',[(x,y),(vx,y),(vx,vy)],'Ramal sanitario '+cs,vt,'Ponto funcional de ventilacao; derivacao, DN, altura e terminal acima da cobertura a detalhar')

par=MODEL['parametros'];roof=MODEL['cobertura'];a=roof['divisao_T1']-10;b=roof['divisao_T2']-10;d=roof['recuo']-10
ROOF=[(-10,-10),(a,-10),(a,d),(b,d),(b,-10),(par['piso_L']-10,-10),(par['piso_L']-10,par['piso_W']-10),(-10,par['piso_W']-10)]
def poly_area(poly):return abs(sum(a[0]*b[1]-b[0]*a[1] for a,b in zip(poly,poly[1:]+poly[:1])))/2
AREA=poly_area(ROOF)*F**2/1e6

def volume_chuva_l(precipitacao_mm,area_m2,coef_escoamento=1,eficiencia=1):
    vals=(precipitacao_mm,area_m2,coef_escoamento,eficiencia)
    if not all(math.isfinite(v) for v in vals):raise ValueError('Valores devem ser finitos')
    if precipitacao_mm<0 or area_m2<=0 or not 0<=coef_escoamento<=1 or not 0<=eficiencia<=1:raise ValueError('Parametros fora da faixa')
    return precipitacao_mm*area_m2*coef_escoamento*eficiencia
CHUVA=[{'cenario':'Evento hipotetico bruto','precipitacao_mm':p,'area_projetada_m2':AREA,'coef_escoamento_hipotese':1,'eficiencia_hipotese':1,'volume_calculado_l':round(volume_chuva_l(p,AREA),3)} for p in (1,10)]
CHUVA.append({'cenario':'Evento hipotetico com perdas','precipitacao_mm':10,'area_projetada_m2':AREA,'coef_escoamento_hipotese':.8,'eficiencia_hipotese':.9,'volume_calculado_l':round(volume_chuva_l(10,AREA,.8,.9),3)})

PREMISSAS={'projeto':'Casa Inteligente | NEXUS | ExpoTech','revisao':'Hidraulica residencial R01','data':'2026-11-05','estado':'DISTRIBUICAO ESQUEMATICA; SEM DIMENSIONAMENTO FINAL','unidade':'mm','conversao_maquete_arquitetura':F,'aparelhos':'Centros de referencia propostos, sem dimensoes de loucas ou cotas de conexoes','AF':'Agua potavel; fonte, pressao e reservacao pendentes','AQ':'Aquecimento central proposto; fonte de energia, potencia, vazao, temperatura e recirculacao a definir','NP':'Chuva tratada para descargas; rede separada de AF/AQ; qualidade, tratamento e reposicao a projetar','esgoto':'Rotas sob piso, sem DN, cotas ou declividade; sifoes/CS/CG/inspecoes e ventilacao a dimensionar','chuva':'Captacao proposta na cobertura R02; declividades e area efetivamente conectada a confirmar; sem dados reais de chuva','localizacao_equipamentos':'CAF/AQ1/CG1/CS1/CS2/CI1/CI2/VT1/VT2/DS1/RNP representam nos funcionais; tamanhos e afastamentos nao definidos','maquete':'Circuito fechado de demonstracao; nao tratar a agua como potavel; sem ligacao com instalacao domestica','referencias_a_consultar':'NBR 5626, NBR 8160, NBR 10844, NBR 15527; confirmar edicoes e criterios na etapa de dimensionamento'}

def in_polygon(x,y,poly):
    inside=False
    for a,b in zip(poly,poly[1:]+poly[:1]):
        if (a[1]>y)!=(b[1]>y) and x<(b[0]-a[0])*(y-a[1])/(b[1]-a[1])+a[0]:inside=not inside
    return inside

def validar():
    rooms={r['id']:r['poligono'] for r in ROOMS}
    for p in POINTS:
        x,y=p['x_maquete_mm'],p['y_maquete_mm'];assert in_polygon(x,y,rooms[p['ambiente']]),p['id']
        # Exclusao conservadora: setor completo de giro da porta, incluindo espessura zero.
        for o in OPS:
            if o['tipo']!='porta':continue
            w=WALL[o['parede']];a=o['a'];u=w['u'];rad=o['w']
            if w['eixo']=='H':
                side=-1 if w['id'] in ('R05','R06','R10','R17') else 1
                if x>=a and side*(y-u)>=0:assert math.hypot(x-a,y-u)>rad,p['id']+' no giro '+o['id']
            else:
                if x>=u and y>=a:assert math.hypot(x-u,y-a)>rad,p['id']+' no giro '+o['id']
    assert abs(AREA-85.756)<1e-9
    assert sum('AF' in p['abastecimento'].split(',') for p in POINTS)==7
    assert sum('AQ' in p['abastecimento'].split(',') for p in POINTS)==5
    assert sum('NP' in p['abastecimento'].split(',') for p in POINTS)==2
    assert all('AF' not in p['abastecimento'] and 'AQ' not in p['abastecimento'] for p in POINTS if 'NP' in p['abastecimento'])
    assert len({p['id'] for p in POINTS})==len(POINTS)
    assert all(len(r['vertices_maquete_mm'])>=2 for r in ROUTES)

def csv_write(name,rows):
    keys=list(dict.fromkeys(k for r in rows for k in r))
    with (OUT/name).open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=keys,delimiter=';');w.writeheader()
        for r in rows:w.writerow({k:json.dumps(v,ensure_ascii=False) if isinstance(v,(dict,list)) else v for k,v in r.items()})

NAVY=colors.HexColor('#183a57');GRAY=colors.HexColor('#677787');BLUE=colors.HexColor('#096a9d');RED=colors.HexColor('#c44b26');GREEN=colors.HexColor('#217647');BROWN=colors.HexColor('#815331');TEAL=colors.HexColor('#68718c')
COL={'AF':BLUE,'AQ':RED,'NP':GREEN,'ES':BROWN,'VE':TEAL}
LABEL={'AM01':(65,130),'AM02':(145,245),'AM03':(270,84),'AM04':(390,75),'AM05':(365,130),'AM06':(405,245),'AM07':(600,245),'AM08':(557,84),'AM09':(640,70),'AM10':(260,245)}

def fonts():
    for name,file in [('Nexus','DejaVuSans.ttf'),('NexusBold','DejaVuSans-Bold.ttf')]:pdfmetrics.registerFont(TTFont(name,'/usr/share/fonts/truetype/dejavu/'+file))
def paragraph(c,text,x,top,width,size=9):
    st=ParagraphStyle('p',fontName='Nexus',fontSize=size,leading=size*1.4,textColor=NAVY)
    p=Paragraph(text,st);_,h=p.wrap(width*mm,400*mm);p.drawOn(c,x*mm,top*mm-h);return h/mm

def frame(c,n,title,sub):
    c.setFillColor(NAVY);c.setFont('NexusBold',15);c.drawString(16*mm,281*mm,'CASA INTELIGENTE | NEXUS | ExpoTech')
    c.setFont('NexusBold',12);c.drawString(16*mm,267*mm,title)
    c.setFillColor(GRAY);c.setFont('Nexus',8.3);c.drawString(16*mm,260*mm,sub)
    c.setStrokeColor(BLUE);c.setLineWidth(.8);c.line(16*mm,255*mm,404*mm,255*mm)
    c.setLineWidth(.5);c.line(16*mm,28*mm,404*mm,28*mm)
    paragraph(c,'ESTUDO ACADEMICO | R01 | 05/11/2026 | Distribuicao esquematica; DN, cotas verticais e declividades a dimensionar.',16,23,365,7)
    c.setFont('NexusBold',8);c.setFillColor(NAVY);c.drawRightString(403*mm,15*mm,f'HPR-{n:02} / 04')

def segments(w):
    cursor=w['a']
    for o in sorted([o for o in OPS if o['parede']==w['id']],key=lambda o:o['a']):
        if o['a']>cursor:yield cursor,o['a']
        cursor=max(cursor,o['a']+o['w'])
    if cursor<w['b']:yield cursor,w['b']

def base(c):
    # arquitetura 1:50 em A3, coordenadas locais da R02
    s=F*mm/50;ox=29*mm;oy=112*mm
    def xy(x,y):return ox+x*s,oy+y*s
    for r in ROOMS:
        path=c.beginPath();pts=r['poligono'];path.moveTo(*xy(*pts[0]))
        for p in pts[1:]:path.lineTo(*xy(*p))
        path.close();c.setFillColor(colors.HexColor('#f5f8fb'));c.drawPath(path,fill=1,stroke=0)
    for w in WALLS:
        c.setFillColor(colors.HexColor('#d7dfe5'));c.setStrokeColor(GRAY);c.setLineWidth(.4)
        for a,b in segments(w):
            if w['eixo']=='H':c.rect(*xy(a,w['u']-1.5),(b-a)*s,3*s,stroke=1,fill=1)
            else:c.rect(*xy(w['u']-1.5,a),3*s,(b-a)*s,stroke=1,fill=1)
    for o in OPS:
        w=WALL[o['parede']];a=o['a'];b=a+o['w'];u=w['u'];rad=o['w'];c.setStrokeColor(colors.HexColor('#aab8c4'));c.setLineWidth(.4)
        if o['tipo']=='porta':
            path=c.beginPath()
            if w['eixo']=='H':
                side=-1 if w['id'] in ('R05','R06','R10','R17') else 1
                c.line(*xy(a,u),*xy(a,u+side*rad));path.moveTo(*xy(b,u))
                for j in range(1,17):path.lineTo(*xy(a+rad*math.cos(j*math.pi/32),u+side*rad*math.sin(j*math.pi/32)))
            else:
                c.line(*xy(u,a),*xy(u+rad,a));path.moveTo(*xy(u,b))
                for j in range(1,17):path.lineTo(*xy(u+rad*math.sin(j*math.pi/32),a+rad*math.cos(j*math.pi/32)))
            c.drawPath(path)
        elif w['eixo']=='H':c.line(*xy(a,u),*xy(b,u))
        else:c.line(*xy(u,a),*xy(u,b))
    c.setFillColor(GRAY);c.setFont('Nexus',7);c.drawString(29*mm,239*mm,'ARQUITETURA: mm | 1:50 em A3 a 100% | Origem local da R02')
    c.setStrokeColor(GRAY);c.setLineWidth(.4);xx1,y=xy(0,-83);xx2,_=xy(697.5,-83);c.line(xx1,y,xx2,y)
    for xx in (xx1,xx2):c.line(xx,y-1*mm,xx,y+1*mm)
    c.drawCentredString((xx1+xx2)/2,y+2*mm,'13.950 mm - envelope de paredes; largura 5.760 mm')
    return xy,s

def room_labels(c,xy):
    for r in ROOMS:
        x,y=xy(*LABEL[r['id']]);width=max(pdfmetrics.stringWidth(r['id'],'NexusBold',6.8),pdfmetrics.stringWidth(r['nome'],'Nexus',6.4))+4
        c.setFillColor(colors.white);c.roundRect(x-width/2,y-4*mm,width,7*mm,1*mm,fill=1,stroke=0)
        c.setFillColor(GRAY);c.setFont('NexusBold',6.8);c.drawCentredString(x,y,r['id']);c.setFont('Nexus',6.4);c.drawCentredString(x,y-3*mm,r['nome'])

def draw_routes(c,xy,nets):
    for r in ROUTES:
        if r['rede'] not in nets:continue
        net=r['rede'];c.setStrokeColor(COL[net]);c.setLineWidth(1 if net!='VE' else .8)
        c.setDash(3,2) if net in ('AQ','ES','VE') else c.setDash()
        pts=r['vertices_maquete_mm'];path=c.beginPath();path.moveTo(*xy(*pts[0]))
        for p in pts[1:]:path.lineTo(*xy(*p))
        c.drawPath(path)
    c.setDash()

def fixtures(c,xy,ids=None):
    for p in POINTS:
        if ids and p['id'] not in ids:continue
        x,y=xy(p['x_maquete_mm'],p['y_maquete_mm']);c.setFillColor(colors.white);c.setStrokeColor(NAVY);c.setLineWidth(.6);c.circle(x,y,1.7*mm,fill=1,stroke=1)
        c.setFillColor(NAVY);c.setFont('NexusBold',7);c.drawString(x+2.3*mm,y+1.5*mm,p['id'])

def node(c,xy,id,labeldx=0,labeldy=0):
    x,y=xy(*NODES[id]);c.setStrokeColor(NAVY);c.setFillColor(colors.white);c.setLineWidth(.6);c.rect(x-2*mm,y-1.7*mm,4*mm,3.4*mm,fill=1,stroke=1)
    c.setFillColor(NAVY);c.setFont('NexusBold',7);c.drawString(x+3*mm+labeldx*mm,y+1.5*mm+labeldy*mm,id)

def table(c,top,headers,rows,widths,size=8):
    body=ParagraphStyle('b',fontName='Nexus',fontSize=size,leading=size*1.4,textColor=NAVY);head=ParagraphStyle('h',parent=body,fontName='NexusBold',textColor=colors.white)
    data=[[Paragraph(str(t),head) for t in headers]]+[[Paragraph(str(t),body) for t in row] for row in rows]
    t=Table(data,colWidths=[v*mm for v in widths],repeatRows=1)
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),NAVY),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.HexColor('#f0f5fa'),colors.white]),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6),('VALIGN',(0,0),(-1,-1),'MIDDLE')]))
    _,h=t.wrap(385*mm,240*mm)
    if top*mm-h<33*mm:raise ValueError('Tabela ultrapassa rodape')
    t.drawOn(c,20*mm,top*mm-h);return top-h/mm

def box(c,x,y,w,h,title,desc,color=BLUE):
    c.setFillColor(colors.HexColor('#f4f7fa'));c.setStrokeColor(color);c.setLineWidth(.8);c.roundRect(x*mm,y*mm,w*mm,h*mm,2*mm,fill=1,stroke=1)
    paragraph(c,'<b>'+title+'</b><br/>'+desc,x+3,y+h-3,w-6,8.5)
def arrow(c,a,b,color=BLUE):
    x1,y1=a[0]*mm,a[1]*mm;x2,y2=b[0]*mm,b[1]*mm;c.setStrokeColor(color);c.setFillColor(color);c.setLineWidth(.8);c.line(x1,y1,x2,y2)
    t=math.atan2(y2-y1,x2-x1);path=c.beginPath();path.moveTo(x2,y2)
    for da in (-.5,.5):path.lineTo(x2-2.5*mm*math.cos(t+da),y2-2.5*mm*math.sin(t+da))
    path.close();c.drawPath(path,fill=1,stroke=0)

def pdf():
    fonts();c=canvas.Canvas(str(OUT/'NEXUS_Hidraulica_Residencial_R01.pdf'),pagesize=(420*mm,297*mm));c.setTitle('Casa Inteligente | NEXUS | ExpoTech - Hidraulica R01');c.setAuthor('Projeto NEXUS')
    frame(c,1,'Agua fria, quente e nao potavel','Centros de referencia e distribuicao proposta. Nao define cotas de conexoes, DN, pressoes ou capacidade de reservatorios.')
    xy,s=base(c);draw_routes(c,xy,('AF','AQ','NP'));room_labels(c,xy);fixtures(c,xy,[p['id'] for p in POINTS if p['abastecimento']]);node(c,xy,'CAF');node(c,xy,'AQ1',-15,3)
    c.setFillColor(GREEN);c.setFont('NexusBold',7);c.drawString(*xy(600,-13),'vem de RNP; fora da planta')
    c.setFillColor(BLUE);c.drawString(*xy(338,-49),'entrada/reservacao AF a definir')
    paragraph(c,'<b>REDES DO ESTUDO</b><br/><br/><font color="#096a9d">AF: agua fria potavel</font>, linha azul continua.<br/><br/><font color="#c44b26">AQ: agua quente potavel</font>, linha vermelha tracejada.<br/><br/><font color="#217647">NP: agua nao potavel</font>, linha verde continua.<br/><br/>CAF: no de distribuicao AF; alimentacao e reservacao pendentes.<br/><br/>AQ1: aquecimento central proposto na area de servico; tecnologia e energia a decidir.<br/><br/>RNP: reservacao de chuva tratada, sem localizacao fisica definida.',326,239,75,8.8)
    paragraph(c,'<b>PROGRAMA PROPOSTO:</b> 7 aparelhos com AF, 5 com AQ e 2 bacias sanitarias com NP. Cada circulo identifica um centro de referencia, nao a dimensao da louca. Posicoes completas nos CSVs, em mm da arquitetura e da maquete.',20,68,383,9)
    paragraph(c,'<b>COMPATIBILIZACAO:</b> tracados representam projecoes. Passagens, niveis, acessos e registros ainda serao detalhados. Preservar redes independentes; reposicao de agua potavel no sistema NP somente por solucao com separacao atmosferica a projetar. Nao ha ligacao direta AF-NP neste estudo.',20,51,383,8.8)
    c.showPage()
    frame(c,2,'Esgoto sanitario e ventilacao','Rotas propostas sob piso, sem declividades ou DN definidos. Pontos de ventilacao e caixas indicam funcoes a detalhar.')
    xy,s=base(c);draw_routes(c,xy,('ES','VE'));room_labels(c,xy);fixtures(c,xy)
    for id in ('CG1','CS1','CS2','CI1','CI2','DS1','VT1','VT2'):node(c,xy,id,0,-6 if id in ('CS1','CS2') else 0)
    for id in ('VT1','VT2'):
        x,y=xy(*NODES[id]);c.setStrokeColor(TEAL);c.line(x,y+3*mm,x,y+12*mm);c.line(x,y+12*mm,x-1.2*mm,y+10*mm);c.line(x,y+12*mm,x+1.2*mm,y+10*mm)
    paragraph(c,'<b>LEGENDA DESTE ESTUDO</b><br/><br/><font color="#815331">ES: esgoto sanitario</font>, marrom tracejado.<br/><br/><font color="#68718c">VE: ventilacao</font>, cinza tracejado; sobe acima da cobertura, sem cota final.<br/><br/>CG1: caixa de gordura da pia.<br/>CS1/CS2: desconexao/colecao dos banhos, a dimensionar.<br/>CI1/CI2: inspecoes propostas, acessiveis.<br/>DS1: destinacao sanitaria a definir.<br/><br/>Bacias nao atravessam caixas sifonadas.<br/><br/>Tanque/lavadora: desconexao a detalhar.<br/><br/>Chuva permanece separada do esgoto sanitario.',326,239,75,8.5)
    paragraph(c,'<b>INTERFERENCIA IDENTIFICADA:</b> o percurso H01-CG1 passa em projecao sob o piso da sala. Conferir estrutura, fundacoes, acesso para manutencao e alternativa de rota antes de dimensionar. A cota da saida do lote e as condicoes da concessionaria ainda nao foram definidas.',20,68,383,9)
    paragraph(c,'Derivacoes de ventilacao, fechos hidricos, conexoes, declividades, cotas de fundo e dimensoes de caixas nao estao detalhados. As linhas do desenho nao comprovam escoamento por gravidade nem viabilidade executiva. Verificar chuveiros, loucas e areas de uso junto aos pontos eletricos.',20,50,383,8.8)
    c.showPage()
    frame(c,3,'Captacao de chuva e integracao com a automacao','Esquema funcional de aproveitamento para descargas. A demonstracao de bancada e um circuito separado.')
    # Cobertura desenhada em 1:100, preservando recuo do modelo R02.
    ss=F*mm/100;ox,oy=25*mm,167*mm
    def rx(x,y):return ox+x*ss,oy+y*ss
    path=c.beginPath();path.moveTo(*rx(*ROOF[0]))
    for p in ROOF[1:]:path.lineTo(*rx(*p))
    path.close();c.setStrokeColor(NAVY);c.setFillColor(colors.HexColor('#edf3f7'));c.drawPath(path,fill=1,stroke=1)
    for xx in (a,b):c.line(*rx(xx,d),*rx(xx,298))
    c.setStrokeColor(GREEN);c.setLineWidth(2);c.line(*rx(-10,298),*rx(707.5,298))
    for xx in (115,300,530):
        x1,y1=rx(xx,160);x2,y2=rx(xx,270);c.setStrokeColor(BLUE);c.setLineWidth(.7);c.line(x1,y1,x2,y2);c.line(x2,y2,x2-1*mm,y2-2*mm);c.line(x2,y2,x2+1*mm,y2-2*mm)
    paragraph(c,'<b>COBERTURA R02 | 1:100</b><br/>Area projetada: <b>85,756 m2</b>. Recuo preservado. Setas de caimento e calha na borda superior sao propostas; sem declividade ou DN. Confirmar area efetivamente conectada e interferencias com o solar.',186,232,213,9)
    paragraph(c,'V bruto (L) = chuva (mm) x area (m2).<br/>Com perdas hipoteticas: V = P x A x C x eta.<br/>Exemplo: 10 x 85,756 x 0,80 x 0,90 = <b>617,443 L</b>.<br/><b>10 mm e os fatores sao exemplos, nao dados climaticos.</b> Esse volume nao dimensiona a cisterna nem demonstra economia/autonomia.',186,210,213,9)
    paragraph(c,'Calhas, condutores e destinacao de excedentes exigem chuva de projeto, cotas e dimensionamento. A separacao de redes segue como criterio de concepcao; tratamento e qualidade devem ser definidos antes do uso.',25,161,374,8.7)
    box(c,23,116,78,29,'CAPTACAO','Calha/condutores; tela e desvio inicial a projetar',BLUE)
    box(c,118,116,78,29,'TRATAMENTO','Selecao e controle de qualidade para uso nao potavel',BLUE)
    box(c,213,116,78,29,'RNP','Reservacao propria; nivel, extravasor e limpeza',GREEN)
    box(c,308,116,87,29,'DISTRIBUICAO NP','Bombeamento conforme pressao; descargas H03/H06',GREEN)
    for x1,x2 in ((101,118),(196,213),(291,308)):arrow(c,(x1,130),(x2,130),GREEN)
    paragraph(c,'<b>FALTA DE CHUVA:</b> reposicao com agua potavel por separacao atmosferica a detalhar. Excedentes e desvios de chuva: destinacao pluvial a definir. Nao conectar diretamente a rede potavel nem descarregar agua pluvial no coletor sanitario deste estudo.',23,109,372,8.7)
    box(c,23,55,178,31,'MAQUETE | CIRCUITO FECHADO','Recipiente -> bomba RS-385 -> sensor de fluxo -> retorno. HC-SR04 mede nivel. Bandeja e acessos para manutencao; volumes e conexoes ainda a conferir.',TEAL)
    box(c,217,55,178,31,'A05 | ESTADO REAL DO CODIGO','D8 permanece como entrada: a bomba nao e acionada. Nivel/vazao e driver aguardam ensaio. Falha de nivel/fluxo bloqueia apenas a permissao logica; nao e protecao fisica validada.',TEAL)
    paragraph(c,'O circuito de recirculacao nao trata agua nem valida o sistema predial. Referencias de concepcao: Senado Verde, Edificios Publicos Sustentaveis, pp. 30-32; CAESB PR-14/2023-DC (referencia do DF, sem presumir aplicabilidade local). Links e limites no memorial.',23,47,372,8)
    c.showPage()
    frame(c,4,'Pontos de referencia, decisoes e continuidade','Todas as coordenadas em milimetros. Os IDs correspondem as plantas HPR-01/HPR-02 e ao arquivo CSV editavel.')
    rows=[[p['id'],p['ambiente'],p['aparelho'],f"{p['x_arquitetura_mm']:g} / {p['y_arquitetura_mm']:g}",f"{p['x_maquete_mm']:g} / {p['y_maquete_mm']:g}",p['abastecimento'] or '-',p['destino_esgoto']] for p in POINTS]
    y=table(c,246,['ID','AMBIENTE','REFERENCIA PROPOSTA','X / Y ARQUITETURA','X / Y MAQUETE','AGUA','ESGOTO'],rows,[19,24,78,65,60,38,42],8.2)-8
    y-=paragraph(c,'As coordenadas indicam centros de referencia. Altura, eixo e afastamento das conexoes dependem dos aparelhos escolhidos. Os centros foram conferidos dentro dos ambientes e fora do setor de giro das portas desenhado na R02; isso nao verifica dimensoes das loucas, acessibilidade ou folgas de uso.',20,y,385,9)+5
    y-=paragraph(c,'<b>DECISOES PARA DIMENSIONAR:</b> populacao e consumo; pressao de entrada; capacidade/cotas de reservatorios; modelos e vazoes dos aparelhos; fonte de aquecimento e protecoes; materiais; comprimentos tridimensionais; chuva local; qualidade/tratamento; cotas do lote e destinacoes sanitaria/pluvial.',20,y,385,9)+5
    y-=paragraph(c,'<b>COMPATIBILIZACAO ELETRICA:</b> verificar T09/T24 e todos os pontos em relacao aos volumes finais dos chuveiros. Compatibilizar pia/bancada com T05/T06; lavadora H09 com reserva R03/T12. AQ1 deve ser compatibilizado com a reserva eletrica R04; a bomba de NP exige reserva propria. Definir tecnologia/potencia e revisar cargas. Nao acrescentar uma potencia sem identificar o equipamento.',20,y,385,9)+5
    paragraph(c,'<b>PROXIMAS ENTREGAS INDEPENDENTES DA MONTAGEM:</b> memoria de calculo hidraulica, rede de dados/seguranca e BOM por funcao. Antes de comprar ou cortar tubos, validar esta distribuicao e completar os dimensionamentos. NBR 5626, 8160, 10844 e 15527 sao referencias a consultar para a etapa seguinte, sem declaracao de atendimento nesta revisao.',20,y,385,8.7)
    c.save()

def dxf(nets,name):
    doc=ezdxf.new('R2010');doc.units=4;doc.header['$MEASUREMENT']=1;m=doc.modelspace()
    for name_,col in [('PAREDES',8),('ABERTURAS',9),('PONTOS',7),('AF',5),('AQ',1),('NP',3),('ES',30),('VE',6),('NOTAS',7)]:doc.layers.new(name_,dxfattribs={'color':col})
    for w in WALLS:
        for a,b in segments(w):
            pts=[(a,w['u']-1.5),(b,w['u']-1.5),(b,w['u']+1.5),(a,w['u']+1.5)] if w['eixo']=='H' else [(w['u']-1.5,a),(w['u']+1.5,a),(w['u']+1.5,b),(w['u']-1.5,b)]
            m.add_lwpolyline([(x*F,y*F) for x,y in pts],close=True,dxfattribs={'layer':'PAREDES'})
    for o in OPS:
        w=WALL[o['parede']];u=w['u'];a=o['a'];b=a+o['w'];pts=[(a,u),(b,u)] if w['eixo']=='H' else [(u,a),(u,b)]
        m.add_line(tuple(v*F for v in pts[0]),tuple(v*F for v in pts[1]),dxfattribs={'layer':'ABERTURAS'})
    for r in ROUTES:
        if r['rede'] in nets:m.add_lwpolyline([(x*F,y*F) for x,y in r['vertices_maquete_mm']],dxfattribs={'layer':r['rede']})
    for p in POINTS:
        x,y=p['x_arquitetura_mm'],p['y_arquitetura_mm'];m.add_circle((x,y),85,dxfattribs={'layer':'PONTOS'});m.add_text(p['id'],dxfattribs={'height':110,'insert':(x+120,y+100),'layer':'PONTOS'})
    ids=('CAF','AQ1','RNP') if 'AF' in nets else ('CG1','CS1','CS2','CI1','CI2','DS1','VT1','VT2')
    for id in ids:
        x,y=(v*F for v in NODES[id]);m.add_circle((x,y),100,dxfattribs={'layer':'PONTOS'});m.add_text(id,dxfattribs={'height':100,'insert':(x+150,y+150),'layer':'PONTOS'})
    m.add_text('NEXUS | HIDRAULICA R01 | mm | ROTAS ESQUEMATICAS SEM DN/COTAS/DECLIVIDADES',dxfattribs={'height':140,'insert':(0,6600),'layer':'NOTAS'})
    doc.saveas(OUT/name)

def main():
    validar();csv_write('Pontos_Hidraulicos_mm.csv',POINTS);csv_write('Rotas_Propostas_mm.csv',ROUTES);csv_write('Cenarios_Chuva.csv',CHUVA)
    data={'premissas':PREMISSAS,'pontos':POINTS,'nos_funcionais_maquete_mm':NODES,'rotas':ROUTES,'cobertura_maquete_mm':ROOF,'area_projetada_cobertura_m2':AREA,'cenarios_chuva':CHUVA}
    (OUT/'Modelo_Hidraulico_R01.json').write_text(json.dumps(data,ensure_ascii=False,indent=2))
    pdf();dxf(('AF','AQ','NP'),'HPR01_Agua.dxf');dxf(('ES','VE'),'HPR02_Esgoto_Ventilacao.dxf')
    print(json.dumps({'pontos':len(POINTS),'rotas':len(ROUTES),'area_cobertura_m2':AREA,'pdf':str(OUT/'NEXUS_Hidraulica_Residencial_R01.pdf')},ensure_ascii=False))
if __name__=='__main__':main()
