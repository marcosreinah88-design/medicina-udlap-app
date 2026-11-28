"""Ayudas para escribir casos nuevos del simulador ya en formato lineal.

C(id, bloque, tema, dif, título, paciente, motivo, (TA, FC, FR, T, SpO2), historia, pasos, perla, fuente, **sv_extra)
P(fase, pregunta, opciones, r=resultado, add=además): opciones = [(texto, 1|0, explicación), ...]; una sola correcta.
Las opciones incorrectas inventadas llevan † en su explicación (convención del simulador).
"""


def P(f, q, o, r=None, add=None):
    st = {"f": f, "q": q, "o": [[t, ok, fb] for t, ok, fb in o]}
    if r:
        st["r"] = r
    if add:
        st["add"] = add
    return st


def C(id, b, tema, dif, t, pac, mc, sv, hx, pasos, perla, src, **extra):
    ta, fc, fr, temp, sat = sv
    s = {"ta": ta, "fc": fc, "fr": fr, "t": temp, "sat": sat}
    s.update(extra)
    return {"id": id, "b": b, "tema": tema, "dif": dif, "t": t, "pac": pac, "mc": mc, "sv": s,
            "hx": hx, "pasos": pasos, "perla": perla, "src": src}
