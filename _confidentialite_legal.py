# -*- coding: utf-8 -*-
"""20/10 (C3 + C5) : page /privacy/ mise à jour et page /legal/ créée, 4 langues (EN, fr, es, he). Script ciblé, idempotent.
   EN = _pages/privacy.py et _pages/legal.py (source). fr/es/he = textes ci-dessous. Les sorties sont dérivées de la page privacy de la langue
   (en-tête, pied, sélecteur de langue, décor déjà posés), on n'y relance donc pas _decor.py.
   Ordre : python _ajout_legal_pied.py ; python _confidentialite_legal.py (appelle _mesure pour la section Cookies et mesure) ; python _build_sitemap.py
   Marqueur {{SIREN}} : à remplacer ici (SIREN) et dans _pages/legal.py, puis relancer ce script."""
import re, os, io, json, html, importlib.util
ICI = os.path.dirname(os.path.abspath(__file__)); os.chdir(ICI)
SIREN = "{{SIREN}}"
def charge(n):
    sp = importlib.util.spec_from_file_location(n, f"_pages/{n}.py"); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m.PAGE
EN_P, EN_L = charge("privacy"), charge("legal")
MAIL = '<a href="mailto:contact@mishpachatours.com">contact@mishpachatours.com</a>'

# ------------------------------------------------------------------ textes fr / es / he (même format que les modules)
FR_P = dict(
  desc="Ce que Mishpacha Tours collecte via le formulaire de demande, pourquoi, qui le reçoit, combien de temps, vos droits RGPD. Cookies seulement avec votre accord.",
  chips=["RGPD", "Cookies seulement avec votre accord", "Données conservées 3 ans"],
  sections=[
    dict(h2="Qui est <i>responsable</i>", ico="message-circle", html=f"""<p>Mishpacha Tours, entreprise individuelle exploitée par la guide, à Lyon, France. Contact : {MAIL}, ou le formulaire de demande. Les informations sur l'entreprise figurent dans les <a href="/fr/legal/">mentions légales</a>.</p>"""),
    dict(h2="Ce que nous <i>collectons</i>", icos=["calendar-days", "lock", "message-circle", "calendar-x"], html="""<ul>
<li><b>Lorsque vous envoyez le formulaire de demande :</b> le séjour ou la visite souhaité, vos dates, le nombre de personnes, la langue, votre nom, votre numéro de téléphone ou WhatsApp, et votre adresse e-mail si vous en donnez une. Le formulaire demande aussi des informations qui nous servent à préparer votre devis : besoins alimentaires et allergies, âges des enfants, niveau de pratique religieuse (minyan et cacherout) et budget. Le formulaire écrit une ligne dans une feuille Google privée et nous envoie un e-mail.</li>
<li><b>Base légale :</b> mesures précontractuelles pour les informations de réservation. Pour les allergies et besoins alimentaires (données de santé) et pour la pratique religieuse, nous nous appuyons sur votre consentement explicite (article 9, paragraphe 2, point a, du RGPD), donné en cochant la case sous le bouton d'envoi du formulaire. Sans ce consentement, le formulaire ne peut pas être envoyé.</li>
<li><b>Lorsque vous écrivez sur WhatsApp ou par e-mail :</b> vos messages et votre numéro ou adresse, conservés dans ces services selon leurs propres conditions.</li>
<li><b>Lorsque vous visitez le site :</b> avant que vous appuyiez sur « Accepter », rien de notre part : aucun cookie et aucun script tiers. Après « Accepter », Google Analytics et Google Ads se chargent, comme décrit dans la section Cookies et mesure ci-dessous. Notre hébergeur (Vercel) conserve des journaux de serveur standard pour la sécurité. Les pages avec carte chargent des tuiles depuis OpenStreetMap et les horaires de Shabbat depuis Hebcal : ces services voient votre adresse IP au chargement de la page.</li>
</ul>"""),
    dict(h2="Qui <i>les reçoit</i>", ico="users", html="""<p>Pour un séjour dans les Alpes, nous transmettons votre demande au prestataire des Alpes qui établit le devis (chalet, chef, minyan, transferts). Ce prestataire reçoit vos réponses, y compris l'alimentation et la pratique religieuse, et ne les utilise que pour établir votre devis. En dehors de lui, seuls les services qui stockent les données pour notre compte les voient (Google, WhatsApp, Vercel). Nous ne vendons ni ne partageons jamais vos coordonnées, et nous n'envoyons jamais de lettre d'information.</p>"""),
    dict(h2="Combien de temps <i>nous les conservons</i>", ico="clock", html="""<p>Les demandes et la correspondance, y compris les réponses sur l'alimentation et la pratique religieuse, sont conservées trois ans après notre dernier échange, puis supprimées.</p>"""),
    dict(h2="Vos <i>droits</i>", ico="message-circle", html=f"""<p>Vous pouvez demander ce que nous détenons à votre sujet, le faire rectifier ou supprimer, ou vous opposer à son utilisation. Vous pouvez retirer votre consentement à tout moment en écrivant à {MAIL} ; nous supprimons alors les réponses sur la santé et la pratique religieuse, sans effet sur ce qui a été fait avant. Nous répondons sous un mois. Vous pouvez aussi déposer une plainte auprès de la CNIL, l'autorité française de protection des données, sur cnil.fr.</p>"""),
  ])
