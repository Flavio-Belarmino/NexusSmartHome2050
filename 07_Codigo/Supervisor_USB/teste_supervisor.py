import csv
import json
import tempfile
from pathlib import Path
import threading
import unittest
import urllib.request
from http.server import ThreadingHTTPServer
from supervisor import interpretar,Registro,criar_handler

class TesteSupervisor(unittest.TestCase):
    def test_json_valido(self):
        self.assertEqual(interpretar('{"module":"A04","valid":true,"temperature_c":24,"humidity_pct":55}')['module'],'A04')
    def test_falha_nao_vira_zero(self):
        d=interpretar('{"module":"A04","valid":false,"temperature_c":24,"humidity_pct":55}')
        self.assertIsNone(d['temperature_c'])
    def test_linhas_invalidas(self):
        for linha in ('ajuda','{}','[]','{"module":"X"}','{"module":"A02","angle_command_deg":1e999}','{"module":"A04","valid":true,"temperature_c":NaN,"humidity_pct":50}','{"module":"A04","valid":true,"temperature_c":"24","humidity_pct":50}','x'*4097):
            self.assertIsNone(interpretar(linha))
    def test_a01(self):
        d=interpretar('ms=100 bruto=300 filtrado=310 PIR=1 modo=AUTO pronto=1 calibrado=1 escuro=1 LED=1')
        self.assertEqual(d['LED'],1);self.assertEqual(d['module'],'A01')
    def test_csv_origem_e_cabecalho(self):
        with tempfile.TemporaryDirectory() as d:
            f=Path(d)/'dados.csv';r=Registro('DEMONSTRACAO',f)
            r.adicionar({'module':'A05','level_pct':None});r.adicionar({'module':'A05','level_pct':40})
            with f.open() as arquivo:linhas=list(csv.reader(arquivo))
            self.assertEqual(len(linhas),3);self.assertEqual(linhas[1][1],'DEMONSTRACAO')
            self.assertEqual(r.estado()['recebidos'],2)
    def test_http(self):
        r=Registro('DEMONSTRACAO');r.adicionar({'module':'A02','enabled':False})
        server=ThreadingHTTPServer(('127.0.0.1',0),criar_handler(r));t=threading.Thread(target=server.serve_forever);t.start()
        try:
            base='http://127.0.0.1:'+str(server.server_address[1])
            with urllib.request.urlopen(base+'/api/estado') as resposta:s=json.loads(resposta.read())
            self.assertEqual(s['origem'],'DEMONSTRACAO');self.assertEqual(s['recebidos'],1)
            with urllib.request.urlopen(base) as resposta:self.assertIn(b'NEXUS',resposta.read())
        finally:server.shutdown();t.join();server.server_close()
if __name__=='__main__':unittest.main()
