# -*- coding: utf-8 -*-
"""Lot 4, n° 18 : page Pessah /kosher-pesach-french-alps/ en 4 langues. Idempotent (marqueurs LOT4-PESSAH). Depuis site-v5/.
 - bannière : photo réelle de table dressée du chalet de Val Thorens (img/chalet/valthorens-table.jpg, aucune hallah) à la
   place de wp-soleil (neige au soleil, sans rapport avec la fête) ;
 - section « Votre minhag, votre table » : séfarade ou ashkénaze, kitniyot, gebrokts, matsa : rien d'affirmé sur ce que
   l'équipe sait faire, le client dit son minhag et reçoit une confirmation écrite (questions à Mendel dans le rapport) ;
 - section « Skier à Pessah 2027 » : texte du rapport 06-reports/2026-11-06-stations-ouvertes-pessah-2027.md (stations dont
   la fermeture 2026-27 est publiée, sous réserve de neige) ;
 - 2 questions de FAQ (minhag, ski) ; JSON-LD FAQ complété par _build_i18n.py ld (lancé après)."""
import io, os, re
from PIL import Image
os.chdir(os.path.dirname(os.path.abspath(__file__)))
PAGE = "kosher-pesach-french-alps"
A, Z = "<!--LOT4-PESSAH-->", "<!--/LOT4-PESSAH-->"
FA, FZ = "<!--LOT4-PESSAH-FAQ-->", "<!--/LOT4-PESSAH-FAQ-->"

