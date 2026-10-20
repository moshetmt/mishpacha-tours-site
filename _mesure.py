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
PRIV = {   # 20/10 (C3) : texte complet, aligné sur js/mesure.js (cookie_expires 395 j, _gcl_au 90 j, choix 6 mois en localStorage, remarketing coupé)
 "en": ("Cookies and <i>measurement</i>", "Cookies only with your consent. Before you press Accept, the site loads no third-party script and sets no cookie. After Accept, two Google services load: Google Analytics 4 (audience statistics: page views, steps of the request form, clicks on the WhatsApp and email links) and Google Ads (conversion measurement: which ad led to a request). They set the cookies _ga and _ga_* (Analytics, 13 months) and _gcl_au (Google Ads, 90 days). We do not use them for remarketing or to personalise ads. For enhanced conversions, when you send a request, your email address and your phone number are passed to Google in hashed form (SHA-256, one-way) so that Google can match your request with the ad you clicked; we never pass your name. Google may process this data outside the European Union, under the safeguards described in its own policies. Your choice is kept for six months in your browser (not as a cookie). To withdraw it, click \"Cookies\" at the bottom of any page and choose Refuse: the Google cookies are deleted and nothing is measured any more."),
 "fr": ("Cookies et <i>mesure</i>", "Cookies seulement avec votre accord. Avant que vous appuyiez sur « Accepter », le site ne charge aucun script tiers et ne dépose aucun cookie. Après « Accepter », deux services Google se chargent : Google Analytics 4 (statistiques d'audience : pages vues, étapes du formulaire de demande, clics sur les liens WhatsApp et e-mail) et Google Ads (mesure des conversions : quelle annonce mène à une demande). Ils déposent les cookies _ga et _ga_* (Analytics, 13 mois) et _gcl_au (Google Ads, 90 jours). Nous ne les utilisons ni pour le reciblage publicitaire ni pour personnaliser des annonces. Pour les conversions améliorées, quand vous envoyez une demande, votre adresse e-mail et votre numéro de téléphone sont transmis à Google sous forme hachée (SHA-256, à sens unique) afin que Google rapproche votre demande de l'annonce sur laquelle vous avez cliqué ; nous ne transmettons jamais votre nom. Google peut traiter ces données hors de l'Union européenne, selon les garanties décrites dans ses propres politiques. Votre choix est conservé six mois dans votre navigateur (hors cookie). Pour le retirer, cliquez sur « Cookies » en bas de n'importe quelle page et choisissez « Refuser » : les cookies Google sont supprimés et plus rien n'est mesuré."),
 "es": ("Cookies y <i>medición</i>", "Cookies solo con su consentimiento. Antes de que pulse «Aceptar», el sitio no carga ningún script de terceros ni instala ninguna cookie. Tras «Aceptar» se cargan dos servicios de Google: Google Analytics 4 (estadísticas de audiencia: páginas vistas, pasos del formulario de solicitud, clics en los enlaces de WhatsApp y de correo) y Google Ads (medición de conversiones: qué anuncio lleva a una solicitud). Instalan las cookies _ga y _ga_* (Analytics, 13 meses) y _gcl_au (Google Ads, 90 días). No las usamos ni para remarketing ni para personalizar anuncios. Para las conversiones mejoradas, cuando envía una solicitud, su correo electrónico y su número de teléfono se transmiten a Google en forma codificada (hash SHA-256, irreversible) para que Google relacione su solicitud con el anuncio en el que hizo clic; nunca transmitimos su nombre. Google puede tratar estos datos fuera de la Unión Europea, con las garantías descritas en sus propias políticas. Su elección se conserva seis meses en su navegador (fuera de una cookie). Para retirarla, pulse «Cookies» al final de cualquier página y elija «Rechazar»: se eliminan las cookies de Google y ya no se mide nada."),
 "he": ("עוגיות <i>ומדידה</i>", "עוגיות רק בהסכמתכם. לפני שלוחצים על ״לאשר״, האתר אינו טוען סקריפט של צד שלישי ואינו שומר עוגיות. אחרי ״לאשר״ נטענים שני שירותים של Google: Google Analytics 4 (סטטיסטיקות קהל: צפיות בעמודים, שלבי טופס הבקשה, לחיצות על קישורי וואטסאפ ודוא״ל) ו-Google Ads (מדידת המרות: איזו מודעה הובילה לבקשה). הם שומרים את העוגיות _ga ו-_ga_* (Analytics, 13 חודשים) ו-_gcl_au (Google Ads, 90 יום). איננו משתמשים בהן למיקוד מחדש (רימרקטינג) ולא להתאמה אישית של מודעות. לצורך המרות משופרות, כששולחים בקשה, כתובת הדוא״ל ומספר הטלפון שלכם מועברים ל-Google בצורה מגובבת (hash, SHA-256, חד-כיווני) כדי ש-Google תקשר בין הבקשה למודעה שעליה לחצתם; איננו מעבירים לעולם את השם שלכם. Google עשויה לעבד את הנתונים מחוץ לאיחוד האירופי, בכפוף להגנות המתוארות במדיניותה. הבחירה שלכם נשמרת שישה חודשים בדפדפן (לא כעוגיה). כדי לבטל אותה, לחצו על ״עוגיות״ בתחתית כל עמוד ובחרו ״לסרב״: עוגיות Google נמחקות ושום דבר לא נמדד עוד."),
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