ES_P = dict(
  desc="Qué recoge Mishpacha Tours con el formulario de solicitud, por qué, quién lo recibe, cuánto tiempo y sus derechos según el RGPD. Cookies solo con su consentimiento.",
  chips=["RGPD", "Cookies solo con su consentimiento", "Datos conservados 3 años"],
  sections=[
    dict(h2="Quién es el <i>responsable</i>", ico="message-circle", html=f"""<p>Mishpacha Tours, empresa individual explotada por la guía, en Lyon, Francia. Contacto: {MAIL}, o el formulario de solicitud. Los datos de la empresa figuran en el <a href="/es/legal/">aviso legal</a>.</p>"""),
    dict(h2="Qué <i>recogemos</i>", icos=["calendar-days", "lock", "message-circle", "calendar-x"], html="""<ul>
<li><b>Cuando envía el formulario de solicitud:</b> el viaje o la visita que desea, sus fechas, el número de personas, el idioma, su nombre, su número de teléfono o de WhatsApp y su correo electrónico si indica uno. El formulario también pide datos que nos sirven para preparar su presupuesto: necesidades alimentarias y alergias, edades de los niños, nivel de práctica religiosa (minyan y cashrut) y presupuesto. El formulario escribe una línea en una hoja de Google privada y nos envía un correo.</li>
<li><b>Base jurídica:</b> medidas previas a un contrato para los datos de la reserva. Para las alergias y necesidades alimentarias (datos de salud) y para la práctica religiosa, nos basamos en su consentimiento explícito (artículo 9, apartado 2, letra a, del RGPD), que usted da al marcar la casilla situada bajo el botón de envío del formulario. Sin ese consentimiento, el formulario no se puede enviar.</li>
<li><b>Cuando escribe por WhatsApp o por correo:</b> sus mensajes y su número o dirección, conservados en esos servicios según sus propias condiciones.</li>
<li><b>Cuando visita el sitio:</b> antes de que pulse «Aceptar», nada por nuestra parte: ninguna cookie y ningún script de terceros. Tras «Aceptar» se cargan Google Analytics y Google Ads, como se describe en la sección Cookies y medición más abajo. Nuestro proveedor de alojamiento (Vercel) conserva registros estándar del servidor por motivos de seguridad. Las páginas con mapa cargan teselas de OpenStreetMap y los horarios de Shabat provienen de Hebcal; esos servicios ven su dirección IP cuando se carga la página.</li>
</ul>"""),
    dict(h2="Quién <i>los recibe</i>", ico="users", html="""<p>Para una estancia en los Alpes, transmitimos su solicitud al prestador de servicios de los Alpes que prepara el presupuesto (chalet, chef, minyan, traslados). Este prestador recibe sus respuestas, incluidas las de alimentación y práctica religiosa, y solo las usa para elaborar su presupuesto. Aparte de él, solo ven los datos los servicios que los almacenan por nuestra cuenta (Google, WhatsApp, Vercel). Nunca vendemos ni compartimos sus datos, y nunca enviamos boletines.</p>"""),
    dict(h2="Cuánto tiempo <i>los conservamos</i>", ico="clock", html="""<p>Las solicitudes y la correspondencia, incluidas las respuestas sobre alimentación y práctica religiosa, se conservan durante tres años después de nuestro último intercambio y luego se eliminan.</p>"""),
    dict(h2="Sus <i>derechos</i>", ico="message-circle", html=f"""<p>Puede preguntar qué datos tenemos sobre usted, pedir que se corrijan o se eliminen, u oponerse a su uso. Puede retirar su consentimiento en cualquier momento escribiendo a {MAIL}; eliminaremos entonces las respuestas sobre salud y práctica religiosa, sin efecto sobre lo hecho antes. Respondemos en el plazo de un mes. También puede presentar una reclamación ante la CNIL, la autoridad francesa de protección de datos, en cnil.fr.</p>"""),
  ])
