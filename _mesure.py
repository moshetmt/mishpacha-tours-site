# -*- coding: utf-8 -*-
"""Mesure GA4 + conversions Ads + consentement (15/10, Ads 19/10). Idempotent. A lancer depuis site-v5/ apres _decor.py, avant _animations.py.
  (a) <head> de chaque page : Consent Mode v2 tout refuse + <script src="/js/mesure.js" defer> (js/mesure.js ecrit a la main),
  (b) lien « Cookies » dans la ligne legale du pied,
  (c) section « Cookies and measurement » dans les 4 pages privacy,
  (d) bloc CSS ===MESURE=== dans styles.css.
gtag.js n'est charge par mesure.js qu'apres un « Accept » (aucun hit /collect avant). `--strip` retire (a) (b) (c) (d)."""
import io, os, re, sys, glob
ICI = os.path.dirname(os.path.abspath(__file__)); os.chdir(ICI)
MARQ = "<!--mesure-->"
HEAD = (MARQ + "<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments)}"
        "gtag('consent','default',{ad_storage:'denied',analytics_storage:'denied',ad_user_data:'denied',ad_personalization:'denied',wait_for_update:500});"
        "gtag('js',new Date());</script><script src=\"/js/mesure.js\" defer></script><!--/mesure-->")
COOKIES = {"en": "Cookies", "fr": "Cookies", "es": "Cookies", "he": "עוגיות"}
PRIV = {
 "en": ("Cookies and <i>measurement</i>", "With your consent only, we use Google Analytics and Google Ads to count visits and to see which pages and which ads lead to a request. They set cookies that last up to 13 months. We measure page views, the steps of the request form, the sending of a request, and clicks on WhatsApp and email links. When you send a request, your phone number and your email address, if you give one, are passed to Google in a scrambled form (a one-way hash) so that Google can match your request with the ad you clicked. We never pass your name. Your choice is kept for six months. Use the \"Cookies\" link at the bottom of any page to change it or withdraw it at any time. If you refuse, no measurement cookie is set and nothing is measured."),
 "fr": ("Cookies et <i>mesure</i>", "Avec votre seul consentement, nous utilisons Google Analytics et Google Ads pour compter les visites et voir quelles pages et quelles annonces mènent à une demande. Ils déposent des cookies d'une durée maximale de 13 mois. Nous mesurons les pages vues, les étapes du formulaire de demande, l'envoi d'une demande et les clics sur les liens WhatsApp et e-mail. Quand vous envoyez une demande, votre numéro de téléphone et votre adresse e-mail, si vous en donnez une, sont transmis à Google sous une forme brouillée (une empreinte à sens unique) pour que Google rapproche votre demande de l'annonce sur laquelle vous avez cliqué. Nous ne transmettons jamais votre nom. Votre choix est conservé six mois. Le lien « Cookies » en bas de chaque page permet de le modifier ou de le retirer à tout moment. Si vous refusez, aucun cookie de mesure n'est déposé et rien n'est mesuré."),
 "es": ("Cookies y <i>medición</i>", "Solo con su consentimiento, usamos Google Analytics y Google Ads para contar las visitas y ver qué páginas y qué anuncios llevan a una solicitud. Instalan cookies de hasta 13 meses de duración. Medimos las páginas vistas, los pasos del formulario de solicitud, el envío de una solicitud y los clics en los enlaces de WhatsApp y de correo electrónico. Cuando envía una solicitud, su número de teléfono y su correo electrónico, si indica uno, se transmiten a Google de forma codificada (una huella irreversible) para que Google relacione su solicitud con el anuncio en el que hizo clic. Nunca transmitimos su nombre. Su elección se conserva seis meses. El enlace «Cookies» al final de cada página permite cambiarla o retirarla en cualquier momento. Si rechaza, no se instala ninguna cookie de medición y no se mide nada."),
 "he": ("עוגיות <i>ומדידה</i>", "רק בהסכמתכם, אנו משתמשים ב-Google Analytics וב-Google Ads כדי לספור ביקורים ולראות אילו עמודים ואילו מודעות מובילים לבקשה. הם שומרים עוגיות לתקופה של עד 13 חודשים. אנו מודדים צפיות בעמודים, שלבים בטופס הבקשה, שליחת בקשה ולחיצות על קישורי וואטסאפ ודוא״ל. כששולחים בקשה, מספר הטלפון וכתובת הדוא״ל שלכם, אם מסרתם כתובת, מועברים ל-Google בצורה מוצפנת (טביעת אצבע חד-כיוונית) כדי ש-Google תקשר בין הבקשה למודעה שעליה לחצתם. איננו מעבירים לעולם את השם שלכם. הבחירה שלכם נשמרת לשישה חודשים. הקישור ״עוגיות״ בתחתית כל עמוד מאפשר לשנות אותה או לבטל אותה בכל עת. אם תסרבו, לא תישמר עוגיית מדידה ושום דבר לא יימדד."),
}
CSS_D, CSS_F = "/* ===MESURE=== */", "/* ===/MESURE=== */"
CSS = """
.cb{position:fixed;left:12px;right:12px;bottom:12px;z-index:70;max-width:760px;margin-inline:auto;display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:12px 20px;padding:14px 18px;background:var(--creme);color:var(--encre);border:1px solid rgba(28,27,31,.18);border-radius:18px;box-shadow:0 8px 28px rgba(28,27,31,.16);font-size:14px;line-height:1.5}
.cb[hidden]{display:none}
.cb-haut{bottom:auto;top:12px}
.cb p{margin:0;flex:1 1 280px}
.cb p a{text-decoration:underline;text-underline-offset:3px;white-space:nowrap}
.cb-b{display:flex;gap:10px}
.cb button{min-width:104px;min-height:44px;padding:0 22px;border:0;border-radius:999px;background:var(--encre);color:var(--creme);font:inherit;font-size:14px;font-weight:600;cursor:pointer}
@media(max-width:480px){.cb-b{width:100%}.cb button{flex:1}}
"""
def css(strip):
    p = "styles.css"; s = io.open(p, encoding="utf-8", newline="").read()
    o = s; bloc = CSS_D + CSS + CSS_F + "\n"; motif = re.escape(CSS_D) + r".*?" + re.escape(CSS_F) + r"\n?"
    if strip: s = re.sub(motif, "", s, flags=re.S)
    elif CSS_D in s: s = re.sub(motif, lambda m: bloc, s, flags=re.S)  # remplace en place, ne deplace pas le bloc
    else: s = s.rstrip("\n") + "\n" + bloc
    if s != o: io.open(p, "w", encoding="utf-8", newline="\n").write(s)
