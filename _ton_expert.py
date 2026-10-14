# -*- coding: utf-8 -*-
"""Ton expert (14/10) : retire des 4 langues (texte visible, FAQ JSON-LD, meta) les béquilles « what is published »,
« according to … », sources de presse ou de sites tiers, « ask for … in writing », fait divers, bas de page « Sources : ».
Les faits restent (distances, altitudes, horaires, services), seules les béquilles sautent.
Idempotent : une deuxième passe ne trouve plus rien. À lancer après _lead.py, avant _decor.py.
  python _ton_expert.py            : toutes les pages
  python _ton_expert.py --dry      : liste ce qui serait supprimé ou réécrit, sans écrire
Les sources restent dans les modules _pages/*.py (commentaires et VERIF), jamais à l'écran."""
import io, os, re, sys, glob, html, json

ICI = os.path.dirname(os.path.abspath(__file__))
os.chdir(ICI)
LANGS = ('fr', 'es', 'he')
SENT = ''   # marque d'une suppression, pour nettoyer les conteneurs vides

# ---------------------------------------------------------------- règles par langue
# prot : phrases laissées intactes. rew : réécritures (regex, remplacement) appliquées dans l'ordre sur la phrase.
# dele : toute phrase qui correspond encore après réécriture est supprimée.
DOM = r'(?:\.(?:com|fr|org|uk|eu|net|city|io|gouv\.fr)\b)'
R = {}

R['en'] = dict(
  prot=[r'meeting points online', r'do not publish them'],
  rew=[
    (r'what is published, what we organise', 'what we organise'),
    (r'^What is published and what we organise in each', 'What we organise in each'),
    (r'\s*[:,]\s*what is published$', ''),
    (r'a published (?:Jewish )?community', 'a Jewish community'),
    (r'^published community$', 'Jewish community'),
    (r'\s*\(photographed[^)]*\)', ''),
    (r'^The same article places a kosher supermarket in the resort', 'The resort has a kosher supermarket'),
    (r'^The article says kosher organisations', 'Kosher organisations'),
    (r'^The same article reports that the organiser', 'The organiser'),
    (r', which an article describes as open', ', open'),
    (r', what is published for Chamonix,', ','),
    (r', ce qui est publié pour Chamonix,', ','),
    (r', qué hay publicado para Chamonix,', ','),
    (r', מה שפורסם על שאמוני,', ','),
    (r',? depending on the source(?: and the year)?', ''),
    (r'a published Chabad (service|house|office)', r'a Chabad \1'),
    (r'^Supervision is rarely published[^.:;]*[:;]\s*', ''),
    (r'[Aa]sk for the (?:details of supervision|supervision details|details)(?: of the supervision)? in writing with your quote(?:, as you would anywhere)?', 'the supervision details come in writing with your quote'),
    (r'^AFP \(Sud Radio, 23 August 2026\) reports that ', ''),
    (r', and that a ', ', and a '),
    (r', and according to (?:his|her|its) biography ', ' and '),
    (r'^According to [^,]*, ', ''),
    (r'\s*\((?![^()]*@)(?:[^()]*?(?:' + DOM + r'|checked|read on|read \d|consulted)[^()]*)\)', ''),
    (r'; (?:other sites|Alps2Alps|transfer operators|transfer companies)[^.]*', ''),
    (r',? (?:and )?according to (?!the weather)(?:[^.;]|\.(?=\w))*', ''),
    (r',? per the (?:[^.;]|\.(?=\w))*', ''),
    (r',? as listed by (?:[^.;]|\.(?=\w))*', ''),
    (r'Our standard and the sourced facts are on', 'Our standard is on'),
    (r'answered with what we can source and clear about what is not published', 'with straight answers'),
    (r'^Most Jewish visits to Lyon pass without incident, and every', 'Every'),
    (r'^Antisemitic acts do occur in the Lyon area, so we give you the figures and the practical steps below, without alarm and without spin\.', 'Our standard and the practical steps follow.'),
    (r',? listed (?:as [a-z ]+ )?on (?:mikvah\.org|Chabad\.org|ci-aixlesbains\.fr)', ''),
    (r'is listed as (open nightly) on mikvah\.org', r'is '),
    (r'^Listed on Chabad\.org at ', 'At '),
    (r'Security gets a direct answer, without alarm and without spin\.', 'Security gets a direct answer.'),
    (r'Jewish travel to Lyon: the honest FAQ', 'Jewish travel to Lyon: the FAQ'),
    (r'^the honest FAQ$', 'the FAQ'),
    (r'The sourced facts', 'The facts'),
  ],
  dele=[r'publish(?:ed|es)\b', r'\bpublish (?!them)', r'Sources?\s*:', r'\bAFP\b', r'Sud Radio', r'Euronews', r'j2ski', r'alps2alps', r'(?-i:VERIF)',
        r'\bwe found\b', r'\bwe have not verified', r'not verified', r'\bsources we\b', r'\bwe read\b', r'we could reach', r'we know of no', r'we name no\b', r'we name none',
        r'\bsourced?\b', r'[Cc]hecked \d', r'(?:read|consulted) (?:on )?\d', r'^Here is what', r'This is what we found', r'[Aa]sk before you book', r'ask for it in writing',
        r'in writing before you (?:book|travel)', r'\bincident', r'What we promise is the standard', r'Lyon Capitale', r'Interior Minist', r'(?i:Pr[ée]fecture)', r'prosecutor', r'Sentinelle', r'shopkeeper', r'The same report',
        r'\bthe (?:Jewish |ski )?press\b', r'press article', r'blog post', r'does not verify', r'operators we found', r'[Ss]ourced, with gaps',
        r'JGuide', r'skikosher', r'TripAdvisor', r'mikvah\.org', r'(?<!\w)chabad\.org', r'ci-aixlesbains', r'alloj', r'koshertraveldeals', r'wreschner', r'thejewishweekly', r'williamsburg365', r'mikvelyon', r'ynetnews', r'telephone\.city', r'seechamonix', r'Kosher Travel Deals', r'Kosher Outdoor', r'sources? (?:differ|diverge|disagree|date)', r'two sources', r'(?:No|no) source', r'Listed on', r'listing gives', r'^The (?:same )?article', r'^Sources? give', r'directory does not', r'Website listed', r'Contact person listed', r'could read the'],
)

