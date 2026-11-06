# -*- coding: utf-8 -*-
"""Accueils FR, ES et HE sur la structure de l'accueil EN validé (charte LV, Moshé 02/11). Idempotent. À lancer après _charte_lv_partout.py.

Repris de l'accueil EN : héros court (libellé « Alpes · Lyon », titre avec mot-clé, sous-titre, « strictement casher », un bouton,
plus de chercheur sous la vidéo), libellés de section (lv-eyebrow), « Comment ça marche » avec les pictos père / mère / enfant
(enfant à 72 %, mêmes fichiers que l'EN), section Lyon en trois cartes photo, bloc Contact avec son libellé.
Gardé de chaque langue : <head> (title, description, JSON-LD, hreflang), en-tête, pied, bande des 4 visuels, rail des 8 chalets,
voyages, textes déjà traduits et validés (étapes, Lyon), bloc Contact (bouton vers /xx/plan-your-trip/ et WhatsApp : le formulaire
court de l'EN, js/court.js, n'existe qu'en anglais).
Phrases nouvelles = celles du dictionnaire T ci-dessous ; l'hébreu suit le lexique du skill relecture-hebreu.
python _accueils_lv.py   (depuis site-v5/)"""
import io
import os
import re

os.chdir(os.path.dirname(os.path.abspath(__file__)))

T = {
    "fr": {
        "eyebrow_hero": "Alpes · Lyon", "h1": 'Vacances <em class="lv-cle">casher</em> <i>dans les Alpes</i>',
        "sous": "Chalet privé, chef privé, Chabbat et minyan. Tout est organisé pour vous.",
        "rassure": "Strictement casher · Chomer Chabbat", "bouton": "Organiser mon séjour",
        "e_chalets": "Chalets", "e_trips": "Voyages", "e_how": "Votre séjour", "how_h2": 'Comment ça <i><em class="lv-cle">marche</em></i>',
        "e_lyon": "Patrimoine juif de Lyon", "lyon_h2": "Le patrimoine juif de Lyon, <i>sur la route</i>",
        "lyon_chapo": "L'aéroport de Lyon est à environ deux heures des stations. Faites une halte en chemin, avec une guide juive, pratiquante et membre de la communauté.",
        "c1_eti": "La seule visite à l'intérieur", "c1_titre": "La Grande Synagogue et le patrimoine juif de Lyon",
        "c1_info": "Cinq visites privées · à partir de 290 € par groupe", "c1_lien": "Les cinq visites",
        "c2_eti": "L'Escale à Lyon", "c2_titre": "Trois heures entre le vol et les pistes",
        "c3_eti": "Guide gratuit", "c3_titre": "Chabbat, repas casher, synagogues",
        "lyon_note": "Visite en français, en anglais ou en espagnol · Jamais le Chabbat", "e_contact": "Contact",
        "alt_stopover": "La rue Juiverie dans le Vieux Lyon", "alt_guide": "Bougies de Chabbat",
    },
    "es": {
        "eyebrow_hero": "Alpes · Lyon", "h1": 'Vacaciones <em class="lv-cle">kosher</em> <i>en los Alpes</i>',
        "sous": "Chalet privado, chef privado, Shabat y minyán. Todo organizado para usted.",
        "rassure": "Estrictamente kosher · Shomer Shabat", "bouton": "Planear mi estancia",
        "e_chalets": "Chalets", "e_trips": "Viajes", "e_how": "Su estancia", "how_h2": 'Cómo <i><em class="lv-cle">funciona</em></i>',
        "e_lyon": "El Lyon judío", "lyon_h2": "El Lyon judío, <i>en el camino</i>",
        "lyon_chapo": "El aeropuerto de Lyon está a unas dos horas de las estaciones. Haga una parada en el camino, con una guía judía, observante y parte de la comunidad.",
        "c1_eti": "La única visita por dentro", "c1_titre": "La Gran Sinagoga y el Lyon judío",
        "c1_info": "Cinco visitas privadas · desde 290 € por grupo", "c1_lien": "Las cinco visitas",
        "c2_eti": "La Escala", "c2_titre": "Tres horas entre el vuelo y las pistas",
        "c3_eti": "Guía gratuita", "c3_titre": "Shabat, comida kosher, sinagogas",
        "lyon_note": "Guiadas en español, inglés o francés · Nunca en Shabat", "e_contact": "Contacto",
        "alt_stopover": "La rue Juiverie en el Viejo Lyon", "alt_guide": "Velas de Shabat",
    },
    "he": {
        "eyebrow_hero": "האלפים · ליון", "h1": 'חופשת סקי <em class="lv-cle">כשרה</em> <i>באלפים</i>',
        "sous": "צ'אלה פרטית, שף פרטי, שבת ומניין. הכול מאורגן בשבילכם.",
        "rassure": "כשר למהדרין · שומר שבת", "bouton": "לתכנן את החופשה",
        "e_chalets": "צ'אלות", "e_trips": "חופשות", "e_how": "החופשה שלכם", "how_h2": 'איך זה <i><em class="lv-cle">עובד</em></i>',
        "e_lyon": "יהדות ליון", "lyon_h2": "יהדות ליון, <i>בדרך</i>",
        "lyon_chapo": "שדה התעופה של ליון נמצא כשעתיים מהאתרים. עצרו בדרך, עם מדריכה יהודייה, שומרת מצוות וחלק מהקהילה.",
        "c1_eti": "הסיור היחיד בפנים", "c1_titre": "בית הכנסת הגדול ויהדות ליון",
        "c1_info": 'חמישה סיורים פרטיים · מ-<bdi dir="ltr">290 €</bdi> לקבוצה', "c1_lien": "חמשת הסיורים",
        "c2_eti": "עצירת ביניים", "c2_titre": "שלוש שעות בין הטיסה למסלולים",
        "c3_eti": "מדריך חינם", "c3_titre": "שבת, אוכל כשר, בתי כנסת",
        "lyon_note": "ההדרכה באנגלית, בצרפתית או בספרדית · לעולם לא בשבת", "e_contact": "צור קשר",
        "alt_stopover": "ליון העתיקה", "alt_guide": "נרות שבת",
    },
}
MARQUE = "<!--ACCUEIL-LV-->"


