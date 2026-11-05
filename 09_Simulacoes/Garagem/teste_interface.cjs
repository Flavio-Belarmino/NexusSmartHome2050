// Executa os scripts do HTML em DOM minimo. Nao e inspecao visual de navegador.
const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
const html=fs.readFileSync(__dirname+'/NEXUS_Garagem_Simulador.html','utf8');
const elementos={};for(const m of html.matchAll(/id="([^"]+)"/g))elementos[m[1]]={checked:false,value:'',textContent:'',setAttribute(k,v){this[k]=v;}};
let proximo;
const contexto=vm.createContext({document:{getElementById(id){assert.ok(elementos[id],'ID ausente: '+id);return elementos[id];}},performance:{now:()=>0},requestAnimationFrame(fn){proximo=fn;},console});
for(const m of html.matchAll(/<script>([\s\S]*?)<\/script>/g))vm.runInContext(m[1],contexto);
let tempo=0;
function avancar(ms){for(let i=0;i<ms;i+=50){tempo+=50;proximo(tempo);}}
elementos.entrada.onclick();avancar(18000);assert.equal(elementos.estado.textContent,'FECHADO');
elementos.saida.onclick();avancar(18000);assert.equal(elementos.estado.textContent,'FECHADO');
elementos.entrada.onclick();let viu=false;
for(let i=0;i<400;i++){avancar(50);if(elementos.estado.textContent==='FECHANDO'){viu=true;break;}}
assert.ok(viu);elementos.obstaculo.checked=true;avancar(100);assert.ok(['ABRINDO','ABERTO'].includes(elementos.estado.textContent));assert.equal(elementos.outFechar.textContent,'Desligado');
elementos.entrada.onclick();avancar(1800);assert.equal(elementos.estado.textContent,'ABRINDO');elementos.falha.checked=true;avancar(6500);assert.equal(elementos.estado.textContent,'FALHA');
console.log('OK: entrada, saida, obstaculo e falha nos scripts da interface HTML. Sem validacao visual ou fisica.');