R['fr'] = dict(
  prot=[r'ne publiez pas', r'Ne publiez pas'],
  rew=[
    (r'\s*:\s*ce qui est publié, ce que nous organisons', ' : ce que nous organisons'),
    (r'^Ce qui est publié et ce que nous organisons dans chacune', 'Ce que nous organisons dans chacune'),
    (r'\s*:\s*ce qui est publié$', ''),
    (r'(?:une|la) communauté publiée', 'une communauté juive'),
    (r'^communauté publiée$', 'communauté juive'),
    (r'\s*\(photographié[^)]*\)', ''),
    (r'^Le même article situe dans la station un supermarché casher', 'La station compte un supermarché casher'),
    (r'^Selon l’article, des organisations', 'Des organisations'),
    (r'^Le même article indique que l’organisateur', 'L’organisateur'),
    (r', qu’un article décrit comme ouverte', ', ouverte'),
    (r',? selon la source(?: et l’année)?', ''),
    (r'(office|maison) Chabad publié(?:e)?', r'\1 Chabad'),
    (r'^La (?:surveillance rabbinique|supervision) est rarement publiée[^.:;]*[:;]\s*', ''),
    (r'[Dd]emandez le détail (?:de la surveillance rabbinique )?par écrit avec votre devis(?:, comme partout ailleurs)?', 'le détail de la surveillance rabbinique vous est remis par écrit avec le devis'),
    (r'^L’AFP \(Sud Radio, 23 août 2026\) rapporte que ', ''),
    (r', et qu’un séminaire', ', et un séminaire'),
    (r',? et selon sa biographie ', ' et '),
    (r'^Selon [^,]*, ', ''),
    (r'\s*\((?![^()]*@)(?:[^()]*?(?:' + DOM + r'|vérifi|consult|lu le)[^()]*)\)', ''),
    (r',? (?:selon|d[’\']après) (?:j2ski|alps2alps|Alps2Alps|jguide|SNCF|Omio|FlixBus|Sport 2000|l[’\']office|la station|l[’\']annuaire|un prestataire|la ville|sa biographie|le grand-rabbin|les historiens|une synthèse|le directeur|l[’\']article|Vinci|les guides|des guides|la page|notre estimation|notre mesure|son site|la source|la liste officielle|l[’\']AFP|des sites|les sociétés)(?:[^.;]|\.(?=\w))*', ''),
    (r'; (?:d[’\']autres sites|Alps2Alps|les sociétés de transfert)[^.]*', ''),
    (r'Notre standard et les faits sourcés se trouvent sur', 'Notre standard se trouve sur'),
    (r'avec les réponses que nous pouvons sourcer et la mention claire de ce qui n’est pas publié', 'avec des réponses franches'),
    (r'^La plupart des visites juives à Lyon se passent sans incident, et chaque', 'Chaque'),
    (r' Des actes antisémites ont bien lieu dans la région, aussi[^.]*\.', ' Notre standard et les gestes pratiques suivent.'),
    (r'La sécurité reçoit une réponse directe, sans alarme et sans enjolivement\.', 'La sécurité reçoit une réponse directe.'),
    (r'la FAQ honnête', 'la FAQ'),
    (r'^Des actes antisémites ont lieu dans la région lyonnaise[^.]*\.', 'Notre standard et les gestes pratiques suivent.'),
    (r'^Répertorié sur Chabad\.org au ', 'Au '),
    (r' (?:est indiqué|figure) (ouvert chaque soir) sur mikvah\.org', r' est '),
    (r'(?:, )?répertoriés? sur ci-aixlesbains\.fr', ''),
  ],
  dele=[r'publi(?:é|ée|és|ées|ent|ons|er)\b', r'\bpublie\b', r'non publi', r'Sources?\s*:', r'\bAFP\b', r'Sud Radio', r'Euronews', r'j2ski', r'(?i:alps2alps)', r'(?-i:VERIF)',
        r'sources? que nous', r'sources trouvées', r'nous avons (?:trouvé|lu|consulté)', r'n’avons (?:trouvé|pas vérifié)', r'nous ne connaissons aucun', r'(?:vérifi|consult)(?:é|ée|és|ées) le \d', r'lu le \d', r'^Voici ce que',
        r'\bsourcer\b', r'sourcés?\b', r'[Dd]emand\w+[^.]*par écrit', r'ne vérifie pas', r'non vérifié', r'pas vérifié', r'exploitants que nous',
        r'\bincident', r'Lyon Capitale', r'ministre de l’Intérieur', r'parquet', r'préfecture', r'Sentinelle', r'commerçant', r'la presse', r'article de presse', r'presse juive', r'article de blog',
        r'JGuide', r'skikosher', r'TripAdvisor', r'Le site ne vérifie', r'sources? (?:divergent|donnent|datent)', r'Deux sources', r'^(?:Le même article|L’article)', r'avec sources', r'^Un annuaire de stations', r'^L’annuaire ne précise', r'seconde source', r'source nommée', r'faute de source', r'n’en citons', r'relevé ces horaires', r'Nous avons pu lire', r'nous avons bien'],
)

