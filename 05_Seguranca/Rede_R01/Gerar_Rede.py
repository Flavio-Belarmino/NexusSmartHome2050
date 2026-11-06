"""NEXUS - Rede e seguranca R01. Posicoes/rotas propostas, sem hardware ou rede ativa."""
from pathlib import Path
import importlib.util, json, csv, math
import ezdxf
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
OUT=Path(__file__).resolve().parent;REPO=OUT.parents[1]
helper=REPO/'03_Hidraulica/Residencial_R01/Gerar_Estudo.py'
spec=importlib.util.spec_from_file_location('nexus_pranchas',helper);h=importlib.util.module_from_spec(spec);spec.loader.exec_module(h)
h.LABEL['AM01']=(65,145);h.LABEL['AM05']=(320,130)
F=h.F;M=h.MODEL;NAVY=h.NAVY;BLUE=h.BLUE;GRAY=h.GRAY;GREEN=h.GREEN;ORANGE=h.RED
# Centros propostos. CT01 e residencial; a eletronica da maquete permanece na central externa R02.
ITEMS=[
('CT01','AM09','Central de dados/automacao',640,45,1500,'REDE','PROPOSTO','ONT/roteador/switch; alojamento, ventilacao e energia a detalhar'),
('AP01','AM05','Ponto de acesso Wi-Fi',360,120,2600,'REDE','PROPOSTO','Posicao inicial; sem garantia de cobertura ou capacidade'),
('TD01','AM01','Ponto de dados social',75,50,300,'REDE','PROPOSTO','Posicao de uso; caixa/parede e mobiliario a compatibilizar'),
('TD02','AM06','Ponto de dados quarto 1',405,180,300,'REDE','PROPOSTO','Posicao de uso; caixa/parede e mobiliario a compatibilizar'),
('TD03','AM07','Ponto de dados quarto 2',620,200,300,'REDE','PROPOSTO','Posicao de uso; caixa/parede e mobiliario a compatibilizar'),
('TD04','AM09','Ponto de dados de manutencao',650,65,750,'REDE','PROPOSTO','Posto de uso proximo a central'),
('CM01','EXTERIOR','Camera entrada',-20,65,2400,'SEGURANCA','PROPOSTO','Reserva residencial IP; nao equivale a OV7670 conectada'),
('CM02','EXTERIOR','Camera lateral',610,305,2400,'SEGURANCA','PROPOSTO','Enquadramento e garagem a compatibilizar; sem campo de visao calculado'),
('AC01','EXTERIOR','RFID',-18,35,1100,'SEGURANCA','POSICAO_R02','Leitor do inventario; ensaio A03 compara UID, sem liberar fechadura'),
('PR01','AM01','Presenca/intrusao',65,120,1800,'SEGURANCA','POSICAO_R02','Mesmo PIR da iluminacao; compartilhar leitura, sem duplicar sensor'),
('RD01','PORTA_P01','Contato porta principal',1.5,34.5,2100,'SEGURANCA','COMPLEMENTO','Contato/suporte e interface ainda a definir'),
('RD02','PORTA_P02','Contato porta lateral',184.5,286.5,2100,'SEGURANCA','COMPLEMENTO','Contato/suporte e interface ainda a definir'),
('SM01','AM05','Referencia de fumaca',430,120,2600,'SEGURANCA','COMPLEMENTO','Posicao academica; nao dimensiona deteccao/cobertura de incendio'),
('VA01','AM02','Agua junto a pia',192,181,0,'SEGURANCA','COMPLEMENTO','Sensor dedicado e ponto real de acumulacao a definir'),
('VA02','AM04','Agua junto a lavadora',467,21,0,'SEGURANCA','COMPLEMENTO','Sensor dedicado; vazao isolada nao confirma vazamento'),
('AL01','AM09','Sinalizacao de alarme',640,80,2200,'SEGURANCA','COMPLEMENTO','Indicacao demonstrativa; carga/driver e sinalizacao real a definir')]
POINTS=[{'id':id,'ambiente':am,'funcao':fn,'x_maquete_mm':x,'y_maquete_mm':y,'z_maquete_mm':z/F,'x_arquitetura_mm':x*F,'y_arquitetura_mm':y*F,'z_arquitetura_mm':z,'grupo':gr,'estado':st,'observacao':obs} for id,am,fn,x,y,z,gr,st,obs in ITEMS]
P={p['id']:p for p in POINTS};ROUTES=[]
for id in ('TD01','TD02','TD03','TD04','AP01','CM01','CM02'):
    p=P[id];x,y=p['x_maquete_mm'],p['y_maquete_mm'];start=(640,45)
    pts=[start,(640,120),(x,120),(x,y)] if id!='TD04' else [start,(650,45),(650,65)]
    if id=='CM01':pts=[start,(640,120),(-25,120),(-25,65),(x,y)]
    pts=[pt for i,pt in enumerate(pts) if i==0 or pt!=pts[i-1]]
    plano=sum(math.dist(a,b) for a,b in zip(pts,pts[1:]))*F
    vertical=abs(2600-P['CT01']['z_arquitetura_mm'])+abs(2600-p['z_arquitetura_mm'])
    ROUTES.append({'id':'CB_'+id,'origem':'CT01','destino':id,'tipo_proposto':'Cabo de dados Cat6; conectores/PoE a compatibilizar','vertices_maquete_mm':pts,'comprimento_projecao_mm':round(plano,2),'subidas_descidas_adotadas_mm':vertical,'comprimento_geometrico_m':round((plano+vertical)/1000,3),'reserva_conectores_patchcords':'Nao incluida','estado':'ESTIMATIVA DE PERCURSO; NAO E LISTA DE CORTE'})

