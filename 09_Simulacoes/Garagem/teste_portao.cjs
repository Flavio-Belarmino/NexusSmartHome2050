'use strict';
const assert=require('node:assert/strict');
const {Portao}=require('./controle_portao.js');
let casos=0,verificacoes=0;
function eq(a,b){++verificacoes;assert.equal(a,b);}
function caso(nome,fn){fn();++casos;console.log('OK',nome);}
const aberto={aberto:true};
function ateFechar(){
  const p=new Portao();p.atualizar(0,{fechado:true});p.atualizar(100,{externo:true});
  p.atualizar(200,{...aberto,externo:true});p.atualizar(300,{...aberto,vao:true});
  p.atualizar(400,{...aberto,vao:true,interno:true});p.atualizar(500,{...aberto,interno:true});
  return p;
}
caso('posicao inicial desconhecida',()=>{let p=new Portao();let s=p.atualizar(0);eq(s.estado,'INICIALIZACAO');eq(s.abrir,false);eq(s.fechar,false);});
caso('entrada completa e tempo de vao livre',()=>{let p=ateFechar();eq(p.atualizar(2499,{...aberto,interno:true}).estado,'ABERTO');eq(p.atualizar(2500,{...aberto,interno:true}).estado,'FECHANDO');eq(p.atualizar(2600,{fechado:true,interno:true}).estado,'FECHADO');});
caso('saida completa',()=>{let p=new Portao();p.atualizar(0,{fechado:true});eq(p.atualizar(100,{interno:true}).sentido,'SAIDA');p.atualizar(200,{...aberto,interno:true});p.atualizar(300,{...aberto,vao:true});p.atualizar(400,{...aberto,vao:true,externo:true});p.atualizar(500,{...aberto,externo:true});eq(p.atualizar(2500,{...aberto,externo:true}).estado,'FECHANDO');});
caso('sem passagem nao fecha por tempo',()=>{let p=new Portao();p.atualizar(0,{fechado:true});p.atualizar(100,{externo:true});p.atualizar(200,aberto);eq(p.atualizar(50000,aberto).estado,'ABERTO');});
caso('obstaculo reabre',()=>{let p=ateFechar();p.atualizar(2500,{...aberto,interno:true});let s=p.atualizar(2510,{vao:true,interno:true});eq(s.estado,'ABRINDO');eq(s.fechar,false);eq(s.abrir,true);});
caso('timeout interrompe movimento',()=>{let p=new Portao();p.atualizar(0,{fechado:true});p.atualizar(100,{externo:true});let s=p.atualizar(6100);eq(s.estado,'FALHA');eq(s.abrir,false);eq(s.fechar,false);eq(s.causa,'TEMPO_DE_MOVIMENTO_EXCEDIDO');});
caso('fins de curso contraditorios',()=>{let s=new Portao().atualizar(0,{aberto:true,fechado:true});eq(s.estado,'FALHA');eq(s.abrir,false);});
caso('emergencia exige rearme',()=>{let p=new Portao();p.atualizar(0,{fechado:true});p.atualizar(1,{emergencia:true});eq(p.atualizar(2,{fechado:true}).estado,'FALHA');eq(p.atualizar(3,{fechado:true,rearmar:true}).estado,'FECHADO');});
caso('rearme sem posicao conhecida nao move',()=>{let p=new Portao();p.atualizar(0,{emergencia:true});let s=p.atualizar(1,{rearmar:true});eq(s.estado,'INICIALIZACAO');eq(s.abrir,false);eq(s.fechar,false);});
caso('aproximacoes ambiguas aguardam',()=>{let p=new Portao();p.atualizar(0,{fechado:true});eq(p.atualizar(1,{interno:true,externo:true}).estado,'FECHADO');});
caso('fechamento manual respeita obstaculo',()=>{let p=new Portao();p.atualizar(0,aberto);eq(p.atualizar(1,{...aberto,vao:true,fechar:true}).estado,'ABERTO');eq(p.atualizar(2,{...aberto,fechar:true}).estado,'FECHANDO');});
caso('novo obstaculo reinicia tempo livre',()=>{let p=ateFechar();p.atualizar(1000,{...aberto,vao:true});p.atualizar(1500,aberto);eq(p.atualizar(3499,aberto).estado,'ABERTO');eq(p.atualizar(3500,aberto).estado,'FECHANDO');});
caso('destino ocupado antes da passagem nao confirma',()=>{let p=new Portao();p.atualizar(0,{fechado:true});p.atualizar(1,{externo:true});p.atualizar(2,{...aberto,interno:true});p.atualizar(3,{...aberto,interno:true,vao:true});p.atualizar(4,{...aberto,interno:true});eq(p.atualizar(10000,{...aberto,interno:true}).estado,'ABERTO');});
caso('nova aproximacao durante fechamento reabre',()=>{let p=ateFechar();p.atualizar(2500,{...aberto,interno:true});eq(p.atualizar(2510,{externo:true,interno:true}).estado,'ABRINDO');});
caso('tempo regressivo recusado',()=>{let p=new Portao();p.atualizar(10);++verificacoes;assert.throws(()=>p.atualizar(9));});
caso('nenhuma saida simultanea',()=>{let p=ateFechar();for(let t=600;t<7000;t+=100){let s=p.atualizar(t,{});eq(s.abrir&&s.fechar,false);}});
console.log(JSON.stringify({casos,verificacoes,resultado:'APROVADO',escopo:'logica simulada, sem hardware'}));
