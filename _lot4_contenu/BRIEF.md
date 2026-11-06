# Brief rédaction : pages de service Mishpacha Tours (lot 4, 06/11/2026)

Tu écris le contenu d'une page de service du site mishpachatours.com, en 4 langues (en, fr, es, he), au format JSON strict ci-dessous, dans `_lot4_contenu/<slug>.json`. Source unique des faits : `_lot4_contenu/FAITS.md` dans le même dossier. Rien d'autre. Tout fait absent du dossier se transforme en « dites-nous… / sur demande » et en question à Mendel (champ `mendel`).

## Ton
Luxe sobre, phrases courtes, concret, aucun jargon marketing, aucun superlatif, aucun « le seul », aucun tiret cadratin, aucune liste de trois adjectifs, pas de « ce n'est pas X, c'est Y ». Vouvoiement en FR et ES. Le casher vient après le confort dans l'ordre des phrases (décision client : « le luxe se dit avant le casher »), mais chaque page dit une fois la formule complète du certificat. En hébreu : registre d'un public religieux israélien, impératif pluriel sur les boutons, lexique du dossier, chiffres et noms latins en caractères latins.

## Schéma JSON (clés par langue : "en", "fr", "es", "he")
```json
{
 "en": {
  "title": "Title tag, 50 à 60 signes, mot-clé en premier, sans ' | Mishpacha Tours' (ajouté ensuite)",
  "description": "Meta description 130 à 155 signes",
  "h1": "Titre principal, 3 à 6 mots",
  "h1_i": "Seconde ligne du titre, 3 à 7 mots (affichée en italique léger)",
  "hero_sub": "Phrase sous le titre dans la bannière, 60 à 90 signes",
  "wa": "Texte prérempli du message WhatsApp du client, 1 phrase + 'Resort: / Dates: / Number of people:' (dans la langue)",
  "phrase": "Phrase d'accroche de l'intro, 8 à 14 mots",
  "trois": [["Titre court 3 à 5 mots", "Une phrase de 10 à 16 mots"], ["…", "…"], ["…", "…"]],
  "intro": ["Paragraphe 1, 45 à 70 mots", "Paragraphe 2, 35 à 60 mots"],
  "inclus_titre": ["Partie normale du titre", "mot(s) en italique"],
  "inclus": [["Titre de l'élément.", "Une ou deux phrases, 15 à 35 mots"], … 4 à 6 éléments],
  "etapes_titre": ["How it", "works"],
  "etapes": [["Titre 2 à 5 mots", "Une ou deux phrases, 15 à 30 mots"], ["…", "…"], ["…", "…"]],
  "faq_titre": ["Partie normale", "questions"],
  "faq": [["Question ?", "Réponse 20 à 50 mots"], … 5 à 6 questions dont une sur le prix (prix du dossier seulement), une sur Chabbat, une sur le certificat],
  "final_titre": ["Your … in the Alps,", "organised"],
  "final_p": "Une phrase, 10 à 18 mots",
  "voyage": "Valeur courte du champ caché 'voyage' du formulaire, en anglais quelle que soit la langue (ex. 'Private chef in the Alps')"
 },
 "fr": { … même schéma … },
 "es": { … },
 "he": { … },
 "mendel": "Message WhatsApp pour Mendel (le partenaire, tutoiement, français, 500 à 900 signes) : 'Salut Mendel, voici le texte de la page <service> du site. Ce qu'elle affirme : … (3 à 6 puces courtes). Questions : 1) … 2) … 3) … (questions fermées oui/non ou A/B, 3 à 6). Réponds par audio si c'est plus simple.' Aucun lien, aucun prix inventé."
}
```

## Contraintes
- Les prix cités sont ceux du dossier, à la lettre, précédés de « à partir de » quand c'est un prix de départ.
- La formule du certificat, en entier, une fois par page, dans la FAQ : FR « Certifié cacher par le Beth Habad de Grenoble-Alpes, Rav Yehia Lahiany » ; EN « Certified kosher by Beth Habad Grenoble-Alpes, Rav Yehia Lahiany » ; ES « Certificado kosher por el Beth Habad Grenoble-Alpes, Rav Yehia Lahiany » ; HE « בהשגחת בית חב״ד גרנובל-אלפים, הרב יחיא לחיאני ».
- La cacherout est lamehadrin (« cacher lamehadrin », « kosher lamehadrin », « כשר למהדרין », règle de Moshé du 06/11). Jamais : hashgaha seul, nombre de chalets, le seul, exclusif, numéro de téléphone, nom de partenaire, hélicoptère, prix absents du dossier, promesse de disponibilité d'un masseur ou d'une activité.
- Pudeur stricte sur la page spa et massage : aucune mention du corps ni de peau ; sérénité, calme, vue, eau, silence.
- Le JSON doit être valide (guillemets droits, pas de virgule finale). Écris le fichier avec l'outil Write, encodage UTF-8.