MATRIX=[
['Acesso','RC522 + solenoide 6 V','UID autorizado acende LED no A03; D7 sem acionamento','Interface, driver, fonte e confirmacao de porta; ensaio fisico'],
['Intrusao','1 PIR, compartilhado','PIR/portas virtuais disparam somente com intrusao armada','2 contatos de porta; politica de acesso e firmware integrado'],
['Fumaca/incendio','Sem sensor identificado','Entrada SM01 virtual independente do modo de intrusao','Definir sistema real e cobertura conforme projeto especifico'],
['Vazamento','Sem sensores dedicados','VA01/VA02 virtuais; ocorrencias retidas','Sensores adequados; ensaiar agua, limpeza e falsos eventos'],
['CFTV','2 modulos OV7670','Nenhuma imagem capturada nesta revisao','Identificar FIFO/pinos/captura; residencia IP e outra arquitetura'],
['Rede/IoT','Mega + ESP32','Supervisor USB existente; Wi-Fi/MQTT ainda propostos','Placa ESP32, interfaces, firmware, broker e ensaio de rede'],
['Garagem','Simulador existente','Sensores/atuadores virtuais, com obstaculo e falhas','Mecanismo e deteccoes proprias; nao retirar HC-SR04 do reservatorio'],
['Smart Grid','Experimento solar separado','Nao ha medicao/comando da rede de energia','Medidor/interface/escopo; simulacao nao comprova integracao eletrica']]
BOM=[
{'item':'PIR','quantidade_proposta':1,'escopo':'MAQUETE','inventario':'1 disponivel','acao':'Compartilhar PR01 entre iluminacao e intrusao'},
{'item':'Contato de porta','quantidade_proposta':2,'escopo':'MAQUETE','inventario':'Nao identificado','acao':'Confirmar tipo, contato, interface e fixacao'},
{'item':'Deteccao de fumaca','quantidade_proposta':1,'escopo':'DEMONSTRACAO','inventario':'Nao identificado','acao':'Definir dispositivo; posicao SM01 nao comprova cobertura'},
{'item':'Deteccao de agua','quantidade_proposta':2,'escopo':'MAQUETE','inventario':'Nao identificado','acao':'Definir tecnologia e interface VA01/VA02'},
{'item':'Sinalizador/driver','quantidade_proposta':1,'escopo':'MAQUETE','inventario':'Conjunto nao identificado','acao':'Definir carga; nao ligar diretamente no pino'},
{'item':'Interface UART 5 V / 3,3 V','quantidade_proposta':1,'escopo':'MAQUETE','inventario':'Nao identificado','acao':'Verificar especificacoes em ambos os sentidos; ESP32 sem GPIO escolhido'},
{'item':'OV7670','quantidade_proposta':2,'escopo':'BANCADA','inventario':'2 disponiveis','acao':'Captura pendente; nao contabilizar como camera IP/PoE funcionando'},
{'item':'Ponto de dados','quantidade_proposta':4,'escopo':'RESIDENCIA','inventario':'Nao e compra de maquete','acao':'Terminais/caixas e mobiliario a compatibilizar'},
{'item':'Ponto de acesso','quantidade_proposta':1,'escopo':'RESIDENCIA','inventario':'Nao e compra de maquete','acao':'Cobertura/capacidade por estudo e ensaio'},
{'item':'Camera IP','quantidade_proposta':2,'escopo':'RESIDENCIA','inventario':'Nao confundir com OV7670','acao':'Modelo, fluxo, gravacao, energia e campo de visao a escolher'},
{'item':'ONT/roteador/switch','quantidade_proposta':'Conjunto a selecionar','escopo':'RESIDENCIA','inventario':'Nao e compra de maquete','acao':'7 terminais + 1 uplink = 8 portas; com 2 reservas, prever capacidade >=10 portas'},
{'item':'Cabos de dados','quantidade_proposta':7,'escopo':'RESIDENCIA','inventario':'Comprimento geometrico calculado','acao':'Sem patchcords, folgas e percurso final; nao comprar por esta estimativa'}]

