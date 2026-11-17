# -*- coding: utf-8 -*-
"""Contrôles du lot 1 WhatsApp (16/11/2026) : relit l'état des fichiers (HTML + index.md), n'écrit que le CSV.
    python -X utf8 _lot1_1611_wa_controle.py [chemin_csv]   (depuis site-v5/)"""
import os, re, sys, csv, glob, subprocess, collections
import _lot1_1611_wa as W

ROOT = W.ROOT
CSV = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "..", "..", "06-reports", "2026-11-16-etude-site", "lot1-wa", "messages.csv")
INTERDITS = re.compile(r"Isra[eë]l|ישראל|✡|\bappel|\bappeler|call us|llámanos|llamar|kosher-friendly|Kismet|Vue d'Ange|Nogentil|Bellecôte|Cospillot|Christiania|\b4810\b|Marcandou|Ilulissat|Ikamiut|Sisimiut|Refuge du Cabri|Bettaix|Opale|\bAmbre\b|מורת דרך|שיחה", re.I)
NB_CHALETS = re.compile(r"\b\d+\s+(?:chalets?|צ'אלות)", re.I)

def main():
    pages = [os.path.relpath(f, ROOT).replace(os.sep, "/") for f in sorted(glob.glob(os.path.join(ROOT, "**", "index.html"), recursive=True))]
    pages = [p for p in pages if not p.startswith("_") and W.lang_slug(p)[1] not in W.PRIVEES]
    chalets_ok = [0]; err = collections.defaultdict(list); lignes = []; longs = []; nlien = 0; lg_none = 0; maxlen = (0, "")
    parlangue = collections.Counter(); sans_nom = 0
    for rel in pages:
        l, slug = W.lang_slug(rel); typ = W.type_page(slug); s = W.lire(os.path.join(ROOT, rel)); nom = W.nom_page(s, l, slug)
        pdom = W.PAGE_DOM[typ]; textes = []
        for L in W.liens_page(s):
            if L["old"] is None: err["lien nu restant"].append(rel); continue
            t = L["old"]; textes.append(t); nlien += 1; parlangue[(typ, l)] += 1
            if len(t) > maxlen[0]: maxlen = (len(t), rel)
            if len(t) > W.MAXLEN: longs.append((rel, len(t)))
            mo = re.match(re.escape(W.HELLO[l]) + r"\s+" + re.escape(W.ORIGIN[l].split("{p}")[0]) + r"(.*?)" + re.escape(W.ORIGIN[l].split("{p}")[1]), t)
            if not (mo and nom.startswith(mo.group(1)) and len(mo.group(1)) >= 4): err["nom de page absent"].append((rel, t[:80])); sans_nom += 1
            if not W.ORIGIN_RE[l].match(t): err["mention de page absente ou autre langue"].append((rel, t[:80]))
            lg = W.lang_of(W.sans_origine(t, l))
            if lg is None: lg_none += 1
            elif lg != l: err["langue du message differente"].append((rel, lg, t[:80]))
            r = W.reste(t, l)
            d = W.dom_texte(r)
            if L["kind"] != "offre" and pdom != "both" and d in ("lyon", "alps") and d != pdom: err["sujet Lyon/Alpes inverse"].append((rel, d, t[:80]))
            for mm in (INTERDITS.search(t), NB_CHALETS.search(t)):
                if mm: err["mot interdit"].append((rel, mm.group(0), t[:80]))
        if typ == "chalet":
            gabs = {W.cap(W.corriger(W.GABARIT[g][l], l)) for g in ("general", "lyon", "alps")}
            chal = W.cap(W.corriger(W.GABARIT["chalet"][l], l))
            rs = [W.cap(W.corriger(W.reste(x, l), l)) for x in textes]
            if chal not in rs or any(r in gabs for r in rs): err["fiche chalet sans gabarit chalet ou avec lien general"].append(rel)
            chalets_ok[0] += 1
        if W.lang_slug(rel)[1] in W.PRIX_PAGES:
            nb = len(re.findall(r'class="lot1-prix"', s))
            if nb != 1: err["ligne prix absente ou doublee"].append((rel, nb))
        elif 'class="lot1-prix"' in s: err["ligne prix sur page non retenue"].append(rel)
        # message principal = texte le plus fréquent hors offres
        c = collections.Counter(t for L, t in ((L, L["old"]) for L in W.liens_page(s)) if t is not None and L["kind"] == "text")
        princ = c.most_common(1)[0][0] if c else (textes[0] if textes else "")
        nwa = len(re.findall(r'href="https://wa\.me/' + W.PH, s))
        lignes.append([rel.replace("/index.html", "/") or "/", l, typ, nwa, princ.replace("\n", " ")])
    # liens Beth Habad : comptes et valeurs identiques à HEAD
    git = ["git", "-C", ROOT]
    ref = subprocess.run(git + ["grep", "-ohE", "wa\\.me/" + W.BH + "[^\"' ]*", "HEAD", "--", "*.html"], capture_output=True, text=True).stdout.split()
    ref = sorted(x.split(":", 1)[-1] if x.startswith("HEAD:") else x for x in ref)
    now = []
    for f in glob.glob(os.path.join(ROOT, "**", "*.html"), recursive=True):
        if os.path.relpath(f, ROOT).startswith("_"): continue
        now += re.findall(r"wa\.me/" + W.BH + r"[^\"' ]*", W.lire(f))
    now = sorted(now)
    # mesure.js intact
    diff = subprocess.run(git + ["diff", "--stat", "--", "js/mesure.js"], capture_output=True, text=True).stdout.strip()
    # miroirs md : toutes les URL portent la mention de page
    md_mauvais = 0; md_total = 0
    for rel in pages:
        p = os.path.join(ROOT, rel[:-len("index.html")] + "index.md")
        if not os.path.exists(p): continue
        l = W.lang_slug(rel)[0]
        for m in re.finditer(r"https://wa\.me/" + W.PH + r"(?:\?text=([^\s)]*))?", W.lire(p)):
            md_total += 1
            if m.group(1) is None or not W.ORIGIN_RE[l].match(W.decode(m.group(1))): md_mauvais += 1
    os.makedirs(os.path.dirname(CSV), exist_ok=True)
    with open(CSV, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f, delimiter=";"); w.writerow(["page", "langue", "type", "liens_wa_Mishpacha", "message_principal_decode"]); w.writerows(lignes)
    print("pages controlees :", len(pages), "| liens wa.me/%s avec texte :" % W.PH, nlien)
    print("langue non determinable (signal faible, accepte) :", lg_none)
    print("longueur maximale :", maxlen, "| liens > %d car :" % W.MAXLEN, len(longs), sorted(set(longs))[:12])
    for k, v in err.items(): print("ERREUR", k, len(v), v[:6])
    if not err: print("0 erreur sur : lien nu, mention de page, nom de page, langue, sujet Lyon/Alpes, mots interdits, ligne prix")
    print("Beth Habad avant/apres :", len(ref), len(now), "| listes identiques :", ref == now)
    print("js/mesure.js modifie :", bool(diff), diff)
    print("index.md : liens", md_total, "sans mention de page", md_mauvais)
    print("fiches chalet controlees :", chalets_ok[0])
    print("CSV :", os.path.abspath(CSV))

if __name__ == "__main__":
    main()
