"""NEXUS: supervisor local de telemetria; nunca envia comandos ao Arduino."""
import argparse
import csv
import datetime as dt
import json
import math
from pathlib import Path
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

MODULOS={'A01','A02','A03','A04','A05','A08','A09'}

def interpretar(linha):
    if not isinstance(linha,str) or len(linha)>4096:return None
    try:
        if linha.lstrip().startswith('{'):
            def recusar(_):raise ValueError('Numero JSON nao finito')
            d=json.loads(linha,parse_constant=recusar)
            if not isinstance(d,dict) or d.get('module') not in MODULOS:return None
            def finito(v):
                if isinstance(v,float):return math.isfinite(v)
                if isinstance(v,dict):return all(finito(x) for x in v.values())
                if isinstance(v,list):return all(finito(x) for x in v)
                return True
            if not finito(d):return None
            if d['module']=='A04':
                if type(d.get('valid')) is not bool:return None
                if d['valid']:
                    for nome,limites in (('temperature_c',(-40,80)),('humidity_pct',(0,100))):
                        v=d.get(nome)
                        if type(v) not in (int,float) or not math.isfinite(v) or not limites[0]<=v<=limites[1]:return None
                else:d['temperature_c']=d['humidity_pct']=None
            return d
        if linha.startswith('ms='):
            d={'module':'A01'}
            for parte in linha.strip().split():
                k,v=parte.split('=',1)
                try:v=int(v)
                except ValueError:pass
                d[k]=v
            return d if 'PIR' in d and 'LED' in d else None
    except (ValueError,TypeError,RecursionError):return None
    return None

class Registro:
    def __init__(self,origem,arquivo=None):
        self.origem=origem;self.arquivo=Path(arquivo) if arquivo else None
        self.lock=threading.Lock();self.modulos={};self.recebidos=0
    def adicionar(self,d):
        agora=dt.datetime.now(dt.timezone.utc).isoformat()
        with self.lock:
            self.recebidos+=1;self.modulos[d['module']]={'dados':d,'recebido_utc':agora,'monotonic':time.monotonic()}
            if self.arquivo:
                self.arquivo.parent.mkdir(parents=True,exist_ok=True)
                cabecalho=not self.arquivo.exists() or self.arquivo.stat().st_size==0
                with self.arquivo.open('a',newline='',encoding='utf-8') as f:
                    w=csv.writer(f)
                    if cabecalho:w.writerow(['recebido_utc','origem','modulo','json'])
                    w.writerow([agora,self.origem,d['module'],json.dumps(d,ensure_ascii=False,allow_nan=False)])
    def estado(self):
        with self.lock:
            return {'origem':self.origem,'recebidos':self.recebidos,'modulos':{k:{'dados':v['dados'],'recebido_utc':v['recebido_utc'],'idade_s':round(time.monotonic()-v['monotonic'],1)} for k,v in self.modulos.items()}}

PAGINA='''<!doctype html><html lang="pt-BR"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>NEXUS | Supervisor USB</title><style>body{font:16px/1.6 system-ui;margin:35px auto;padding:0 24px;max-width:1000px;background:#eff4f8;color:#19344d}h1{font-size:30px}.tag{padding:10px 16px;border-radius:10px;background:#d6eaf8;font-weight:bold}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:16px;margin-top:20px}.card{background:white;padding:22px;border-radius:12px;border:1px solid #dae4ed}pre{white-space:pre-wrap;overflow-wrap:anywhere;font-size:14px}.small{font-size:13px;color:#526b80}</style><h1>Casa Inteligente | NEXUS</h1><p>Supervisor de bancada · somente leitura</p><div class="tag" id="origem">Conectando ao servidor local...</div><p class="small">Cada cartão mostra o último quadro recebido e sua idade. Uma leitura antiga ou sem validação não comprova o estado atual do equipamento. Este supervisor não envia comandos.</p><div class="grid" id="cards"></div><p id="total"></p><script>async function atualizar(){try{const r=await fetch('/api/estado');const s=await r.json();document.getElementById('origem').textContent=s.origem==='DEMONSTRACAO'?'DEMONSTRAÇÃO · valores de exemplo, sem sensores':'SERIAL USB · dados recebidos da placa';document.getElementById('total').textContent='Quadros recebidos: '+s.recebidos;const area=document.getElementById('cards');area.replaceChildren();for(const[k,v]of Object.entries(s.modulos)){const card=document.createElement('section');card.className='card';const h=document.createElement('h2');h.textContent=k;const t=document.createElement('p');t.className='small';t.textContent='Recebido há '+v.idade_s+' s · '+v.recebido_utc;const p=document.createElement('pre');p.textContent=JSON.stringify(v.dados,null,2);card.append(h,t,p);area.append(card);}if(!s.recebidos)area.textContent='Aguardando quadros válidos. Verifique porta, velocidade e programa carregado.';}catch(e){document.getElementById('origem').textContent='Servidor local indisponível';}setTimeout(atualizar,1000);}atualizar();</script></html>'''