CONTRACT={'projeto':'Casa Inteligente | NEXUS | ExpoTech','versao':'proposta-r01','implementacao':'CONTRATO FUTURO; NAO IMPLEMENTADO PELO SIMULADOR OU FIRMWARE','transporte':'Mega Serial1 -> interface -> ESP32 -> Wi-Fi -> broker local autenticado; TLS a configurar','sentido_inicial':'Somente telemetria; sem topico de comando de atuador','topico_exemplo':'nexus/maquete/estado','campos_propostos':{'schema':'nexus.estado.v1','origem':'BANCADA ou MAQUETE; nunca substituir SIMULACAO por leitura fisica','modulo':'identificador do modulo','seq':'contador monotono na sessao','uptime_ms':'tempo desde inicio da sessao, sem presumir UTC','valido':'booleano','valor':'dado ou null','unidade':'identificador da grandeza'},'pendencias':['modelo ESP32 e GPIOs','enquadramento UART/tamanho/CRC ou deteccao de erros','reconexao, sequencia/sessao e idade dos dados','autenticacao e certificados','permissoes do broker e interfaces','validacao ponta a ponta'],'proibicoes':['credenciais e UID reais no repositorio','acionar cargas por pacote recebido nesta etapa','ligacao direta de TX 5 V ao ESP32','tratar leitura antiga como evento atual']}

PREMISSAS={'projeto':'Casa Inteligente | NEXUS | ExpoTech','revisao':'Rede e seguranca R01','data':'2026-11-05','geometria':'R02 preservada; coordenadas locais, fator 20; alturas propostas','centrais':'CT01 residencial em AM09. Na maquete, manter central externa da R02; CT01 nao e instrucao para alojar placas em escala','rede':'Fibra ate ONT a compatibilizar; distribuicao cabeada em estrela e Wi-Fi propostos','seguranca':'Posicoes e logica academicas, sem declaracao de cobertura/conformidade ou protecao de pessoas','cameras':'Setas apenas direcao; sem alcance, lentes, pixel/metragem ou reconhecimento','simulador':'Entradas virtuais locais; nao captura dados nem controla equipamentos','comprimentos':'Projecao mais subidas/descidas hipoteticas a plano 2600 mm; sem folgas, patchcords ou reserva; nao liberar compra','garagem':'Dimensoes/atuador/sensores independentes, ainda nao localizados nesta revisao'}

