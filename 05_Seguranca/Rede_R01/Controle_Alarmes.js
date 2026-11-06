/* Casa Inteligente | NEXUS | ExpoTech. SIMULACAO, sem qualquer I/O fisico. */
(function(root,factory){if(typeof module==='object'&&module.exports)module.exports=factory();else root.NexusAlarmes=factory();})(typeof self!=='undefined'?self:this,function(){
  'use strict';
  const IDS=Object.freeze(['RD01','RD02','PR01','SM01','VA01','VA02']);
  class AlarmesDemo {
    constructor(){this.armed=false;this.muted=false;this.latched=new Set();this.inputs=Object.fromEntries(IDS.map(id=>[id,{value:null,time:null}]));}
    time(t){if(!Number.isFinite(t)||t<0)throw new Error('Tempo invalido');}
    sample(id,value,t){this.time(t);if(!IDS.includes(id)||typeof value!=='boolean')return false;const old=this.inputs[id];if(old.time!==null&&t<old.time)return false;this.inputs[id]={value,time:t};return true;}
    evaluate(t){this.time(t);const missing=IDS.filter(id=>{const p=this.inputs[id];return p.time===null||t<p.time||t-p.time>3000;});const validActive=id=>!missing.includes(id)&&this.inputs[id].value===true;
      const reasons=[];
      if(this.armed)for(const id of ['RD01','RD02','PR01'])if(validActive(id))reasons.push('INTRUSAO:'+id);
      if(validActive('SM01'))reasons.push('FUMACA:SM01');
      for(const id of ['VA01','VA02'])if(validActive(id))reasons.push('AGUA:'+id);
      for(const reason of reasons)if(!this.latched.has(reason)){this.latched.add(reason);this.muted=false;}
      return {origem:'SIMULACAO',armed:this.armed,muted:this.muted,alarm:this.latched.size>0,audible_virtual:this.latched.size>0&&!this.muted,reasons:[...this.latched],missing,status:this.latched.size?'ALARME RETIDO':missing.length?'SEM DADOS':this.armed?'ARMADO':'DESARMADO'};
    }
    arm(t){const s=this.evaluate(t);if(s.missing.length||s.alarm||IDS.some(id=>this.inputs[id].value!==false))return false;this.armed=true;return true;}
    disarm(t){this.time(t);this.armed=false;return this.evaluate(t);}
    mute(t){const s=this.evaluate(t);if(s.alarm)this.muted=true;return this.evaluate(t);}
    clear(t){const s=this.evaluate(t);if(s.missing.length||IDS.some(id=>this.inputs[id].value!==false))return false;this.latched.clear();this.muted=false;return true;}
  }
  return Object.freeze({IDS,AlarmesDemo});
});