T = {
 "": dict(
  minhag_h=("Your minhag, ", "your table"),
  minhag_p="Sephardi or Ashkenazi, tell us with your dates. Our team confirms in writing what it prepares for your group.",
  minhag=[("Kitniyot or not.", "Tell us whether your family eats kitniyot at Pesach: the menus follow your custom."),
          ("Gebrokts or not.", "Matza cooked in liquid or kept dry during the holiday: say which custom you keep."),
          ("Matza for the seder.", "Hand-made shmura matza or machine matza: tell us what you need and we tell you what we can provide.")],
  ski_h=("Skiing at ", "Pesach 2027"),
  ski_p=["Pesach 2027 begins on the evening of Wednesday 21 April. Several high-altitude resorts have announced ski seasons that run past that date: Val Thorens, Val d'Isère and Les Deux Alpes until 2 May, Alpe d'Huez until 25 April, and La Plagne and Les Arcs until 24 April. Closing dates belong to each resort and depend on snow, so we confirm them with the resort before you book.",
         "Lower resorts such as Courchevel, Les Menuires and Avoriaz close on 18 April, before the seder, so we do not suggest them for skiing that week. Tell us your dates and your group, and we will suggest a chalet in a resort where the lifts should still be running."],
  faq=[("Sephardi or Ashkenazi?", "Both. Tell us your minhag with your dates: kitniyot or not, gebrokts or not, the matza you want for the seder. Our team confirms in writing what it prepares."),
       ("Can we ski during Pesach 2027?", "In the high resorts, yes: Val Thorens, Val d'Isère and Les Deux Alpes have announced a season until 2 May, Alpe d'Huez until 25 April, La Plagne and Les Arcs until 24 April, subject to snow. Courchevel, Les Menuires and Avoriaz close on 18 April.")]),
 "fr": dict(
  minhag_h=("Votre minhag, ", "votre table"),
  minhag_p="Séfarade ou ashkénaze, dites-le-nous avec vos dates. Notre équipe vous confirme par écrit ce qu'elle prépare pour votre groupe.",
  minhag=[("Kitniyot ou non.", "Dites-nous si votre famille mange des kitniyot à Pessah : les menus suivent votre minhag."),
          ("Gebrokts ou non.", "Matsa trempée ou gardée sèche pendant la fête : dites-nous l'usage que vous suivez."),
          ("La matsa du séder.", "Matsa chmoura faite à la main ou matsa machine : dites-nous ce qu'il vous faut, nous vous disons ce que nous pouvons fournir.")],
  ski_h=("Skier à ", "Pessah 2027"),
  ski_p=["Pessah 2027 commence le mercredi 21 avril au soir. Plusieurs stations d'altitude ont annoncé une saison de ski qui dépasse cette date : Val Thorens, Val d'Isère et Les Deux Alpes jusqu'au 2 mai, l'Alpe d'Huez jusqu'au 25 avril, La Plagne et Les Arcs jusqu'au 24 avril. Chaque station fixe sa date de fermeture selon l'enneigement ; nous la confirmons avec la station avant votre réservation.",
         "Les stations plus basses comme Courchevel, Les Menuires et Avoriaz ferment le 18 avril, avant le séder : nous ne les proposons pas pour skier cette semaine-là. Indiquez-nous vos dates et votre groupe, et nous vous proposerons un chalet dans une station dont les remontées devraient encore fonctionner."],
  faq=[("Séfarade ou ashkénaze ?", "Les deux. Dites-nous votre minhag avec vos dates : kitniyot ou non, gebrokts ou non, la matsa que vous voulez pour le séder. Notre équipe vous confirme par écrit ce qu'elle prépare."),
       ("Peut-on skier pendant Pessah 2027 ?", "Dans les stations d'altitude, oui : Val Thorens, Val d'Isère et Les Deux Alpes ont annoncé une saison jusqu'au 2 mai, l'Alpe d'Huez jusqu'au 25 avril, La Plagne et Les Arcs jusqu'au 24 avril, sous réserve de neige. Courchevel, Les Menuires et Avoriaz ferment le 18 avril.")]),
 "es": dict(
  minhag_h=("Su minhag, ", "su mesa"),
  minhag_p="Sefardí o askenazí, díganoslo con sus fechas. Nuestro equipo le confirma por escrito lo que prepara para su grupo.",
  minhag=[("Kitniyot o no.", "Díganos si su familia come kitniyot en Pésaj: los menús siguen su costumbre."),
          ("Gebrokts o no.", "Matzá remojada o guardada seca durante la fiesta: díganos la costumbre que siguen."),
          ("La matzá del séder.", "Matzá shmurá hecha a mano o matzá de máquina: díganos lo que necesitan y le decimos lo que podemos proporcionar.")],
  ski_h=("Esquiar en ", "Pésaj 2027"),
  ski_p=["Pésaj 2027 empieza el miércoles 21 de abril por la noche. Varias estaciones de altura han anunciado una temporada de esquí que supera esa fecha: Val Thorens, Val d'Isère y Les Deux Alpes hasta el 2 de mayo, Alpe d'Huez hasta el 25 de abril, La Plagne y Les Arcs hasta el 24 de abril. Cada estación fija su fecha de cierre según la nieve; la confirmamos con la estación antes de su reserva.",
         "Las estaciones más bajas, como Courchevel, Les Menuires y Avoriaz, cierran el 18 de abril, antes del séder: no las proponemos para esquiar esa semana. Indíquenos sus fechas y su grupo, y le propondremos un chalet en una estación cuyos remontes deberían seguir funcionando."],
  faq=[("¿Sefardí o askenazí?", "Ambos. Díganos su minhag con sus fechas: kitniyot o no, gebrokts o no, la matzá que quieren para el séder. Nuestro equipo le confirma por escrito lo que prepara."),
       ("¿Se puede esquiar durante Pésaj 2027?", "En las estaciones de altura, sí: Val Thorens, Val d'Isère y Les Deux Alpes han anunciado una temporada hasta el 2 de mayo, Alpe d'Huez hasta el 25 de abril, La Plagne y Les Arcs hasta el 24 de abril, según la nieve. Courchevel, Les Menuires y Avoriaz cierran el 18 de abril.")]),
 "he": dict(
  minhag_h=("המנהג שלכם, ", "השולחן שלכם"),
  minhag_p="ספרדים או אשכנזים, כתבו לנו יחד עם התאריכים. הצוות שלנו מאשר בכתב מה הוא מכין לקבוצה שלכם.",
  minhag=[("קטניות או לא.", "כתבו לנו אם המשפחה אוכלת קטניות בפסח: התפריטים הולכים לפי המנהג שלכם."),
          ("שרויה או לא.", "מצה שרויה או יבשה במהלך החג: כתבו לנו איזה מנהג אתם נוהגים."),
          ("המצות לסדר.", "מצה שמורה בעבודת יד או מצת מכונה: כתבו לנו מה אתם צריכים ואנחנו אומרים מה אפשר לספק.")],
  ski_h=("סקי ב", "פסח 2027"),
  ski_p=["פסח 2027 מתחיל ביום רביעי, 21 באפריל, בערב. כמה אתרי סקי גבוהים הודיעו על עונת סקי שנמשכת אחרי התאריך הזה: ואל טורנס, ואל דיזר ולה דז אלפ עד 2 במאי, אלפ ד'ואז עד 25 באפריל, לה פלאן ולז ארק עד 24 באפריל. כל אתר קובע את תאריך הסגירה לפי השלג; אנחנו מאשרים אותו מול האתר לפני ההזמנה שלכם.",
         "אתרים נמוכים יותר כמו קורשבל, לה מנואר ואבוריאז נסגרים ב-18 באפריל, לפני הסדר: לא נציע אותם לסקי באותו שבוע. כתבו לנו את התאריכים ואת הקבוצה, ונציע צ'אלה באתר שבו המעליות אמורות עדיין לפעול."],
  faq=[("ספרדים או אשכנזים?", "שניהם. כתבו לנו את המנהג שלכם יחד עם התאריכים: קטניות או לא, שרויה או לא, איזו מצה אתם רוצים לסדר. הצוות שלנו מאשר בכתב מה הוא מכין."),
       ("אפשר לעשות סקי בפסח 2027?", "באתרים הגבוהים כן: ואל טורנס, ואל דיזר ולה דז אלפ הודיעו על עונה עד 2 במאי, אלפ ד'ואז עד 25 באפריל, לה פלאן ולז ארק עד 24 באפריל, בכפוף לשלג. קורשבל, לה מנואר ואבוריאז נסגרים ב-18 באפריל.")]),
}
LTR = lambda l, s: s if l != "he" else re.sub(r"([A-Za-z][A-Za-z' .\-]*[A-Za-z]|\d[\d .:\-]*\d|\d)", r'<span dir="ltr">\1</span>', s)