def csv_write(name,rows):
    keys=list(dict.fromkeys(k for r in rows for k in r))
    with (OUT/name).open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=keys,delimiter=';');w.writeheader()
        for r in rows:w.writerow({k:json.dumps(v,ensure_ascii=False) if isinstance(v,(dict,list,tuple)) else v for k,v in r.items()})

def validar():
    rooms={r['id']:r['poligono'] for r in h.ROOMS}
    for p in POINTS:
        if p['ambiente'] in rooms:assert h.in_polygon(p['x_maquete_mm'],p['y_maquete_mm'],rooms[p['ambiente']]),p['id']
    source={r['id']:r for r in csv.DictReader((REPO/'01_Arquitetura/R02/DADOS/Locacao_Pontos_mm.csv').open(encoding='utf-8-sig'),delimiter=';')}
    for id in ('AC01','PR01'):
        for axis in ('x','y','z'):assert P[id][axis+'_maquete_mm']==float(source[id][axis+'_maquete_mm'])
    assert len(ROUTES)==7 and len({r['destino'] for r in ROUTES})==7
    assert all(r['vertices_maquete_mm'][0]==(640,45) for r in ROUTES)
    assert len({p['id'] for p in POINTS})==len(POINTS)

def frame(c,n,title,sub):
    c.setFillColor(NAVY);c.setFont('NexusBold',15);c.drawString(16*mm,281*mm,'CASA INTELIGENTE | NEXUS | ExpoTech')
    c.setFont('NexusBold',12);c.drawString(16*mm,267*mm,title);c.setFillColor(GRAY);c.setFont('Nexus',8.3);c.drawString(16*mm,260*mm,sub)
    c.setStrokeColor(BLUE);c.setLineWidth(.8);c.line(16*mm,255*mm,404*mm,255*mm);c.setLineWidth(.5);c.line(16*mm,28*mm,404*mm,28*mm)
    h.paragraph(c,'ESTUDO ACADEMICO | R01 | 05/11/2026 | Posicoes e interfaces propostas; sem comprovacao de funcionamento fisico.',16,23,365,7)
    c.setFillColor(NAVY);c.setFont('NexusBold',8);c.drawRightString(403*mm,15*mm,f'RS-{n:02} / 04')

def symbol(c,xy,p):
    x,y=xy(p['x_maquete_mm'],p['y_maquete_mm']);col=BLUE if p['grupo']=='REDE' else ORANGE
    c.setStrokeColor(col);c.setFillColor(colors.white);c.setLineWidth(.7)
    if p['id']=='CT01':c.rect(x-2.5*mm,y-2*mm,5*mm,4*mm,fill=1,stroke=1)
    else:c.circle(x,y,1.6*mm,fill=1,stroke=1)
    c.setFont('NexusBold',7);c.setFillColor(col)
    dx,dy=(-14,2) if p['id']=='CT01' else (2.3,1.6)
    if p['id'] in ('RD01','RD02'):dx,dy=2.3,-4
    c.drawString(x+dx*mm,y+dy*mm,p['id'])

