#!/usr/bin/env python3
"""Portada: 'etapas de la carrera' muestra la etapa actual (5/10), no los semestres con guías. Idempotente."""
import sys, re
OLD_T='[semsWith.length+" / "+SEMS.length,"etapas de la carrera"]'
NEW_T='[(SEMS.findIndex(s=>s.n===SEM_ACTUAL)+1)+" / "+SEMS.length,"etapas de la carrera"]'
DECL='const SEM_ACTUAL=5; /* semestre que cursa Marcos ahora */'
for p in sys.argv[1:]:
    s=open(p,encoding='utf-8').read()
    if NEW_T in s: print(p,'ya parchado'); continue
    assert s.count(OLD_T)==1 and s.count(DECL)==1, p
    s=s.replace(DECL+'\n','',1)
    s=s.replace('/* franja de cifras */','/* franja de cifras */\n'+DECL,1)
    s=s.replace(OLD_T,NEW_T,1)
    open(p,'w',encoding='utf-8').write(s); print(p,'parchado')