HE_P = dict(
  desc="מה ש-Mishpacha Tours אוספת בטופס הבקשה, למה, מי מקבל את זה, לכמה זמן, וזכויותיכם לפי ה-GDPR. עוגיות רק בהסכמתכם.",
  chips=["GDPR", "עוגיות רק בהסכמתכם", "נתונים נשמרים 3 שנים"],
  sections=[
    dict(h2="מי <i>אחראי</i>", ico="message-circle", html=f"""<p>Mishpacha Tours, עוסק יחיד המנוהל על ידי המדריכה, בליון, צרפת. יצירת קשר: {MAIL}, או בטופס הבקשה. פרטי העסק מופיעים בעמוד <a href="/he/legal/">מידע משפטי</a>.</p>"""),
    dict(h2="מה אנו <i>אוספים</i>", icos=["calendar-days", "lock", "message-circle", "calendar-x"], html="""<ul>
<li><b>כששולחים את טופס הבקשה:</b> הנופש או הסיור שביקשתם, התאריכים, מספר המשתתפים, השפה, השם, מספר הטלפון או הוואטסאפ, וכתובת דוא״ל אם מסרתם. הטופס שואל גם פרטים שעוזרים לנו להכין את הצעת המחיר: צרכי תזונה ואלרגיות, גילאי הילדים, רמת שמירת המצוות (מניין וכשרות) ותקציב. הטופס כותב שורה בגיליון Google פרטי ושולח לנו דוא״ל.</li>
<li><b>בסיס משפטי:</b> צעדים מקדימים לחוזה לגבי פרטי ההזמנה. לגבי אלרגיות וצרכי תזונה (מידע רפואי) ולגבי שמירת מצוות, אנו נשענים על הסכמתכם המפורשת (סעיף 9(2)(א) ל-GDPR), הניתנת בסימון התיבה מתחת לכפתור השליחה של הטופס. בלי הסכמה זו אי אפשר לשלוח את הטופס.</li>
<li><b>כשכותבים בוואטסאפ או בדוא״ל:</b> ההודעות שלכם והמספר או הכתובת שלכם, נשמרים בשירותים האלה לפי התנאים שלהם.</li>
<li><b>כשמבקרים באתר:</b> לפני שלוחצים על ״לאשר״ אין שום דבר מצדנו: לא עוגיות ולא סקריפטים של צד שלישי. אחרי ״לאשר״ נטענים Google Analytics ו-Google Ads, כמתואר בפרק עוגיות ומדידה להלן. ספק האחסון שלנו (Vercel) שומר יומני שרת רגילים לצורכי אבטחה. דפי המפה טוענים אריחים מ-OpenStreetMap ואת זמני השבת מ-Hebcal; השירותים האלה רואים את כתובת ה-IP שלכם כשהדף נטען.</li>
</ul>"""),
    dict(h2="מי <i>מקבל את זה</i>", ico="users", html="""<p>לנופש באלפים אנו מעבירים את הבקשה לספק השירות באלפים שמכין את הצעת המחיר (צ'אלה, שף, מניין, הסעות). הספק מקבל את התשובות שלכם, כולל תזונה ושמירת מצוות, ומשתמש בהן רק כדי להכין את הצעת המחיר. מלבדו, רואים את המידע רק השירותים ששומרים אותו בשמנו (Google, WhatsApp, Vercel). איננו מוכרים ואיננו משתפים את הפרטים שלכם, ואיננו שולחים ניוזלטרים.</p>"""),
    dict(h2="כמה זמן <i>אנו שומרים</i>", ico="clock", html="""<p>בקשות והתכתבות, כולל התשובות על תזונה ושמירת מצוות, נשמרות שלוש שנים אחרי ההתכתבות האחרונה, ואז נמחקות.</p>"""),
    dict(h2="הזכויות <i>שלכם</i>", ico="message-circle", html=f"""<p>אפשר לבקש לדעת מה אנו מחזיקים עליכם, לתקן או למחוק, או להתנגד לשימוש בו. אפשר לבטל את ההסכמה בכל עת בכתיבה אל {MAIL}; נמחק אז את התשובות על בריאות ועל שמירת מצוות, בלי השפעה על מה שנעשה קודם. אנו עונים תוך חודש. אפשר גם להגיש תלונה ל-CNIL, רשות הגנת המידע בצרפת, ב-cnil.fr.</p>"""),
  ])

