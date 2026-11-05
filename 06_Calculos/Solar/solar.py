"""NEXUS: estimativas explicitas de energia, sem controlar circuito de carga."""
import argparse
import json
import math

def estimar(painel_w, hsp, fator, carga_w=None, bateria_v=None, bateria_ah=None, dod=None, eficiencia=None):
    for valor in (painel_w,hsp,fator,carga_w,bateria_v,bateria_ah,dod,eficiencia):
        if valor is not None and not math.isfinite(valor):raise ValueError('Todas as premissas devem ser finitas.')
    if not (painel_w > 0 and hsp > 0 and hsp <= 24 and 0 < fator <= 1):
        raise ValueError('Potencia/HSP positivos; HSP <= 24; fator entre 0 e 1.')
    if carga_w is not None and carga_w <= 0:
        raise ValueError('Carga deve ser positiva.')
    dados={'natureza':'ESTIMATIVA_SEM_MEDICAO','painel_w_nominal':painel_w,'hsp_assumida':hsp,'fator_assumido':fator,'energia_solar_wh_dia':painel_w*hsp*fator}
    if carga_w is not None:
        dados['carga_w_assumida']=carga_w
        dados['horas_equivalentes_de_carga_por_dia']=dados['energia_solar_wh_dia']/carga_w
    bateria=(bateria_v,bateria_ah,dod,eficiencia)
    if any(x is not None for x in bateria):
        if not all(x is not None for x in bateria):
            raise ValueError('Informar tensao, capacidade em Ah, fracao utilizavel e eficiencia juntas.')
        if not (bateria_v>0 and bateria_ah>0 and 0<dod<=1 and 0<eficiencia<=1):
            raise ValueError('Premissas invalidas da bateria.')
        dados['energia_bateria_wh_nominal']=bateria_v*bateria_ah
        dados['energia_bateria_wh_util_estimada']=bateria_v*bateria_ah*dod*eficiencia
        if carga_w is not None:dados['autonomia_bateria_h_estimada']=dados['energia_bateria_wh_util_estimada']/carga_w
    return dados

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--painel-w',type=float,default=1.5)
    p.add_argument('--hsp',type=float,required=True)
    p.add_argument('--fator',type=float,required=True)
    p.add_argument('--carga-w',type=float)
    p.add_argument('--bateria-v',type=float)
    p.add_argument('--bateria-ah',type=float)
    p.add_argument('--dod',type=float)
    p.add_argument('--eficiencia',type=float)
    a=p.parse_args()
    try: print(json.dumps(estimar(a.painel_w,a.hsp,a.fator,a.carga_w,a.bateria_v,a.bateria_ah,a.dod,a.eficiencia),ensure_ascii=False,indent=2,allow_nan=False))
    except ValueError as e:p.error(str(e))

if __name__=='__main__': main()
