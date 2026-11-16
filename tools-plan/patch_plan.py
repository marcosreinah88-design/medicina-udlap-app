#!/usr/bin/env python3
"""Plan de estudio por examen (v2) en «Calendario y pendientes».

Reemplaza el build() del calendario por el de tools-plan/plan.js (reparte los temas por el tiempo libre de
cada día, Mi horario, pendientes, días sin estudiar; reacomoda si te atrasas) y conecta lo demás.
Idempotente. Uso: python3 tools-plan/patch_plan.py [site/index.html site/app.html copia-del-artefacto.html]
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
FRAG = open(os.path.join(HERE, "plan.js"), encoding="utf-8").read().rstrip("\n") + "\n"


def sub1(src, old, new, name):
    if new in src:
        return src
    if src.count(old) != 1:
        raise SystemExit(f"[{name}] no encontré exactamente una vez: {old[:70]!r}")
    return src.replace(old, new)


def patch(src):
    # 1) el bloque del plan
    if "/*plan2*/" in src:
        src = re.sub(r"  /\*plan2\*/.*?  /\*/plan2\*/\n", lambda m: FRAG, src, count=1, flags=re.S)
    else:
        a = src.index("  /* ---------- el plan ---------- */\n  function build(){")
        b = src.index("  /* App de Mac: le pasa a la app los avisos", a)
        src = src[:a] + FRAG + src[b:]
    # 2) el plan se guarda junto con exámenes y pendientes (se sincroniza)
    src = sub1(src, "let state={exams:[],done:{},tasks:[]},", "let state={exams:[],done:{},tasks:[],plan:planClean()},", "state")
    src = sub1(src, "    return {exams,done,tasks};\n  }", "    return {exams,done,tasks,plan:planClean(x&&x.plan)};\n  }", "clean")
    src = sub1(src, "await ref.set({exams:state.exams,done:state.done,tasks:state.tasks,v:1})",
               "await ref.set({exams:state.exams,done:state.done,tasks:state.tasks,plan:state.plan,v:1})", "set")
    src = sub1(src, "if(snap.exists){state=clean(snap.data());\n", "if(snap.exists){state=clean(snap.data());planMerge(state,local);\n", "merge")
    src = sub1(src, "    state.tasks=state.tasks.filter(p=>!p.done||p.done>=lim);\n  }",
               "    state.tasks=state.tasks.filter(p=>!p.done||p.done>=lim);\n    planPrune(lim,keep);\n  }", "prune")
    # 3) tareas del plan: tiempo, dificultad, atrasado y «Mañana»
    old = ('    return `<label class="task ${it.kind}${done?" done":""}" style="--c:${it.e.color}"><input type="checkbox" data-key="${esc(it.key)}"${done?" checked":""}>'
           '<span class="tx"><b>${esc(it.text)}</b>${it.sub?`<small>${esc(it.sub)}</small>`:""}</span>${link}</label>`;')
    new = ('    const meta=planMeta(it);\n'
           '    return `<label class="task ${it.kind}${done?" done":""}${it.late&&!done?" late":""}" style="--c:${it.e.color}"><input type="checkbox" data-key="${esc(it.key)}"${done?" checked":""}>'
           '<span class="tx"><b>${esc(it.text)}</b>${it.late&&!done?\'<em class="pl-late">Atrasado</em>\':""}${meta?`<small>${esc(meta)}</small>`:""}</span>${link}${planActs(it,done)}</label>`;')
    src = sub1(src, old, new, "taskHTML")
    # 4) carga de cada día, resumen por examen, ajustes y aviso en «Hoy toca»
    src = sub1(src, '`<div class="dayh">${esc(nice(d))} <small>${rel(diff(t,d))}</small></div>`',
               '`<div class="dayh">${esc(nice(d))} <small>${rel(diff(t,d))}</small>${planLoad(d)}</div>`', "dayh")
    src = sub1(src, '"No hay más días de estudio programados.":"Todavía no hay exámenes."}</p>`;\n',
               '"No hay más días de estudio programados.":"Todavía no hay exámenes."}</p>`;\n    planRender(t,days);\n', "planRender")
    src = sub1(src, "    /* plan de los próximos días */\n", "    planToday(t);\n    /* plan de los próximos días */\n", "planToday")
    # 5) en el calendario del mes: «No puedo estudiar este día»
    src = sub1(src, "      box.hidden=false;\n    }else box.hidden=true;", "      planDay(box,selDay);box.hidden=false;\n    }else box.hidden=true;", "planDay")
    return src


def main():
    root = os.path.dirname(HERE)
    files = sys.argv[1:] or [os.path.join(root, "site/index.html"), os.path.join(root, "site/app.html")]
    for f in files:
        s = open(f, encoding="utf-8").read()
        n = patch(s)
        if n != s:
            open(f, "w", encoding="utf-8").write(n)
            print("plan2 →", f)
        else:
            print("sin cambios", f)


if __name__ == "__main__":
    main()
