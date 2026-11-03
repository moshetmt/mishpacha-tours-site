"""Phase 2 lot B1, tache 5 (03/11) : formulaire court de l'accueil EN (form#formContact, zone #book) recopie sur les
accueils FR, ES, HE : memes name, memes champs caches, meme JS (/js/court.js, textes traduits lus dans data-*).
Traductions reprises du tunnel /xx/plan-your-trip/ (libelles, indicatif, erreur, envoi, echec) et des accueils (lien WhatsApp).
Remplace le bouton « Personnaliser mon sejour » + lien WhatsApp du ticket. Idempotent."""
import re, pathlib, io

R = pathlib.Path(__file__).parent
TXT = {
    "fr": dict(societe="Société", prenom="Prénom", wa="Numéro WhatsApp", code_aria="Indicatif du pays", code="Indicatif",
               tel_ph="6 12 34 56 78", ou="Où et quand ?", opt="Facultatif", ou_ph="Courchevel, du 17 au 24 janvier",
               envoyer="Envoyer", small="Nous répondons le jour même, jamais pendant Chabbat.", fcwa="Ou écrivez-nous sur WhatsApp",
               langue="Français", manque="Merci d'indiquer votre prénom et votre numéro WhatsApp.", envoi="Envoi…",
               ko="Votre demande n’est pas partie.", msgwa="Envoyer sur WhatsApp", salut="Bonjour, je suis"),
    "es": dict(societe="Empresa", prenom="Nombre", wa="Número de WhatsApp", code_aria="Prefijo del país", code="Prefijo",
               tel_ph="612 345 678", ou="¿Dónde y cuándo?", opt="Opcional", ou_ph="Courchevel, del 17 al 24 de enero",
               envoyer="Enviar", small="Respondemos el mismo día, nunca en Shabat.", fcwa="O escríbanos por WhatsApp",
               langue="Español", manque="Indique su nombre y su número de WhatsApp para que podamos responderle.", envoi="Enviando…",
               ko="Su solicitud no se envió.", msgwa="Enviar por WhatsApp", salut="Hola, soy"),
    "he": dict(societe="חברה", prenom="שם פרטי", wa="מספר וואטסאפ", code_aria="קידומת מדינה", code="קידומת",
               tel_ph="52 123 4567", ou="איפה ומתי?", opt="לא חובה", ou_ph="קורשבל, 17 עד 24 בינואר",
               envoyer="שליחה", small="מענה באותו יום, לעולם לא בשבת.", fcwa="או כתבו לנו בוואטסאפ",
               langue="עברית", manque="הוסיפו את השם ואת מספר הוואטסאפ שלכם כדי שנוכל לענות.", envoi="שולחים…",
               ko="הבקשה לא נשלחה.", msgwa="שליחה בוואטסאפ", salut="שלום, אני"),
}


def esc(s):
    return s.replace("&", "&amp;").replace('"', "&quot;").replace("<", "&lt;")


def form_en():
    en = io.open(R / "index.html", encoding="utf-8").read()
    m = re.search(r'<form class="chercheur form-court fc-contact" id="formContact".*?</form>', en, re.S)
    return m.group(0)


def traduire(f, lang, wa_href):
    x = TXT[lang]
    rep = [('<label>Company<input', f'<label>{x["societe"]}<input'),
           ('<span>First name</span>', f'<span>{x["prenom"]}</span>'),
           ('<span id="formContact-wa">WhatsApp number</span>', f'<span id="formContact-wa">{x["wa"]}</span>'),
           ('aria-label="Country code"', f'aria-label="{esc(x["code_aria"])}"'),
           ('<option value="">Code</option>', f'<option value="">{x["code"]}</option>'),
           ('placeholder="52 123 4567"', f'placeholder="{x["tel_ph"]}"'),
           ('<span>Where and when? <em>Optional</em></span>', f'<span>{x["ou"]} <em>{x["opt"]}</em></span>'),
           ('placeholder="Courchevel, 17 to 24 Jan"', f'placeholder="{esc(x["ou_ph"])}"'),
           ('<button type="submit">Send</button>', f'<button type="submit">{x["envoyer"]}</button>'),
           ('<small>We answer the same day, never on Shabbat.</small>', f'<small>{x["small"]}</small>'),
           ('Or write to us on WhatsApp</a>', f'{x["fcwa"]}</a>')]
    for a, b in rep:
        assert a in f, a
        f = f.replace(a, b, 1)
    f = re.sub(r'(<a class="fc-wa" href=")[^"]*(")', lambda m: m.group(1) + wa_href + m.group(2), f, count=1)
    data = (f' data-langue="{esc(x["langue"])}" data-msg-manque="{esc(x["manque"])}" data-msg-envoi="{esc(x["envoi"])}"'
            f' data-msg-ko="{esc(x["ko"])}" data-msg-wa="{esc(x["msgwa"])}" data-msg-salut="{esc(x["salut"])}"')
    return f.replace('data-ou="contact"', 'data-ou="contact"' + data, 1)


def main():
    src = form_en()
    for lang in ("fr", "es", "he"):
        p = R / lang / "index.html"
        t = io.open(p, encoding="utf-8", newline="").read()
        n = t
        if 'id="formContact"' not in n:
            z = n.find('<div class="ticket-zone" id="book">')
            m = re.compile(r'<p class="ticket-plan">.*?</p>\s*<a class="wa" href="([^"]+)"[^>]*>.*?</a>', re.S).search(n, z)
            assert z >= 0 and m, lang
            n = n[:m.start()] + traduire(src, lang, m.group(1)) + n[m.end():]
        if '/js/court.js' not in n:
            n = n.replace('<script src="/config.js">', '<script src="/js/court.js" defer></script><script src="/config.js">', 1)
        if n != t:
            io.open(p, "w", encoding="utf-8", newline="").write(n)
        noms = sorted(set(re.findall(r'name="([^"]+)"', re.search(r'<form[^>]*id="formContact".*?</form>', n, re.S).group(0))))
        print(f"formulaire {lang} : {'modifie' if n != t else 'deja a jour'} ; champs {noms}")
    print("formulaire en (reference) : champs", sorted(set(re.findall(r'name="([^"]+)"', src))))


if __name__ == "__main__":
    main()