FR_L = dict(
  title="Mentions légales et éditeur", h1="Mentions légales", ital="qui édite ce site", crumb="Mentions légales",
  desc="Mentions légales de Mishpacha Tours : éditeur, statut d'entreprise individuelle, SIREN, adresse à Lyon, directrice de la publication, contact et hébergeur du site.",
  intro="Ce site est édité par Mishpacha Tours, entreprise individuelle basée à Lyon. Cette page donne l'identité de l'éditeur et de l'hébergeur, et les moyens de nous joindre.",
  chips=["Entreprise individuelle", "Lyon, France", "Hébergé par Vercel"], suite=("Pour <i>aller plus loin</i>", "Confidentialité", "Conditions de réservation"),
  sections=[
    dict(h2="Qui <i>édite</i> ce site", icos=["badge-check", "users", "file-text", "map-pin", "scroll-text", "info"], html=f"""<ul>
<li><b>Nom commercial :</b> Mishpacha Tours</li>
<li><b>Exploitée par :</b> Elisabeth Timsit, guide-conférencière</li>
<li><b>SIREN :</b> {SIREN}</li>
<li><b>Adresse :</b> Lyon, France</li>
<li><b>Forme juridique :</b> entreprise individuelle, sans capital social</li>
<li><b>TVA :</b> non applicable, article 293 B du Code général des impôts</li>
</ul>"""),
    dict(h2="Directrice de la <i>publication</i>", ico="users", html="""<p>Elisabeth Timsit.</p>"""),
    dict(h2="Nous <i>joindre</i>", ico="message-circle", html=f"""<p>Par le <a href="/fr/plan-your-trip/">formulaire de demande</a> ou par e-mail à {MAIL}.</p>"""),
    dict(h2="<i>Hébergement</i>", ico="house", html="""<p>Vercel Inc., 440 N Barranca Ave #4133, Covina, CA 91723, États-Unis.</p>"""),
    dict(h2="<i>Contenu</i> du site", ico="book-open", html="""<p>Les textes et la mise en page de ce site appartiennent à Mishpacha Tours. Les crédits des photographies figurent sur la page <a href="/fr/credits/">Crédits photo</a>.</p>"""),
    dict(h2="<i>Données</i> personnelles", ico="shield-check", html="""<p>Ce que nous collectons, pourquoi et pour combien de temps est expliqué dans la <a href="/fr/privacy/">politique de confidentialité</a>.</p>"""),
  ])