def pdf():
    h.fonts();c=canvas.Canvas(str(OUT/'NEXUS_Rede_Seguranca_R01.pdf'),pagesize=(420*mm,297*mm));c.setTitle('Casa Inteligente | NEXUS | ExpoTech - Rede e seguranca R01');c.setAuthor('Projeto NEXUS')
    frame(c,1,'Rede de dados: central, pontos e percursos','Topologia residencial em estrela. Cabos e alturas sao propostas; nao existe rede fisica instalada nesta revisao.')
    xy,s=h.base(c)
    for r in ROUTES:
        pts=r['vertices_maquete_mm'];c.setStrokeColor(BLUE);c.setLineWidth(.7);c.setDash(2,2) if r['destino'].startswith('CM') else c.setDash();path=c.beginPath();path.moveTo(*xy(*pts[0]))
        for pt in pts[1:]:path.lineTo(*xy(*pt))
        c.drawPath(path)
    c.setDash();h.room_labels(c,xy)
    for p in POINTS:
        if p['grupo']=='REDE' or p['id'].startswith('CM'):symbol(c,xy,p)
    h.paragraph(c,'<b>LEGENDA DO ESTUDO</b><br/><br/>CT01: central residencial em AM09, com ONT/roteador/switch a selecionar.<br/><br/>TD01-TD04: quatro pontos de dados.<br/><br/>AP01: ponto de acesso; cobertura Wi-Fi nao calculada.<br/><br/>CM01/CM02: reservas cabeadas para cameras residenciais IP.<br/><br/>Linhas: cabos individuais propostos em estrela. Linha tracejada identifica destinos de cameras.<br/><br/>Entrada de fibra e acomodacao da central ainda dependem do lote e dos equipamentos.',326,239,75,8.5)
    total=sum(r['comprimento_geometrico_m'] for r in ROUTES)
    h.paragraph(c,f'<b>ESTIMATIVA GEOMETRICA:</b> sete enlaces, soma de {total:.3f} m, com plano de percurso adotado a 2.600 mm. Inclui subidas/descidas hipoteticas, sem folgas, patchcords ou reservas. Os cruzamentos nao indicam emendas. Percurso executivo, segregacao das instalacoes e terminacoes ainda precisam ser compatibilizados.',20,68,383,8.8)
    h.paragraph(c,'<b>PORTAS:</b> 7 terminais + 1 uplink = 8 portas ocupadas no switch proposto; com duas reservas, capacidade de pelo menos 10 portas. PoE, potencia, gravacao e banda dependem dos equipamentos. CT01 e da residencia: na maquete, preservar a central externa da R02 e conferir espaco para placas/conectores.',20,50,383,8.8)
    c.showPage()
    frame(c,2,'Seguranca: acesso, intrusao, fumaca e agua','Posicoes academicas. Campos de deteccao, cobertura de cameras e atendimento normativo nao estao demonstrados.')
    xy,s=h.base(c);h.room_labels(c,xy)
    for p in POINTS:
        if p['grupo']=='SEGURANCA':symbol(c,xy,p)
    for id,end in [('CM01',(-20,35)),('CM02',(560,305))]:
        x,y=xy(P[id]['x_maquete_mm'],P[id]['y_maquete_mm']);xx,yy=xy(*end);c.setStrokeColor(ORANGE);c.setLineWidth(.7);c.line(x,y,xx,yy);ang=math.atan2(yy-y,xx-x)
        for da in (-.5,.5):c.line(xx,yy,xx-2*mm*math.cos(ang+da),yy-2*mm*math.sin(ang+da))
    h.paragraph(c,'<b>LEGENDA DO ESTUDO</b><br/><br/>AC01: RFID; posicao R02.<br/>PR01: PIR da iluminacao, compartilhado com intrusao; posicao R02.<br/><br/>RD01/RD02: contatos de portas a acrescentar.<br/><br/>SM01: referencia de fumaca; dispositivo/cobertura pendentes.<br/><br/>VA01/VA02: deteccao de agua junto a pia/lavadora, a acrescentar.<br/><br/>AL01: sinalizacao demonstrativa a definir.<br/><br/>CM01/CM02: setas apenas de direcao. Modelos, lentes, iluminacao e enquadramento pendentes.',326,239,75,8.5)
    h.paragraph(c,'<b>COMPATIBILIZACAO:</b> nenhum sensor do reservatorio ou servo do brise foi transferido para a garagem. PR01 usa uma unica leitura compartilhada. Ainda nao foram atribuidos GPIOs aos novos sensores. A captura com OV7670 depende do modulo, interface, memoria e software; os modulos do inventario nao equivalem a cameras IP/PoE conectadas.',20,68,383,8.8)
    h.paragraph(c,'A deteccao de fumaca e de agua nesta etapa funciona apenas no simulador por entradas virtuais. Isso nao valida sensores fisicos, cobertura de incendio, atuacao de sirene, protecao de pessoas ou fechamento de valvula. A definicao de um sistema real exige projeto e equipamentos proprios.',20,49,383,8.8)
    c.showPage()
    frame(c,3,'Topologia e interfaces de comunicacao','Distinguir rede da residencia, comunicacao futura da maquete e supervisor USB que ja foi preparado.')
    h.paragraph(c,'<b>RESIDENCIA | PROPOSTA</b>',20,246,380,10)
    for x,w,title,desc in [(20,68,'FIBRA / ONT','Entrada e operadora a definir'),(113,68,'ROTEADOR','Separacao e permissoes de rede a configurar'),(206,68,'SWITCH','Enlaces dedicados; energia PoE e banda a dimensionar'),(299,100,'TERMINAIS','TD01-04, AP01 e cameras IP; gravacao a definir')]:h.box(c,x,196,w,35,title,desc,BLUE)
    for a,b in ((88,113),(181,206),(274,299)):h.arrow(c,(a,213),(b,213),BLUE)
    h.paragraph(c,'<b>MAQUETE | PROPOSTA DE TELEMETRIA</b>',20,183,380,10)
    for x,w,title,desc in [(20,68,'MEGA','Serial1: D18 TX1 / D19 RX1'),(113,68,'INTERFACE','Niveis compativeis 5 V / 3,3 V; nao ligar diretamente'),(206,68,'ESP32','Modelo e GPIOs pendentes; Wi-Fi a implementar'),(299,100,'BROKER / PAINEL LOCAL','MQTT autenticado, TLS a configurar; telemetria sem comando de atuadores')]:h.box(c,x,133,w,35,title,desc,GREEN)
    for a,b in ((88,113),(181,206),(274,299)):h.arrow(c,(a,150),(b,150),GREEN)
    h.paragraph(c,'<b>DISPONIVEL PARA ENSAIO:</b> Mega -> USB -> supervisor no computador, um modulo de bancada por vez. Programa testado por software; leitura da porta fisica ainda nao ensaiada. O simulador de alarmes e separado e nao envia dados a essa rede. Seu limite de validade de 3 s e um parametro virtual.',20,120,380,9)
    h.paragraph(c,'<b>CONTRATO FUTURO:</b> origem, modulo, sequencia/sessao, tempo, validade, valor e unidade. Dado vencido deve aparecer como indisponivel. MQTT, autenticacao/TLS, enquadramento serial e reconexao ainda nao foram implementados. Nao publicar SSID/senha, UID de cartao ou credenciais reais no repositorio.',20,98,380,9)
    h.paragraph(c,'<b>SMART GRID:</b> reservar a interface de medicao/energia no projeto predial. O painel solar de bancada continua como experimento separado; nao ha conexao com a rede de distribuicao nem balanco de cargas integrado demonstrado.',20,76,380,9)
    h.paragraph(c,'Referencias tecnicas: Arduino Mega 2560 (pinagem UART e logica de 5 V); Espressif ESP-FAQ/GPIO e ESP-MQTT; OMNIVISION OV7670. Links e limites no README. Esta folha nao escolhe circuito de adaptacao ou software de ponte por suposicao.',20,53,380,8.2)
    c.showPage()
    frame(c,4,'Matriz funcional e testes antes da montagem','O que temos, o que e apenas simulacao e qual evidencia ainda precisa ser produzida.')
    y=h.table(c,246,['FUNCAO','MATERIAL RECEBIDO','ESTADO DESTA REVISAO','PROXIMA VERIFICACAO'],MATRIX,[36,68,127,149],8)-8
    y-=h.paragraph(c,'<b>SIMULADOR DE ALARMES:</b> intrusao depende de armar; fumaca/agua independem desse modo. Ocorrencias ficam retidas ate todas as entradas voltarem ao normal com dados atuais. Silenciar altera apenas um indicador virtual; nova causa reativa a indicacao. Perda de amostras nao e classificada como intrusao confirmada.',20,y,380,9)+5
    y-=h.paragraph(c,'<b>TESTAR AGORA:</b> abrir o HTML com Controle_Alarmes.js na mesma pasta; armar e abrir porta; desarmar e conferir retencao; normalizar/limpar; simular fumaca/agua; pausar amostras e observar SEM DADOS. Exportar o registro JSON identificado como SIMULACAO. Nao apresentar esse arquivo como leitura de sensor real.',20,y,380,9)+5
    h.paragraph(c,'Depois, identificar componentes e executar os ensaios de bancada dos modulos existentes. Definir os dispositivos complementares e interfaces antes de atribuir novos pinos ou energizar cargas. Ainda faltam testes de rede, captura de imagem, sensores fisicos e firmware integrado.',20,y,380,8.8)
    c.save()