R['es'] = dict(
  prot=[],
  rew=[
    (r'\s*:\s*lo publicado, lo que organizamos', ': lo que organizamos'),
    (r'^Lo publicado y lo que organizamos en cada una', 'Lo que organizamos en cada una'),
    (r'\s*:\s*(?:lo que se ha publicado|qué hay publicado)$', ''),
    (r'una comunidad con información publicada', 'una comunidad judía'),
    (r'\s*\(fotografiado[^)]*\)', ''),
    (r'^El mismo artículo sitúa en la estación un supermercado kosher', 'La estación cuenta con un supermercado kosher'),
    (r'^El artículo dice que las organizaciones', 'Las organizaciones'),
    (r'^El mismo artículo cuenta que el organizador', 'El organizador'),
    (r', que un artículo describe como abierta', ', abierta'),
    (r'y los datos con sus fuentes están en', 'está en'),
    (r'(servicio|casa) de Chabad publicad[oa]', r'\1 de Chabad'),
    (r'^La supervisión rara vez se publica[^.:;]*[:;]\s*', ''),
    (r'[Pp]ida los detalles de la supervisión por escrito con su presupuesto(?:, como haría en cualquier sitio)?', 'los detalles de la supervisión se entregan por escrito con el presupuesto'),
    (r'^La AFP \(Sud Radio, 23 de agosto de 2026\) cuenta que ', ''),
    (r', y que un ', ', y un '),
    (r',? y según su biografía ', ' y '),
    (r'^Según [^,]*, ', ''),
    (r'\s*\((?![^()]*@)(?:[^()]*?(?:' + DOM + r'|comprobad|verificad|consultad|leíd)[^()]*)\)', ''),
    (r'\s*según la (?:propia estación|oficina de turismo),?\s*', ' '),
    (r',? según (?:j2ski|alps2alps|Alps2Alps|jguide|SNCF|Omio|FlixBus|Sport 2000|el directorio|un proveedor|la ciudad|su biografía|el gran rabino|los historiadores|un resumen|el director|su sitio|nuestra estimación|nuestra medición|las guías|guías|la propia página|la AFP|el artículo|Vinci|la fuente|sitios|las empresas)(?:[^.;]|\.(?=\w))*', ''),
    (r'; (?:otros sitios|Alps2Alps|las empresas de traslados)[^.]*', ''),
    (r'Nuestro estándar y los hechos documentados están en', 'Nuestro estándar está en'),
    (r'con lo que podemos documentar y claros sobre lo que no está publicado', 'con respuestas directas'),
    (r'^La mayoría de las visitas judías a Lyon transcurren sin incidentes, y cada', 'Cada'),
    (r'la FAQ honesta', 'la FAQ'),
    (r'La seguridad recibe una respuesta directa, sin alarma y sin adornos\.', 'La seguridad recibe una respuesta directa.'),
    (r'^En la región de Lyon se producen actos antisemitas[^.]*\.', 'Nuestro estándar y los pasos prácticos siguen a continuación.'),
    (r'^Figura en Chabad\.org en ', 'En '),
    (r' figura como (abierta todas las noches) en mikvah\.org', r' está '),
    (r',? que figuran en ci-aixlesbains\.fr', ''),
  ],
  dele=[r'public(?:ad[oa]s?|an|amos)\b', r'se publica\b', r'no publica\b', r'Fuentes?\s*:', r'\bAFP\b', r'Sud Radio', r'Euronews', r'j2ski', r'(?i:alps2alps)', r'(?-i:VERIF)',
        r'fuentes que', r'hemos (?:encontrado|leído)', r'no (?:encontramos|hemos encontrado)', r'no conocemos ninguna', r'(?:comprobad|verificad|consultad|leíd)[oa]s? el \d', r'^Esto es lo que',
        r'no verificad', r'no están verificadas', r'no verifica', r'documentar', r'\bincidente', r'Lyon Capitale', r'ministro del Interior', r'fiscal[ií]a', r'prefectura', r'Sentinelle',
        r'comerciante', r'la prensa', r'artículo de prensa', r'entrada de blog', r'artículo de blog', r'operadores que encontramos', r'[Pp]ida \w+[^.]*por escrito', r'Pregunte antes de reservar',
        r'JGuide', r'skikosher', r'TripAdvisor', r'Fuente\b'],
)

