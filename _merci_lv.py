# -*- coding: utf-8 -*-
"""Pages /merci/ (4 langues) en charte LV (Moshé 03/11) : Jost, blanc, bouton noir 4 px, petit bonhomme, message clair.
   Remplace seulement le <main> ; garde l'adresse, le lien WhatsApp prérempli de chaque page et js/mesure.js (generate_lead et conversion Ads
   envoyés sur /merci/ depuis le drapeau posé par le formulaire). Puis python _charte_lv.py sur les 4 pages. Idempotent.
   python _merci_lv.py (depuis site-v5/)"""
import io, os, re

os.chdir(os.path.dirname(os.path.abspath(__file__)))
T = {
    "": ("Home", "Thank you", "Thank you, we have your request", "We answer you on WhatsApp the same day, never during Shabbat.", "Message us on WhatsApp", "Back to the home page", "../", "../img/"),
    "fr": ("Accueil", "Merci", "Merci, nous avons bien reçu votre demande", "Nous vous répondons sur WhatsApp le jour même, jamais pendant Chabbat.", "Écrivez-nous sur WhatsApp", "Retour à l'accueil", "/fr/", "/img/"),
    "es": ("Inicio", "Gracias", "Gracias, hemos recibido su solicitud", "Le respondemos por WhatsApp el mismo día, nunca durante Shabat.", "Escríbanos por WhatsApp", "Volver al inicio", "/es/", "/img/"),
    "he": ("ראשי", "תודה", "תודה, קיבלנו את הבקשה שלכם", "נחזור אליכם בוואטסאפ באותו היום, אף פעם לא בשבת.", "כתבו לנו בוואטסאפ", "חזרה לדף הבית", "/he/", "/img/"),
}
for lang, (home, fil, h1, txt, wa_t, back, home_url, img) in T.items():
    p = (lang + "/" if lang else "") + "merci/index.html"
    s = io.open(p, encoding="utf-8").read()
    m = re.search(r"<main>.*?</main>", s, re.S)
    wa = re.search(r'href="(https://wa\.me[^"]+)"', m.group(0)).group(1)
    main = ('<main>\n<section class="pf-merci"><div class="pf-merci-c">\n'
            f'  <img class="pf-merci-hp hassid-merci" src="{img}picto-hassid.svg" alt="" width="40" height="56">\n'
            f'  <p class="fil"><a href="{home_url}">{home}</a> / {fil}</p>\n'
            f'  <h1>{h1}</h1>\n  <p class="pf-merci-t">{txt}</p>\n'
            f'  <p><a class="btn-noir pf-merci-b" href="{wa}" rel="noopener"><svg aria-hidden="true"><use href="#wa"/></svg>{wa_t}</a></p>\n'
            f'  <p class="pf-merci-r"><a href="{home_url}">{back}</a></p>\n'
            '</div></section>\n</main>')
    n = s[:m.start()] + main + s[m.end():]
    n = n.replace('<link rel="stylesheet" href="/valora-form.css">', "")
    if n != s:
        io.open(p, "w", encoding="utf-8", newline="\n").write(n)
    print("ok", p)