ES_L = dict(
  title="Aviso legal y editor", h1="Aviso legal", ital="quién edita este sitio", crumb="Aviso legal",
  desc="Aviso legal de Mishpacha Tours: editor, empresa individual, SIREN, dirección en Lyon, directora de la publicación, contacto y proveedor de alojamiento del sitio.",
  intro="Este sitio está editado por Mishpacha Tours, empresa individual con sede en Lyon. Esta página indica la identidad del editor y del proveedor de alojamiento, y cómo contactarnos.",
  chips=["Empresa individual", "Lyon, Francia", "Alojado en Vercel"], suite=("Siga <i>leyendo</i>", "Privacidad", "Condiciones de reserva"),
  sections=[
    dict(h2="Quién <i>edita</i> este sitio", icos=["badge-check", "users", "file-text", "map-pin", "scroll-text", "info"], html=f"""<ul>
<li><b>Nombre comercial:</b> Mishpacha Tours</li>
<li><b>Explotada por:</b> Elisabeth Timsit, guía-conferenciante</li>
<li><b>SIREN:</b> {SIREN}</li>
<li><b>Dirección:</b> Lyon, Francia</li>
<li><b>Forma jurídica:</b> empresa individual, sin capital social</li>
<li><b>IVA:</b> no aplicable, artículo 293 B del Código General Tributario francés</li>
</ul>"""),
    dict(h2="Directora de la <i>publicación</i>", ico="users", html="""<p>Elisabeth Timsit.</p>"""),
    dict(h2="Cómo <i>contactarnos</i>", ico="message-circle", html=f"""<p>Mediante el <a href="/es/plan-your-trip/">formulario de solicitud</a> o por correo electrónico a {MAIL}.</p>"""),
    dict(h2="<i>Alojamiento</i>", ico="house", html="""<p>Vercel Inc., 440 N Barranca Ave #4133, Covina, CA 91723, Estados Unidos.</p>"""),
    dict(h2="<i>Contenido</i> del sitio", ico="book-open", html="""<p>Los textos y el diseño de este sitio pertenecen a Mishpacha Tours. Los créditos de las fotografías figuran en la página de <a href="/es/credits/">créditos fotográficos</a>.</p>"""),
    dict(h2="<i>Datos</i> personales", ico="shield-check", html="""<p>Qué recogemos, por qué y durante cuánto tiempo se explica en la <a href="/es/privacy/">política de privacidad</a>.</p>"""),
  ])
HE_L = dict(
  title="מידע משפטי ופרטי המפעיל", h1="מידע משפטי", ital="מי מפעיל את האתר", crumb="מידע משפטי",
  desc="המידע המשפטי של Mishpacha Tours: מפעיל האתר, מעמד של עוסק יחיד, SIREN, כתובת בליון, העורכת האחראית, יצירת קשר וספק האחסון של האתר.",
  intro="האתר מופעל על ידי Mishpacha Tours, עוסק יחיד הממוקם בליון. בעמוד הזה מפורטים פרטי המפעיל וספק האחסון, ודרכי יצירת הקשר.",
  chips=["עוסק יחיד", "ליון, צרפת", "אחסון ב-Vercel"], suite=("להמשך <i>קריאה</i>", "פרטיות", "תנאי הזמנה"),
  sections=[
    dict(h2="מי <i>מפעיל</i> את האתר", icos=["badge-check", "users", "file-text", "map-pin", "scroll-text", "info"], html=f"""<ul>
<li><b>שם העסק:</b> Mishpacha Tours</li>
<li><b>מנוהל על ידי:</b> Elisabeth Timsit, מדריכה מוסמכת (guide-conférencière)</li>
<li><b>SIREN:</b> <span dir="ltr">{SIREN}</span></li>
<li><b>כתובת:</b> ליון, צרפת</li>
<li><b>צורת התאגדות:</b> עוסק יחיד (entreprise individuelle), ללא הון מניות</li>
<li><b>מע״מ:</b> לא חל, סעיף 293 B בקוד המסים הכללי הצרפתי</li>
</ul>"""),
    dict(h2="העורכת <i>האחראית</i>", ico="users", html="""<p>Elisabeth Timsit.</p>"""),
    dict(h2="איך <i>יוצרים קשר</i>", ico="message-circle", html=f"""<p>דרך <a href="/he/plan-your-trip/">טופס הבקשה</a> או בדוא״ל אל {MAIL}.</p>"""),
    dict(h2="<i>אחסון</i>", ico="house", html="""<p>Vercel Inc., 440 N Barranca Ave #4133, Covina, CA 91723, ארצות הברית.</p>"""),
    dict(h2="<i>תוכן</i> האתר", ico="book-open", html="""<p>הטקסטים והעיצוב של האתר שייכים ל-Mishpacha Tours. קרדיטים לתמונות מופיעים בעמוד <a href="/he/credits/">קרדיטים לתמונות</a>.</p>"""),
    dict(h2="<i>מידע</i> אישי", ico="shield-check", html="""<p>מה אנו אוספים, למה ולכמה זמן מוסבר ב<a href="/he/privacy/">מדיניות הפרטיות</a>.</p>"""),
  ])