def page(path, strip):
    s = io.open(path, encoding="utf-8", newline="").read(); o = s
    lang = path.replace("\\", "/").split("/")[0]; lang = lang if lang in ("fr", "es", "he") else "en"
    s = re.sub(re.escape(MARQ) + r".*?<!--/mesure-->\n?", "", s, flags=re.S)
    s = s.replace("\n" + "<!--mesure-->", "")
    s = re.sub(r'<a href="#cookies" data-cookies>[^<]*</a>', "", s)
    s = re.sub(r'<section class="ss wrap conseils[^"]*" id="cookies-mesure">.*?</section>', "", s, flags=re.S)
    if not strip:
        s = re.sub(r'(<meta name="viewport"[^>]*>)', lambda m: m.group(1) + "\n" + HEAD, s, count=1)
        s = re.sub(r'(<p class="legal">)(.*?)(<a href="[^"]*privacy/">)', lambda m: m.group(1) + m.group(2) + '<a href="#cookies" data-cookies>' + COOKIES[lang] + "</a>" + m.group(3), s, count=1, flags=re.S)
        if path.replace("\\", "/").endswith("privacy/index.html"):
            h, t = PRIV[lang]
            sec = f'<section class="ss wrap conseils" id="cookies-mesure"><h2>{h}</h2><p>{t}</p></section>'
            i = s.rfind("<section", 0, s.find("</main>"))
            s = s[:i] + sec + s[i:]
    if s != o: io.open(path, "w", encoding="utf-8", newline="\n").write(s); return 1
    return 0
if __name__ == "__main__":
    strip = "--strip" in sys.argv
    pages = [p for p in glob.glob("**/index.html", recursive=True) if not p.replace("\\", "/").startswith("_")]
    print(sum(page(p, strip) for p in pages), "pages modifiees sur", len(pages)); css(strip)