R['he'] = dict(
  prot=[],
  rew=[
    (r'\s*[:,]\s*מה פורסם$', ''),
    (r'^מה פורסם$', ''),
    (r'^מעשים אנטישמיים אכן מתרחשים[^.]*\.', 'הסטנדרט שלנו והצעדים המעשיים מובאים בהמשך.'),
    (r'^רוב הביקורים של יהודים בליון עוברים בלי אירוע, וכל', 'כל'),
    (r'^רשום ב-Chabad\.org בכתובת ', 'בכתובת '),
    (r' רשום כ(פתוח מדי לילה) ב-mikvah\.org', r' '),
    (r'בית חב״ד מפורסם', 'בית חב״ד'),
    (r'קהילה מפורסמת', 'קהילה יהודית'),
    (r'בקשו את פרטי ההשגחה בכתב יחד עם הצעת המחיר(?:, כמו בכל מקום)?', 'פרטי ההשגחה נמסרים בכתב יחד עם הצעת המחיר'),
    (r'^פרטי ההשגחה כמעט אינם מפורסמים[^.:;]*[:;]\s*', ''),
    (r'\s*\((?![^()]*@)(?:[^()]*?(?:' + DOM + r'|נבדק|נקרא|נקראו)[^()]*)\)', ''),
    (r',? לפי (?:j2ski|alps2alps|Alps2Alps|jguide|SNCF|Omio|FlixBus|Sport 2000|[A-Za-z]|לשכת התיירות|האתר|התחנה|ספק|העיר|הביוגרפיה|הרב הגדול|היסטוריונים|סיכום|מנהל|המקור|הערכתנו|המדידה|רשימות|מדריכי|מדריך|הדף|הכתבה|התחנה)(?:[^.;]|\.(?=\w))*', ''),
    (r', בלי הפחדה ובלי (?:ספין|ייפוי)', ''),
    (r'; (?:אתרים אחרים|Alps2Alps|חברות הסעות)[^.]*', ''),
  ],
  dele=[r'פורס[מם]', r'מפורס[מם]', r'מפרס[מם]', r'לפרס[מם]', r'^המאמר', r'^רשימת אתרי סקי נותנת', r'מקורות', r'מקור שני', r'שום מקור', r'מקור מוזכר', r'לתעד', r'מתועד', r'חלוקים', r'לאמת במקור', r'ללא אירוע', r'בלי אירוע', r'עוברים בלי', r'אתר רשום', r'איש קשר רשום', r'הרישום נותן', r'מקור(?:ות)?\s*:', r'\bAFP\b', r'Sud Radio', r'Euronews', r'j2ski', r'(?i:alps2alps)', r'(?-i:VERIF)',
        r'מצאנו', r'קראנו', r'לא אימתנו', r'איננו מכירים', r'נבדק ב', r'נבדקו ב', r'נקרא ב', r'עיתונות', r'Lyon Capitale', r'שר הפנים', r'פרקליטות', r'בעל חנות', r'^הנה מה',
        r'בקשו[^.]*בכתב', r'שאלו[^.]*בכתב', r'אירוע חריג', r'ללא אירועים', r'JGuide', r'skikosher', r'TripAdvisor', r'עם המקורות', r'סרטון', r'כתבה'],
)