PRIV = {"en": dict(sections=EN_P["sections"], chips=EN_P["chips"], desc=EN_P["desc"]), "fr": FR_P, "es": ES_P, "he": HE_P}
LEG = {"en": dict(title=EN_L["title"], h1=EN_L["h1"], ital=EN_L["ital"], crumb="Legal notice", desc=EN_L["desc"], intro=EN_L["intro"], chips=EN_L["chips"],
                  sections=EN_L["sections"], suite=("Keep <i>reading</i>", "Privacy", "Terms of booking")),
       "fr": FR_L, "es": ES_L, "he": HE_L}
def chemin(slug, lang): return (f"{lang}/" if lang != "en" else "") + slug + "/index.html"

# ------------------------------------------------------------------ rendu
def img(n, note=False): return f'<img class="dk dk-ico{" dk-ico-note" if note else ""} dk-des" src="/img/des/{n}.webp" alt="" width="96" height="96" loading="lazy">'
def rendre(sec):
    h = sec["html"].strip()
    if h.startswith("<ul>"):
        lis = re.findall(r"<li>(.*?)</li>", h, re.S); ic = sec["icos"]
        return f'<section class="ss wrap conseils"><h2>{sec["h2"]}</h2><ul class="dk-cartes">\n' + "\n".join(f"<li>{img(ic[i % len(ic)])}{li}</li>" for i, li in enumerate(lis)) + "\n</ul></section>"
    inner = re.match(r"<p>(.*)</p>$", h, re.S).group(1)
    return f'<section class="ss wrap conseils dk-note"><h2>{sec["h2"]}</h2><p>{img(sec["ico"], True)}{inner}</p></section>'
def sections(secs): return "".join(rendre(s) for s in secs)
CHECK = '<li><svg class="dk dk-coche" aria-hidden="true" focusable="false"><use href="/img/pictos.svg#check"/></svg>'
def chips_html(c): return '<ul class="chips dk-chips">' + "".join(f"{CHECK}{x}</li>" for x in c) + "</ul>"
def split(s):
    a = s.index("<main>"); b = s.index("</main>")
    h = s.index("</section>", s.index('<section class="pratique-hero')) + len("</section>")
    return a, h, b
def ecrire(p, s): io.open(p, "w", encoding="utf-8", newline="\n").write(s)
def lire(p): return io.open(p, encoding="utf-8", newline="").read()
COOKIES_RE = r'<section class="ss wrap conseils" id="cookies-mesure">.*?</section>'

def ld_maj(s, fn):
    m = re.search(r'<script type="application/ld\+json">(.*?)</script>', s, re.S); data = json.loads(m.group(1))
    for b in data: fn(b)
    return s[:m.start(1)] + json.dumps(data, ensure_ascii=False) + s[m.end(1):]

