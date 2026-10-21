# -*- coding: utf-8 -*-
"""Message WhatsApp du panneau (bouton « panneau-wa » du menu) sur les pages de la zone Alpes (20/10).
Avant : toutes les pages Alpes, 4 langues, ouvraient WhatsApp avec « a private Jewish tour of Lyon »
(blocage n°5 de la stratégie SEA du 19/10). Après : un message Alpes dans la langue de la page.
Idempotent, ciblé : ne touche que l'attribut href du lien panneau-wa, en zone « alpes » (message Alpes)
et sur les pages van et villa (message générique « vos services »)."""
import io, os, re, glob
from urllib.parse import quote
os.chdir(os.path.dirname(os.path.abspath(__file__)))
from _zones import zone, LANGS

MSG = {
    "en": "Hello, we are going to the Alps. Resort: / Dates: / Number of people: / We need (chef, delivered meals, Shabbat, holiday, minyan):",
    "fr": "Bonjour, nous allons dans les Alpes. Station : / Dates : / Nombre de personnes : / Besoins (chef, repas livrés, Shabbat, fête, minyan) :",
    "es": "Buenos días, vamos a los Alpes. Estación: / Fechas: / Número de personas: / Necesitamos (chef, comidas entregadas, Shabat, fiesta, minyan):",
    "he": "שלום, נרצה שירותים כשרים באלפים. אתר: / תאריכים: / מספר משתתפים: / שירותים (צ'אלט עם שף, ארוחות במשלוח, שבת, חג, מניין):",
}
GEN = {  # pages van et villa (zone « general ») : message générique existant du site, par langue
    "en": "Hello, I would like to ask about your services. Dates: / Number of people:",
    "fr": "Bonjour, je voudrais des informations sur vos services. Dates : / Nombre de personnes :",
    "es": "Hola, quisiera información sobre sus servicios. Fechas: / Número de personas:",
    "he": "שלום, אשמח לקבל מידע על השירותים שלכם. תאריכים: / מספר אנשים:",
}
GENERIQUES = {"kosher-van-transfers", "kosher-villa-saint-tropez"}
NUM = "33652092301"
BH = "33781823193"
BH_HE = "%D7%A9%D7%9C%D7%95%D7%9D%2C%20%D7%90%D7%A0%D7%97%D7%A0%D7%95%20%D7%91%D7%90%D7%9C%D7%A4%D7%99%D7%9D%20%D7%95%D7%A0%D7%A9%D7%9E%D7%97%20%D7%9C%D7%A7%D7%91%D7%9C%20%D7%90%D7%A8%D7%95%D7%97%D7%95%D7%AA%20%D7%9B%D7%A9%D7%A8%D7%95%D7%AA%20%D7%91%D7%9E%D7%A9%D7%9C%D7%95%D7%97.%20%D7%90%D7%AA%D7%A8%3A%20%D7%90%D7%9C%D7%A4%20%D7%93%27%D7%95%D7%90%D7%96%20%2F%20%D7%AA%D7%90%D7%A8%D7%99%D7%9B%D7%99%D7%9D%3A%20%2F%20%D7%9E%D7%A1%D7%A4%D7%A8%20%D7%90%D7%A0%D7%A9%D7%99%D7%9D%3A"  # bouton repas du Beth Habad, message hébreu (QA 21/10, F1)
LYON = re.compile(r"tour of Lyon|visite juive privée de Lyon|visita judía privada (en|de) L|סיור יהודי פרטי בליון|עצירת הביניים|Stopover tour in Lyon")

def traiter(path):
    p = path.replace("\\", "/")
    lang = p.split("/")[0] if p.split("/")[0] in LANGS else "en"
    page = os.path.dirname(p[len(lang) + 1:] if lang != "en" else p)
    if zone(page) == "alpes":
        msg = MSG[lang]
    elif page in GENERIQUES:
        msg = GEN[lang]
    else:
        return 0
    h = io.open(path, encoding="utf-8").read()
    href = f"https://wa.me/{NUM}?text={quote(msg, safe='')}"
    n = re.sub(r'(<a class="panneau-wa" href=")[^"]*(")', lambda m: m.group(1) + href + m.group(2), h, count=1)
    # 20/10 soir : tout autre lien WhatsApp de la page (bouton du menu hébreu nav-cta-wa, bannière lead3-wa,
    # bouton noir, flottant) qui parle encore d'une visite de Lyon passe au même message.
    from urllib.parse import unquote
    n = re.sub(r'href="https://wa\.me/' + NUM + r'\?text=([^"]+)"',
               lambda m: f'href="{href}"' if LYON.search(unquote(m.group(1))) else m.group(0), n)
    # QA du 20/10 (C2) : sur une page hébraïque, un message WhatsApp sans aucune lettre hébraïque est un message
    # anglais oublié (stations Annecy, Cervinia, Chamonix… ) : il passe au message Alpes en hébreu.
    if lang == "he":
        n = re.sub(r'(href="https://wa\.me/' + BH + r'\?text=)([^"]+)"',
                   lambda m: m.group(0) if re.search(r"[֐-׿]", unquote(m.group(2))) else m.group(1) + BH_HE + '"', n)
        # QA du 20/10 (C2) : gabarits JavaScript des formulaires courts restés en anglais sur les pages hébraïques
        n = n.replace("`Hello, I would like to check availability for the ${f.tour.value} tour. Dates: ${f.dates.value||'/'} / Number of people: ${f.personnes.value||'/'} / Preferred language:`",
                      "`שלום, אשמח לבדוק זמינות לסיור ${f.tour.value}. תאריכים: ${f.dates.value||'/'} / מספר משתתפים: ${f.personnes.value||'/'} / שפה מועדפת:`")
        n = n.replace("'Hello, we are planning: '", "'שלום, אנחנו מתכננים: '")
        n = re.sub(r'href="https://wa\.me/' + NUM + r'\?text=([^"]+)"',
                   lambda m: m.group(0) if re.search(r"[֐-׿]", unquote(m.group(1))) else f'href="{href}"', n)
    if n != h:
        io.open(path, "w", encoding="utf-8", newline="\n").write(n)
        return 1
    return 0

if __name__ == "__main__":
    pages = [p for p in glob.glob("**/index.html", recursive=True) if not p.replace("\\", "/").startswith(("_", "preview"))]
    print(sum(traiter(p) for p in pages), "pages modifiees sur", len(pages))