def dxf(group,name):
    doc=ezdxf.new('R2010');doc.units=4;m=doc.modelspace()
    for layer,col in [('PAREDES',8),('REDE',5),('SEGURANCA',30),('CABOS',3),('NOTAS',7)]:doc.layers.new(layer,dxfattribs={'color':col})
    for w in h.WALLS:
        for a,b in h.segments(w):
            pts=[(a,w['u']-1.5),(b,w['u']-1.5),(b,w['u']+1.5),(a,w['u']+1.5)] if w['eixo']=='H' else [(w['u']-1.5,a),(w['u']+1.5,a),(w['u']+1.5,b),(w['u']-1.5,b)]
            m.add_lwpolyline([(x*F,y*F) for x,y in pts],close=True,dxfattribs={'layer':'PAREDES'})
    if group=='REDE':
        for r in ROUTES:m.add_lwpolyline([(x*F,y*F) for x,y in r['vertices_maquete_mm']],dxfattribs={'layer':'CABOS'})
    for p in POINTS:
        if p['grupo']!=group and not (group=='REDE' and p['id'].startswith('CM')):continue
        x,y,z=p['x_arquitetura_mm'],p['y_arquitetura_mm'],p['z_arquitetura_mm'];m.add_circle((x,y),85,dxfattribs={'layer':group});m.add_text(p['id']+f' z={z}',dxfattribs={'height':100,'insert':(x+120,y+120),'layer':group})
    m.add_text('NEXUS | REDE/SEGURANCA R01 | mm | ESTUDO SEM COBERTURA/EXECUCAO VALIDADA',dxfattribs={'height':130,'insert':(0,6800),'layer':'NOTAS'});doc.saveas(OUT/name)

def main():
    validar();csv_write('Pontos_Rede_Seguranca_mm.csv',POINTS);csv_write('Cabos_Dados_Estimativa.csv',ROUTES);csv_write('Complementos_por_Escopo.csv',BOM)
    (OUT/'Modelo_Rede_Seguranca_R01.json').write_text(json.dumps({'premissas':PREMISSAS,'pontos':POINTS,'enlaces':ROUTES,'complementos':BOM},ensure_ascii=False,indent=2))
    (OUT/'Contrato_Telemetria_Proposto.json').write_text(json.dumps(CONTRACT,ensure_ascii=False,indent=2))
    pdf();dxf('REDE','RS01_Rede_Dados.dxf');dxf('SEGURANCA','RS02_Seguranca.dxf')
    print(json.dumps({'pontos':len(POINTS),'enlaces':len(ROUTES),'comprimento_geometrico_m':sum(r['comprimento_geometrico_m'] for r in ROUTES)},ensure_ascii=False))
if __name__=='__main__':main()