def rd(p): return io.open(p, encoding="utf-8", newline="").read()
def wr(p, s): io.open(p, "w", encoding="utf-8", newline="").write(s)

# 1. image de bannière (réelle), 3 largeurs
src = Image.open("img/chalet/valthorens-table.jpg").convert("RGB")
for w in (640, 960, 1264):
    out = f"img/h/pessah-table-{w}.webp"
    if not os.path.exists(out):
        im = src.resize((w, round(src.height * w / src.width)), Image.LANCZOS); im.save(out, "WEBP", quality=82)
print("bannière :", src.size)
HERO_OLD = re.compile(r'<img src="/img/h/wp-soleil-960\.webp"[^>]*>')
HERO_NEW = '<img src="/img/h/pessah-table-960.webp" srcset="/img/h/pessah-table-640.webp 640w, /img/h/pessah-table-960.webp 960w, /img/h/pessah-table-1264.webp 1264w" sizes="100vw" alt="" width="1264" height="848" fetchpriority="high">'

n = 0
for l, pre in (("", ""), ("fr", "fr/"), ("es", "es/"), ("he", "he/")):
    p = f"{pre}{PAGE}/index.html"; s = rd(p); t = T[l]
    s = HERO_OLD.sub(HERO_NEW, s)
    s = s.replace('<img src="/img/h/pessah-table-960.webp" srcset="/img/h/pessah-table-640.webp 640w, /img/h/pessah-table-960.webp 960w, /img/h/pessah-table-1600.webp 1600w"', '<img src="/img/h/pessah-table-960.webp" srcset="/img/h/pessah-table-640.webp 640w, /img/h/pessah-table-960.webp 960w, /img/h/pessah-table-1264.webp 1264w"')
    s = re.sub(re.escape(A) + ".*?" + re.escape(Z), "", s, flags=re.S)
    s = re.sub(re.escape(FA) + ".*?" + re.escape(FZ), "", s, flags=re.S)
    li = "".join(f'<li class="dk-sans-ico"><b>{b}</b> {LTR(l, x)}</li>' for b, x in t["minhag"])
    bloc = (f'{A}<section class="clair ss wrap conseils"><h2>{t["minhag_h"][0]}<i>{t["minhag_h"][1]}</i></h2><p>{t["minhag_p"]}</p>'
            f'<ul class="dk-cartes">{li}</ul></section>'
            f'<section class="clair clair-2 ss wrap conseils"><h2>{t["ski_h"][0]}<i>{LTR(l, t["ski_h"][1])}</i></h2>'
            + "".join(f"<p>{LTR(l, x)}</p>" for x in t["ski_p"]) + f'</section>{Z}')
    s, k = re.subn(r'(</ul></div></div>)(<section class="ss wrap etapes">)', lambda m: m.group(1) + bloc + m.group(2), s, count=1)
    assert k == 1, p
    faq = FA + "".join(f'<details><summary>{q}</summary><p>{LTR(l, a)}</p></details>' for q, a in t["faq"]) + FZ
    s, k = re.subn(r'(</details>)(</section><section class="ss lead-final")', lambda m: m.group(1) + faq + m.group(2), s, count=1)
    assert k == 1, p
    wr(p, s); n += 1
print("pages Pessah :", n)