# ---------------------------------------------------------------- moteur
def cap(s):
    return s[:1].upper() + s[1:] if s else s

def fix(sent, lang):
    r = R[lang] if lang == 'en' else dict(prot=R[lang]['prot'], rew=R[lang]['rew'] + R['en']['rew'], dele=R[lang]['dele'] + R['en']['dele'])
    u = html.unescape(sent)
    if re.fullmatch(r'[\s.,;:()\-–!?]*', u):
        return sent
    for p in r['prot']:
        if re.search(p, u):
            return sent
    new = u
    for rx, rep in r['rew']:
        new = re.sub(rx, rep, new)
    new = new.strip()
    if lang != 'he' and new and u[:1].isupper():
        new = cap(new)
    if not new or re.fullmatch(r'[\s.,;:()\-–]*', new):
        return None
    if ': ' in new and not re.match(r'(?i)(sources?|fuentes?|source|מקור)', new):
        head, tail = new.split(': ', 1)
        if len(tail) > 35 and any(re.search(d, head, re.I) for d in r['dele']) and not any(re.search(d, tail, re.I) for d in r['dele']):
            new = cap(tail) if lang != 'he' else tail
    for d in r['dele']:
        if re.search(d, new, re.I):
            return None
    if new == u.strip():
        return sent
    return html.escape(new, quote=False).replace('&#x27;', "'")

LOG = []
def respace(t):
    t = re.sub(r'([a-zà-ÿ0-9»)])([.!?])([A-ZÀ-Ý¿¡])', r' ', t)
    return re.sub(r'([֐-׿])([.!?])([֐-׿A-Z])', r' ', t)
def texte(t, lang, ctx=''):
    """Traite un nœud texte : phrase par phrase."""
    parts = re.split(r'(?<=[.!?])(\s+)', t)
    out = []
    changed = False
    for i, p in enumerate(parts):
        if i % 2 == 1:
            out.append(p)
            continue
        if not p.strip():
            out.append(p)
            continue
        lead = re.match(r'\s*', p).group(0)
        trail = re.search(r'\s*$', p).group(0)
        core = p.strip()
        res = fix(core, lang)
        if res is None:
            LOG.append(('DEL', ctx, core))
            out.append(SENT)
            changed = True
        elif res != core:
            LOG.append(('REW', ctx, core + '  =>  ' + res))
            out.append(lead + res + trail)
            changed = True
        else:
            out.append(p)
    if not changed:
        return t
    # retire les espaces orphelins autour des marques de suppression
    s = ''.join(out)
    s = re.sub(r'\s*' + SENT + r'\s*', SENT, s)
    return s

def inert(p):
    return re.sub(r'<(?:svg|img) class="dk[^>]*>(?:.*?</svg>)?', '', p, flags=re.S)

