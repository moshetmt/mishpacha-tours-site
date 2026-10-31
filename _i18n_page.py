# -*- coding: utf-8 -*-
"""30/10 : moteur commun des traductions FR / ES / HE d'une page générée par _build_guide.py (même mécanique que
_verbier_i18n.py du 29/10, sortie dans une fonction pour servir Gstaad, Davos et « Ailleurs sur demande »).
traduire(S, FR, ES, HE, force) : rend la page traduite avec _build_guide, greffe le <main>, le title, la description et
les og dans la copie préparée fr|es|he/<S>/index.html (pied et bouton WhatsApp flottant repris de Crans-Montana dans la
même langue). Ne s'applique qu'à une copie encore marquée data-i18n="todo" (sauf force). Lancer avec py -3.14 depuis site-v5."""
import io, os, re, shutil, importlib.util, html
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import _build_guide as G
import _build_i18n as I

def charger(S):
    spec = importlib.util.spec_from_file_location("p", f"_pages/{S}.py"); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m.PAGE

def page(EN, lang, T):
    """PAGE anglais où chaque texte est remplacé par sa traduction (même ordre de sections)."""
    P = dict(EN); secs = []; k = 0
    for s in EN["sections"]:
        s = dict(s); t = T["sections"][k]; k += 1
        if s["type"] in ("text", "beige"): s["h2"], s["html"] = t
        elif s["type"] == "steps": s["h2"], s["items"] = t
        elif s["type"] == "map": s["h2"], s["note"] = t
        elif s["type"] == "faq": s["h2"], s["items"] = t
        elif s["type"] == "cta": s["txt"], s["msg"] = t
        secs.append(s)
    P.update(slug=f"_tmp-{EN['slug']}-{lang}", title=T["title"], desc=T["desc"], h1=T["h1"], ital=T["ital"], intro=T["intro"], chips=T["chips"],
             crumb=(EN["crumb"][0], T["crumb"]), sections=secs, related=[(u, t) for (u, _), t in zip(EN["related"], T["related"])], source=T["source"])
    return P

def nbsp_fr(h):
    """Typographie française dans le texte (pas dans les balises) : espace insécable avant : ; ? ! et dans les nombres."""
    def f(m):
        t = m.group(0)
        t = re.sub(r" ([:;?!])", "\u00a0\\1", t)
        t = re.sub(r"(\d) (\d{3})", "\\1\u00a0\\2", t)
        t = re.sub(r"(\d) (h|m|km|min|minutes|heures)\b", "\\1\u00a0\\2", t)
        return t
    return re.sub(r">[^<]+<", f, h)

def traduire(S, FR, ES, HE, force=False):
    EN = charger(S)
    for lang, T in (("fr", FR), ("es", ES), ("he", HE)):
        dst = f"{lang}/{S}/index.html"
        cur = I.rd(dst)
        if 'data-i18n="todo"' not in cur and not force: print("déjà traduit", dst); continue
        P = page(EN, lang, T)
        G.build(P)
        out = io.open(f"{P['slug']}/index.html", encoding="utf-8").read(); shutil.rmtree(P["slug"])
        main = out[out.index("<main>"):out.index("</main>") + 7]
        main = main.replace(f'<p class="source">{T["source"]} Compiled by Mishpacha Tours from these sources. Checked {G.CHECKED}.</p>', f'<p class="source">{T["source"]}</p>')
        for a, b in T["fixe"].items(): main = main.replace(a, b)
        main = I.absolutize(main, S)
        for q in I.LOT:
            qp = f"/{q}/" if q else "/"
            main = re.sub(r'href="' + re.escape(qp) + r'(#[^"]*)?"', lambda mm: f'href="/{lang}{qp}{mm.group(1) or ""}"', main)
        if lang == "fr": main = nbsp_fr(main)
        h = cur[:cur.index("<main>")] + main + cur[cur.index("</main>") + 7:]
        tt, dd = html.escape(T["title"]), html.escape(T["desc"])
        if lang == "fr": tt, dd = nbsp_fr(">" + tt + "<")[1:-1], nbsp_fr(">" + dd + "<")[1:-1]
        h = re.sub(r"<title>.*?</title>", f"<title>{tt} | Mishpacha Tours</title>", h, count=1)
        for k in ('name="description"', 'property="og:description"', 'name="twitter:description"'):
            h = re.sub(r'(<meta ' + k + r' content=")[^"]*', lambda mm: mm.group(1) + dd, h)
        for k in ('property="og:title"', 'name="twitter:title"'):
            h = re.sub(r'(<meta ' + k + r' content=")[^"]*', lambda mm: mm.group(1) + f"{tt} | Mishpacha Tours", h)
        ref = I.rd(f"{lang}/kosher-crans-montana/index.html")
        pied = re.search(r'<footer class="pied">.*?</footer>', ref, re.S).group(0)
        h = re.sub(r'<footer class="pied">.*?</footer>', lambda _: pied, h, count=1, flags=re.S)
        flot = re.search(r'<a class="wa-flottant"[^>]*>.*?</a>', ref, re.S).group(0)
        h = re.sub(r'<a class="wa-flottant"[^>]*>.*?</a>', lambda _: flot, h, count=1, flags=re.S)
        h = h.replace(' data-i18n="todo"', "", 1)
        I.wr(dst, h); print("traduit", dst)

FIXE = {
  "fr": {"Home": "Accueil", "Ask on WhatsApp": "Écrire sur WhatsApp", "Get a quote": "Demander un devis", "Same-day reply, never on Shabbat.": "Réponse le jour même, jamais pendant Shabbat.", "Keep <i>reading</i>": "Pour <i>aller plus loin</i>"},
  "es": {"Home": "Inicio", "Ask on WhatsApp": "Escribir por WhatsApp", "Get a quote": "Pedir presupuesto", "Same-day reply, never on Shabbat.": "Respuesta el mismo día, nunca en Shabat.", "Keep <i>reading</i>": "Siga <i>leyendo</i>"},
  "he": {"Home": "דף הבית", "Ask on WhatsApp": "כתבו לנו בוואטסאפ", "Get a quote": "בקשו הצעת מחיר", "Same-day reply, never on Shabbat.": "מענה באותו יום, לעולם לא בשבת.", "Keep <i>reading</i>": "להמשך <i>קריאה</i>"},
}
