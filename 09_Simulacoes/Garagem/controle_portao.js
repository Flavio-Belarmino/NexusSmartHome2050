/* Casa Inteligente | NEXUS | ExpoTech. Modelo de sequencia A07 R01.
 * Entradas e atuador sao simulados. Nao envia comandos a hardware.
 */
(function(root,factory){
  if(typeof module==='object'&&module.exports)module.exports=factory();
  else root.NexusGaragem=factory();
})(typeof globalThis!=='undefined'?globalThis:this,function(){
  'use strict';
  class Portao {
    constructor({tempoMovimento=6000,tempoLivre=2000}={}){
      if(!(tempoMovimento>0&&tempoLivre>=0))throw Error('Tempos invalidos');
      this.tempoMovimento=tempoMovimento;this.tempoLivre=tempoLivre;
      this.estado='INICIALIZACAO';this.causa='';this.entrou=0;this.ultimoTempo=0;
      this.sentido=null;this.viuVao=false;this.viuDestino=false;this.livreDesde=null;
      this.anterior={externo:false,interno:false};
    }
    transicao(estado,t){this.estado=estado;this.entrou=t;this.livreDesde=null;}
    falhar(causa,t){this.causa=causa;this.transicao('FALHA',t);}
    iniciar(sentido,t){this.sentido=sentido;this.viuVao=false;this.viuDestino=false;this.transicao('ABRINDO',t);}
    atualizar(t,entrada={}){
      if(!Number.isFinite(t)||t<0||t<this.ultimoTempo)throw Error('Tempo deve ser crescente');
      this.ultimoTempo=t;
      const i=Object.assign({externo:false,interno:false,vao:false,aberto:false,fechado:false,emergencia:false,abrir:false,fechar:false,rearmar:false},entrada);
      const sobeExterno=!!i.externo&&!this.anterior.externo,sobeInterno=!!i.interno&&!this.anterior.interno;
      const anterior=this.anterior;this.anterior={externo:!!i.externo,interno:!!i.interno};
      if(i.aberto&&i.fechado){this.falhar('FINS_DE_CURSO_CONTRADITORIOS',t);return this.saida();}
      if(i.emergencia){this.falhar('EMERGENCIA',t);return this.saida();}
      if(i.rearmar){
        this.causa='';this.sentido=null;this.viuVao=this.viuDestino=false;
        this.transicao(i.fechado?'FECHADO':i.aberto?'ABERTO':'INICIALIZACAO',t);
        return this.saida();
      }
      if(this.estado==='FALHA')return this.saida();
      if(this.estado==='INICIALIZACAO'){
        if(i.fechado)this.transicao('FECHADO',t);else if(i.aberto)this.transicao('ABERTO',t);
        return this.saida();
      }
      if(this.estado==='FECHADO'){
        if(i.abrir)this.iniciar(i.externo&&!i.interno?'ENTRADA':i.interno&&!i.externo?'SAIDA':null,t);
        else if(sobeExterno&&!i.interno)this.iniciar('ENTRADA',t);
        else if(sobeInterno&&!i.externo)this.iniciar('SAIDA',t);
        return this.saida();
      }
      if(this.estado==='ABRINDO'&&i.aberto)this.transicao('ABERTO',t);
      else if(this.estado==='FECHANDO'){
        if(i.vao){this.transicao('ABRINDO',t);return this.saida();}
        if(i.abrir||sobeExterno||sobeInterno){this.iniciar(sobeExterno?'ENTRADA':sobeInterno?'SAIDA':null,t);return this.saida();}
        if(i.fechado){this.sentido=null;this.transicao('FECHADO',t);return this.saida();}
      }
      if((this.estado==='ABRINDO'||this.estado==='FECHANDO')&&t-this.entrou>=this.tempoMovimento){
        this.falhar('TEMPO_DE_MOVIMENTO_EXCEDIDO',t);return this.saida();
      }
      if(this.estado==='ABRINDO'||this.estado==='ABERTO'){
        if(i.vao)this.viuVao=true;
        const destino=this.sentido==='ENTRADA'?i.interno:this.sentido==='SAIDA'?i.externo:false;
        const antesDestino=this.sentido==='ENTRADA'?anterior.interno:this.sentido==='SAIDA'?anterior.externo:false;
        if(this.viuVao&&destino&&!antesDestino)this.viuDestino=true;
      }
      if(this.estado==='ABERTO'){
        if(i.fechar&&!i.vao){this.transicao('FECHANDO',t);return this.saida();}
        const origem=this.sentido==='ENTRADA'?i.externo:this.sentido==='SAIDA'?i.interno:true;
        const passou=!!this.sentido&&this.viuVao&&this.viuDestino&&!origem&&!i.vao;
        if(!passou)this.livreDesde=null;
        else{
          if(this.livreDesde===null)this.livreDesde=t;
          if(t-this.livreDesde>=this.tempoLivre)this.transicao('FECHANDO',t);
        }
      }
      return this.saida();
    }
    saida(){return {estado:this.estado,causa:this.causa,abrir:this.estado==='ABRINDO',fechar:this.estado==='FECHANDO',sentido:this.sentido,passagemConfirmada:this.viuVao&&this.viuDestino};}
  }
  return {Portao};
});