def process_html(s, lang, ctx):
    # blocs à ne pas toucher : scripts et styles (JSON-LD traité à part)
    holders = []
    def hold(m):
        holders.append(m.group(0)); return f'{len(holders)-1}'
    s = re.sub(r'<(script|style)\b.*?</\1>', hold, s, flags=re.S)
    # bas de page « Sources »
    s = re.sub(r'<section class="wrap">\s*<p class="source">.*?</p>\s*</section>\s*', lambda m: (LOG.append(('DEL', ctx, 'bloc Sources')) or SENT), s, flags=re.S)
    s = re.sub(r'<p class="source">.*?</p>\s*', lambda m: (LOG.append(('DEL', ctx, 'p.source')) or SENT), s, flags=re.S)
    # sources en liens externes : « according to <a>site</a> and <a>site</a> » et paragraphes de liens seuls
    ext = r'<a [^>]*href="https?://(?!wa\.me|www\.hebcal|mishpachatours)[^"]*"[^>]*>[^<]*</a>'
    s = re.sub(r',? (?:according to|selon|d.après|según|לפי) ' + ext + r'(?:[,]? (?:and|et|y|ו-) ?' + ext + r')*', lambda m: (LOG.append(('DEL', ctx, 'source en lien')) or ''), s)
    s = re.sub(r'<p>(?:\s|' + SENT + r'|[,;]|' + ext + r')*</p>', lambda m: (SENT if re.search(r'href="https?://', m.group(0)) else m.group(0)), s)
    # titres h2 : forme « Kosher in X: what is published »
    h2r = {
      'en': [(r'(Kosher) (in [^<:]*?): <i>what is published</i>', r'\1 <i>\2</i>'), (r'Safety, <i>without alarm</i>', 'Safe, <i>by design</i>'),
             ],
      'fr': [(r'(Casher) ([^<:]*?) : <i>ce qui est publié</i>', r'\1 <i>\2</i>'), (r'(?<=>)(La sécurité|Sécurité), <i>sans alarmisme</i>', r', <i>pensée dès le départ</i>'), (r'(La sécurité|Sécurité), <i>sans alarmisme</i>', r', <i>pensée dès le départ</i>')],
      'es': [(r'(Kosher) (en [^<:]*?): <i>lo que se ha publicado</i>', r'\1 <i>\2</i>'), (r'Seguridad, <i>sin alarmismo</i>', 'Seguridad, <i>por diseño</i>')],
      'he': [(r'(כשר) (ב[^<:]*?): <i>מה מפורסם</i>', r'\1 <i>\2</i>'), (r'ביטחון, <i>בלי להלחיץ</i>', 'ביטחון, <i>מתוכנן מראש</i>')],
    }[lang]
    for rx, rep in h2r:
        s = re.sub(rx, rep, s)
    toks = re.split(r'(<[^>]+>)', s)
    for i, tk in enumerate(toks):
        if tk.startswith('<') or not tk.strip() or '' in tk:
            continue
        toks[i] = respace(texte(tk, lang, ctx))
    s = ''.join(toks)
    s = nettoyer(s)
    s = re.sub('(\\d+)', lambda m: holders[int(m.group(1))], s)
    return s

