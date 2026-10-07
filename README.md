# Mishpacha Tours - site v5 (direction retenue le 06/10)

Site statique, un dossier par URL. Les pages sont generees depuis `index.html`
(en-tete et pied repris tels quels) par quatre scripts, a relancer dans cet
ordre apres toute modification de l'accueil :

```
python _build_tours.py      # 5 fiches tours (donnees dans le script)
python _build_pratique.py   # kosher, synagogues, chabad, cimetiere
python _build_hub.py        # /jewish-lyon-guide/ et /jewish-life-around-lyon/
python _build_merci.py      # /merci/
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