def privacy(lang):
    p = chemin("privacy", lang); s = re.sub(COOKIES_RE, "", lire(p), flags=re.S); T = PRIV[lang]
    a, h, b = split(s)
    suite = s[s.rfind("<section", 0, b):b]
    hero = re.sub(r'<ul class="chips dk-chips">.*?</ul>', lambda m: chips_html(T["chips"]), s[a:h], count=1, flags=re.S)
    s = s[:a] + hero + sections(T["sections"]) + suite + s[b:]
    d = html.escape(T["desc"], quote=True)
    s = re.sub(r'(<meta name="description" content=")[^"]*(")', lambda m: m.group(1) + d + m.group(2), s, count=1)
    s = re.sub(r'(<meta property="og:description" content=")[^"]*(")', lambda m: m.group(1) + d + m.group(2), s, count=1)
    s = ld_maj(s, lambda x: x.update(description=T["desc"]) if x.get("@type") == "WebPage" else None)
    ecrire(p, s); print("ok", p)

def legal(lang):
    s = re.sub(COOKIES_RE, "", lire(chemin("privacy", lang)), flags=re.S); T = LEG[lang]
    a, h, b = split(s); suite = s[s.rfind("<section", 0, b):b]; hero = s[a:h]
    hero = re.sub(r"(<h1>).*?(</h1>)", lambda m: f'{m.group(1)}{T["h1"]}<br><i>{T["ital"]}</i>{m.group(2)}', hero, count=1, flags=re.S)
    hero = re.sub(r'(<p class="intro-fiche">).*?(</p>)', lambda m: m.group(1) + T["intro"] + m.group(2), hero, count=1, flags=re.S)
    hero = re.sub(r'<ul class="chips dk-chips">.*?</ul>', lambda m: chips_html(T["chips"]), hero, count=1, flags=re.S)
    hero = re.sub(r'(<p class="fil">.*?/ )[^<]*(</p>)', lambda m: m.group(1) + html.escape(T["crumb"]) + m.group(2), hero, count=1, flags=re.S)
    # suite : deux vignettes, Terms et Privacy (le lien Credits devient Privacy)
    h2s, privtxt, termstxt = T["suite"]
    suite = re.sub(r"<h2>.*?</h2>", lambda m: f"<h2>{h2s}</h2>", suite, count=1)
    suite = re.sub(r'href="([^"]*)credits/">[^<]*<', lambda m: f'href="{m.group(1)}privacy/">{privtxt}<', suite, count=1)
    suite = suite.replace("book-open.webp", "shield-check.webp")
    suite = re.sub(r'(href="[^"]*terms/">)[^<]*<', lambda m: m.group(1) + termstxt + "<", suite, count=1)
    out = s[:a] + hero + sections(T["sections"]) + suite + s[b:]
    ib = out.index("<body"); head, rest = out[:ib], out[ib:]
    head = head.replace("privacy/", "legal/")
    rest = re.sub(r'(<li><a href="/(?:(?:fr|es|he)/)?)privacy/"', r'\1legal/"', rest)
    tt = html.escape(T["title"] + " | Mishpacha Tours", quote=True); d = html.escape(T["desc"], quote=True)
    head = re.sub(r"<title>.*?</title>", lambda m: f"<title>{tt}</title>", head, count=1, flags=re.S)
    head = re.sub(r'(<meta property="og:title" content=")[^"]*(")', lambda m: m.group(1) + tt + m.group(2), head, count=1)
    head = re.sub(r'(<meta name="description" content=")[^"]*(")', lambda m: m.group(1) + d + m.group(2), head, count=1)
    head = re.sub(r'(<meta property="og:description" content=")[^"]*(")', lambda m: m.group(1) + d + m.group(2), head, count=1)
    def f(x):
        if x.get("@type") == "BreadcrumbList": x["itemListElement"][-1]["name"] = T["crumb"]
        if x.get("@type") == "WebPage": x.update(name=T["title"], description=T["desc"])
    head = ld_maj(head, f)
    p = chemin("legal", lang); os.makedirs(os.path.dirname(p) or ".", exist_ok=True); ecrire(p, head + rest); print("ok", p)

if __name__ == "__main__":
    import _mesure   # section « Cookies et mesure » (PRIV de _mesure.py) posée sur les pages privacy
    LG = ("en", "fr", "es", "he")
    for lg in LG: privacy(lg)
    for lg in LG: legal(lg)
    for lg in LG: _mesure.page(chemin("privacy", lg), False)
    for lg in LG: _mesure.page(chemin("legal", lg), False)