def criar_handler(registro):
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            if self.path=='/':conteudo=PAGINA.encode();tipo='text/html; charset=utf-8'
            elif self.path=='/api/estado':conteudo=json.dumps(registro.estado(),ensure_ascii=False,allow_nan=False).encode();tipo='application/json; charset=utf-8'
            else:self.send_error(404);return
            self.send_response(200);self.send_header('Content-Type',tipo);self.send_header('Cache-Control','no-store');self.send_header('Content-Length',str(len(conteudo)));self.end_headers();self.wfile.write(conteudo)
        def log_message(self,*_):pass
    return Handler

def main():
    p=argparse.ArgumentParser(description=__doc__)
    g=p.add_mutually_exclusive_group(required=True);g.add_argument('--demo',action='store_true');g.add_argument('--porta');g.add_argument('--listar-portas',action='store_true')
    p.add_argument('--baud',type=int,default=115200);p.add_argument('--http',type=int,default=8765);p.add_argument('--csv')
    args=p.parse_args()
    if args.listar_portas:
        try:from serial.tools import list_ports
        except ImportError:p.error('Instale pyserial: python -m pip install -r requirements.txt')
        for item in list_ports.comports():print(item.device,item.description)
        return
    dispositivo=None
    if args.porta:
        try:
            import serial
            dispositivo=serial.Serial(args.porta,args.baud,timeout=1)
        except ImportError:p.error('Instale pyserial: python -m pip install -r requirements.txt')
        except Exception as e:p.error('Falha ao abrir a porta: '+str(e))
    registro=Registro('DEMONSTRACAO' if args.demo else 'SERIAL_USB',args.csv)
    parar=threading.Event()
    def ler():
        exemplos=[{'module':'A04','valid':True,'temperature_c':24.0,'humidity_pct':55.0},{'module':'A05','distance_cm':20,'level_pct':50,'pulses':0,'flow_l_min':None,'flow_enabled':False,'pump_permission':False,'actuator_enabled':False}]
        j=0
        while not parar.is_set():
            if args.demo:
                registro.adicionar(dict(exemplos[j%len(exemplos)]));j+=1;parar.wait(2)
            else:
                try:
                    linha=dispositivo.readline(4097)
                    if len(linha)>4096 or (linha and not linha.endswith(b'\n')):continue
                    d=interpretar(linha.decode('utf-8',errors='replace'))
                    if d:registro.adicionar(d)
                except Exception as e:
                    print('Leitura serial interrompida:',e,flush=True);return
    worker=threading.Thread(target=ler,daemon=True);worker.start()
    servidor=ThreadingHTTPServer(('127.0.0.1',args.http),criar_handler(registro))
    print(f'NEXUS | {registro.origem} | http://127.0.0.1:{args.http}',flush=True)
    try:servidor.serve_forever()
    except KeyboardInterrupt:pass
    finally:
        parar.set();servidor.server_close();worker.join(timeout=2)
        if dispositivo:dispositivo.close()

if __name__=='__main__':main()