def accueil(lang):
    t = T[lang]
    p = f"{lang}/index.html"
    s = io.open(p, encoding="utf-8", newline="").read()
    s0 = s
    pre = f"/{lang}"
    # 1. héros : bloc texte de l'EN, plus de chercheur sous la vidéo (ni de son script de préremplissage)
    if MARQUE not in s:
        a, b = s.index("<!--LUXE-HERO-->"), s.index("<!--/LUXE-HERO-->")
        hero = (f'<!--LUXE-HERO-->{MARQUE}<div class="hero-texte">\n    <p class="lv-eyebrow">{t["eyebrow_hero"]}</p>\n'
                f'    <h1>{t["h1"]}</h1>\n    <p class="hero-sous">{t["sous"]}</p>\n    <p class="lv-reassure">{t["rassure"]}</p>\n'
                f'    <a class="btn-hero lv-plan" href="{pre}/plan-your-trip/">{t["bouton"]}</a>\n  </div>\n</section>\n')
        s = s[:a] + hero + s[b:]
        s = re.sub(r"/\*prefill\*/.*?/\*/prefill\*/", "", s, flags=re.S)
    # 2. libellés de section
    def eyebrow(sel, txt, after):
        nonlocal s
        i = s.find(sel)
        if i < 0: return
        j = s.find(after, i)
        if s[j:j + 200].find('class="lv-eyebrow"') >= 0 or s[i:j].find('class="lv-eyebrow"') >= 0: return
        k = j + len(after)
        s = s[:k] + f'<p class="lv-eyebrow">{txt}</p>' + s[k:]
    eyebrow('id="chalet">', t["e_chalets"], 'id="chalet">')
    eyebrow('id="trips">', t["e_trips"], '<div class="wrap centre">')
    # 3. « Comment ça marche » : pictos famille de l'EN, libellé, mot-clé
    m = re.search(r'<section class="ss beige etapes" id="how">.*?</section>', s, re.S)
    sec = m.group(0)
    if "pere-A-skis" not in sec:
        imgs = ['<img src="/img/illus/famille/pere-A-skis.svg" alt="" width="1109" height="951" loading="lazy">',
                '<img src="/img/illus/famille/mere.svg" alt="" width="819" height="1019" loading="lazy">',
                '<img class="lv-enfant" src="/img/illus/famille/garcon-B-boule-de-neige.svg" alt="" width="875" height="926" loading="lazy">']
        lis = re.findall(r"<li>.*?</li>", sec, re.S)
        neuf = sec
        for li, im in zip(lis, imgs):
            neuf = neuf.replace(li, "<li>" + im + re.sub(r"^<li>(?:<img[^>]*>)?", "", li), 1)
        neuf = re.sub(r'<h2 class="centre">.*?</h2>', f'<p class="lv-eyebrow">{t["e_how"]}</p>\n    <h2 class="centre">{t["how_h2"]}</h2>', neuf, count=1, flags=re.S)
        s = s.replace(sec, neuf)
    # 4. Lyon en trois cartes photo (structure de l'EN)
    m = re.search(r'<section class="clair ss beige ac-lyon" id="tours">.*?</section>', s, re.S)
    if m:
        alt1 = re.search(r'<div class="ac-lyon-photo"><img [^>]*alt="([^"]*)"', m.group(0)).group(1)
        lyon = (f'<section class="clair ss beige ac-lyon lv-lyon" id="tours">\n  <div class="wrap lv-lyon-tete">\n    <p class="lv-eyebrow">{t["e_lyon"]}</p>\n'
                f'    <h2>{t["lyon_h2"]}</h2>\n    <p class="lv-lyon-chapo">{t["lyon_chapo"]}</p>\n  </div>\n  <div class="wrap lv-lyon-cartes" id="guide">\n'
                f'    <a class="lv-lc lv-lc-grande" href="{pre}/jewish-lyon-tours/"><img src="/img/synagogue-tilsitt-galerie.jpg" alt="{alt1}" width="1000" height="1000" loading="lazy">'
                f'<span class="lv-lc-texte"><span class="lv-lc-eti">{t["c1_eti"]}</span><span class="lv-lc-titre">{t["c1_titre"]}</span><span class="lv-lc-info">{t["c1_info"]}</span><span class="lv-lc-lien">{t["c1_lien"]}</span></span></a>\n'
                f'    <a class="lv-lc" href="{pre}/tours/stopover/"><img src="/img/cartes/hub-rue-juiverie-lyon.webp" alt="{t["alt_stopover"]}" width="704" height="396" loading="lazy">'
                f'<span class="lv-lc-texte"><span class="lv-lc-eti">{t["c2_eti"]}</span><span class="lv-lc-titre">{t["c2_titre"]}</span></span></a>\n'
                f'    <a class="lv-lc" href="{pre}/jewish-lyon-guide/"><img src="/img/cartes/hub-shabbat-in-lyon.webp" alt="{t["alt_guide"]}" width="704" height="528" loading="lazy">'
                f'<span class="lv-lc-texte"><span class="lv-lc-eti">{t["c3_eti"]}</span><span class="lv-lc-titre">{t["c3_titre"]}</span></span></a>\n'
                f'  </div>\n  <p class="wrap lv-lyon-note">{t["lyon_note"]}</p>\n</section>')
        s = s[:m.start()] + lyon + s[m.end():]
    # 5. Contact : libellé au-dessus du bloc (formulaire de chaque langue gardé)
    if '<div class="ticket-zone" id="book">\n  <p class="lv-eyebrow">' not in s and 'id="book"><p class="lv-eyebrow">' not in s:
        s = re.sub(r'(<div class="ticket-zone" id="book">)', r'\1\n  <p class="lv-eyebrow">' + t["e_contact"] + "</p>", s, count=1)
    if s != s0:
        io.open(p, "w", encoding="utf-8", newline="").write(s)
    return "modifiée" if s != s0 else "déjà à jour"


if __name__ == "__main__":
    for lang in T:
        print(lang, accueil(lang))
