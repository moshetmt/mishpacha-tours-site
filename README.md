# Mishpacha Tours - site v5 (direction retenue le 06/10)

Site statique, un dossier par URL. Les pages sont generees depuis `index.html`
(en-tete et pied repris tels quels) par les scripts ci-dessous, a relancer dans cet
ordre apres toute modification de l'accueil. Le site existe en 4 langues : EN (source) + fr/ es/ he/.

```
python _build_tours.py      # 5 fiches tours (donnees dans le script)
python _build_pratique.py   # kosher, synagogues, chabad, cimetiere
python _build_hub.py        # /jewish-lyon-guide/ et /jewish-life-around-lyon/
python _build_merci.py      # /merci/
python _build_guide.py      # pages du guide depuis _pages/*.py (voir _pages/README.md)
python _build_i18n.py prepare  # hreflang + selecteur de langue sur TOUTES les pages EN, copies fr/ es/ he/ a traduire (n'ecrase pas une traduction faite)
python _build_i18n.py ld       # JSON-LD des copies traduites regenere depuis le JSON-LD EN + title/desc/FAQ/fil d'Ariane traduits (les traducteurs n'y touchent pas)
python _build_sitemap.py    # sitemap.xml + robots.txt + llms.txt (les copies non traduites sont exclues)
python _qa.py               # liens, mots interdits, title/desc, canonical, JSON-LD
python _build_i18n.py check # structure EN / traduit identique, anglais residuel, mots interdits

Traductions : une page EN modifiee n'est PAS repercutee sur fr/ es/ he/ : supprimer la copie et relancer `prepare` (ou
`prepare --force` pour tout, DANGER : ecrase les traductions), puis retraduire, ou reporter la modification a la main dans
les 3 copies. Brief et lexique des traducteurs : `00-brief/charte-graphique/charte-graphique.md` (lexique hebreu) ;
methode = dictionnaire de noeuds texte applique par script, structure de balises identique, verifiee par `check`.
JSON-LD : entite unique `TravelAgency` @id `/#organization` (accueil), `TouristTrip`+`Offer` sur les tours, `WebPage`
(dateModified = `_head.DATE`) partout, `ItemList` de `Place` sur les listes d'adresses (geo depuis `img/geo.json`).
```

## Formulaire de reservation (Apps Script)

Toutes les pages a formulaire chargent `/config.js` et envoient un
`sendBeacon` JSON (tour, dates, personnes, langue, nom, contact, page) vers
`window.MISHPACHA_ENDPOINT`, puis redirigent vers `/merci/`. Tant que la
valeur de repli `ENDPOINT_APPS_SCRIPT_A_POSER` est en place, rien n'est
enregistre : le visiteur voit la page merci, mais la demande est perdue.

1. Google Sheets : creer une feuille « Mishpacha - Leads ».
2. Extensions > Apps Script, coller `apps-script/Code.gs`, Enregistrer.
3. Deployer > Nouveau deploiement > Application web, executer en tant que
   Moi, acces Tout le monde. Copier l'URL `/exec`.
4. La coller dans `config.js` a la place de `ENDPOINT_APPS_SCRIPT_A_POSER`.
   Seul fichier a modifier.

Le champ cache `societe` est un piege a robots : rempli, rien n'est ecrit.

## Deployer

Depuis ce dossier : `vercel deploy --prod` (projet `mishpacha-tours-v5`,
compte contactclims-4659). `vercel.json` sert `X-Robots-Tag: noindex` tant que
le domaine n'est pas branche.