def nettoyer(s):
    """Retire les conteneurs devenus vides ou réduits à une étiquette, puis les marques."""
    for _ in range(6):
        before = s
        # éléments en ligne vides
        s = re.sub(r'<(i|b|span)(?: [^>]*)?>\s*(?:' + SENT + r'\s*)*</\1>', lambda m: SENT if SENT in m.group(0) else m.group(0), s)
        s = re.sub(r'<(p|li)(?: [^>]*)?>((?:(?!</\1>).)*?)</\1>',
                   lambda m: SENT if (SENT in m.group(2) and not re.sub(r'<[^>]+>|\s|' + SENT, '', inert(re.sub(r'<b>.*?</b>', '', m.group(2), flags=re.S)))) and not re.search(r'<(?:a|img|svg)\b(?!\s+class="dk)', re.sub(r'<(?:svg|img) class="dk[^>]*>(?:.*?</svg>)?', '', m.group(2), flags=re.S)) else m.group(0), s, flags=re.S)
        # FAQ : details sans réponse
        s = re.sub(r'<details>\s*<summary>(?:(?!</summary>).)*</summary>\s*(?:' + SENT + r'\s*)+</details>', SENT, s, flags=re.S)
        # listes vides
        s = re.sub(r'<ul(?: [^>]*)?>\s*(?:' + SENT + r'\s*)*</ul>', lambda m: SENT if SENT in m.group(0) else m.group(0), s)
        # titre : deux-points ou virgule orphelin
        s = re.sub(r'(<h2[^>]*>(?:(?!</h2>).)*?)\s*[:,]\s*(?:' + SENT + r')?\s*(</h2>)', r'\1\2', s, flags=re.S)
        if s == before:
            break
    # sections réduites au seul titre
    s = re.sub(r'<section class="[^"]*">\s*<h2[^>]*>(?:(?!</h2>).)*</h2>\s*' + SENT + r'(?:\s*' + SENT + r')*\s*</section>', SENT, s, flags=re.S)
    s = re.sub(r'<div class="ss beige">\s*<div class="wrap">\s*<h2[^>]*>(?:(?!</h2>).)*</h2>\s*' + SENT + r'(?:\s*' + SENT + r')*\s*</div>\s*</div>', SENT, s, flags=re.S)
    s = re.sub(r'(</(?:b|a|i|strong)>)' + SENT + r'(?=[^\s<' + SENT + r'])', r' ', s)
    s = re.sub(r'(?<=[.!?:;,])' + SENT + r'(?=[^\s<' + SENT + r'])', ' ', s)
    s = s.replace(SENT, '')
    s = re.sub(r'<(i|b)>\s*</\1>', '', s)
    s = re.sub(r'  +(?=[^<\n])', ' ', s) if False else s
    return s

def process_ld(s, lang, ctx):
    def one(m):
        raw = m.group(1)
        try:
            d = json.loads(raw)
        except Exception:
            return m.group(0)
        def walk(o):
            if isinstance(o, dict):
                if o.get('@type') == 'FAQPage':
                    keep = []
                    for q in o.get('mainEntity', []):
                        a = q.get('acceptedAnswer', {})
                        t = texte_plain(a.get('text', ''), lang, ctx)
                        if t:
                            a['text'] = t; keep.append(q)
                        else:
                            LOG.append(('DEL', ctx, 'FAQ JSON-LD : ' + q.get('name', '')))
                    o['mainEntity'] = keep
                for k, v in list(o.items()):
                    if k in ('description', 'name', 'headline') and isinstance(v, str):
                        o[k] = texte_plain(v, lang, ctx) or v
                    elif k != 'mainEntity':
                        walk(v)
            elif isinstance(o, list):
                for v in o: walk(v)
        walk(d)
        new = json.dumps(d, ensure_ascii=False)
        if json.loads(new) == json.loads(raw):
            return m.group(0)
        return m.group(0).replace(raw, new)
    return re.sub(r'<script type="application/ld\+json">(.*?)</script>', one, s, flags=re.S)

def texte_plain(t, lang, ctx):
    r = texte(html.escape(t, quote=False), lang, ctx)
    return html.unescape(r.replace(SENT, '')).strip()

def process_meta(s, lang, ctx):
    def one(m):
        v = html.unescape(m.group(2))
        new = texte_plain(v, lang, ctx)
        if not new or new == v: return m.group(0)
        return m.group(1) + html.escape(new, quote=True).replace('&#x27;', "'") + m.group(3)
    return re.sub(r'(<meta (?:name="description"|property="og:description"|name="twitter:description") content=")([^"]*)(")', one, s)

def pages():
    for p in glob.glob('**/index.html', recursive=True):
        if p.startswith('_') or 'credits' in p.replace(os.sep, '/').split('/') or '/_' in p.replace(os.sep, '/'):
            continue
        yield p

if __name__ == '__main__':
    dry = '--dry' in sys.argv
    n = 0
    for p in sorted(pages()):
        q = p.replace('\\', '/')
        lang = q.split('/')[0] if q.split('/')[0] in LANGS else 'en'
        s = io.open(p, encoding='utf8', newline='').read()
        t = process_ld(process_meta(process_html(s, lang, q), lang, q), lang, q)
        if t != s:
            n += 1
            if not dry:
                io.open(p, 'w', encoding='utf8', newline='').write(t)
    if dry:
        for k, c, t in LOG:
            print(k, c, '|', t[:300])
    print('pages modifiées :', n, '| opérations :', len(LOG))
