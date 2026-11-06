const assert=require('node:assert/strict');
const {IDS,AlarmesDemo}=require('./Controle_Alarmes.js');
let count=0;
function test(name,fn){fn();count++;console.log('OK '+name);}
function fresh(m,t=0){for(const id of IDS)m.sample(id,false,t);}
test('inicio desconhecido bloqueia armar',()=>{const m=new AlarmesDemo();assert.equal(m.arm(0),false);assert.equal(m.evaluate(0).missing.length,6);});
test('falso valido nao e dado ausente',()=>{const m=new AlarmesDemo();fresh(m);assert.equal(m.evaluate(0).status,'DESARMADO');assert.equal(m.arm(0),true);});
test('porta e PIR nao geram intrusao desarmado',()=>{const m=new AlarmesDemo();fresh(m);m.sample('RD01',true,0);m.sample('PR01',true,0);assert.equal(m.evaluate(0).alarm,false);assert.equal(m.arm(0),false);});
test('cada entrada de intrusao dispara quando armado',()=>{for(const id of ['RD01','RD02','PR01']){const m=new AlarmesDemo();fresh(m);m.arm(0);m.sample(id,true,1);assert.deepEqual(m.evaluate(1).reasons,['INTRUSAO:'+id]);}});
test('fumaça funciona desarmado',()=>{const m=new AlarmesDemo();fresh(m);m.sample('SM01',true,1);assert.equal(m.evaluate(1).alarm,true);});
test('cada vazamento funciona desarmado',()=>{for(const id of ['VA01','VA02']){const m=new AlarmesDemo();fresh(m);m.sample(id,true,1);assert.deepEqual(m.evaluate(1).reasons,['AGUA:'+id]);}});
test('desarmar nao apaga ocorrencia',()=>{const m=new AlarmesDemo();fresh(m);m.arm(0);m.sample('RD02',true,1);m.evaluate(1);assert.equal(m.disarm(2).alarm,true);});
test('silenciar so muda indicacao virtual',()=>{const m=new AlarmesDemo();fresh(m);m.sample('SM01',true,1);assert.equal(m.mute(1).audible_virtual,false);assert.equal(m.evaluate(1).alarm,true);});
test('nova causa restaura indicacao virtual',()=>{const m=new AlarmesDemo();fresh(m);m.sample('SM01',true,1);m.mute(1);m.sample('VA01',true,2);assert.equal(m.evaluate(2).audible_virtual,true);});
test('evento ativo impede limpar',()=>{const m=new AlarmesDemo();fresh(m);m.sample('SM01',true,1);assert.equal(m.clear(1),false);});
test('limpar exige retorno normal e dados atuais',()=>{const m=new AlarmesDemo();fresh(m);m.sample('SM01',true,1);m.evaluate(1);fresh(m,2);assert.equal(m.clear(2),true);assert.equal(m.evaluate(2).alarm,false);});
test('dados vencidos bloqueiam limpar e armar',()=>{const m=new AlarmesDemo();fresh(m);assert.equal(m.evaluate(3000).missing.length,0);assert.equal(m.evaluate(3001).missing.length,6);assert.equal(m.clear(3001),false);assert.equal(m.arm(3001),false);});
test('perda de dados nao e intrusao confirmada',()=>{const m=new AlarmesDemo();fresh(m);m.arm(0);assert.equal(m.evaluate(3001).alarm,false);assert.equal(m.evaluate(3001).status,'SEM DADOS');});
test('perda de dados nao apaga alarme anterior',()=>{const m=new AlarmesDemo();fresh(m);m.sample('VA02',true,1);m.evaluate(1);assert.equal(m.evaluate(4000).alarm,true);});
test('amostra atrasada ou invalida e rejeitada',()=>{const m=new AlarmesDemo();fresh(m,10);assert.equal(m.sample('RD01',true,9),false);assert.equal(m.sample('RD01','false',11),false);assert.equal(m.sample('DESCONHECIDO',false,11),false);assert.equal(m.inputs.RD01.value,false);});
test('relogio invalido rejeitado e futuro e ausente',()=>{const m=new AlarmesDemo();assert.throws(()=>m.evaluate(-1));assert.throws(()=>m.sample('RD01',true,NaN));fresh(m,10);assert.equal(m.evaluate(9).missing.length,6);});
test('reinicio volta a desconhecido sem armar',()=>{const m=new AlarmesDemo();fresh(m);m.arm(0);const reset=new AlarmesDemo();assert.equal(reset.evaluate(0).armed,false);assert.equal(reset.evaluate(0).status,'SEM DADOS');});
test('multiplas causas persistem com origem fixa',()=>{const m=new AlarmesDemo();fresh(m);m.arm(0);for(const id of IDS)m.sample(id,true,1);const s=m.evaluate(1);assert.equal(s.reasons.length,6);assert.equal(s.origem,'SIMULACAO');});
console.log(count+' cenarios passaram; sem hardware conectado.');
