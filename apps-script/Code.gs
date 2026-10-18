/**
 * Mishpacha Tours - reception du formulaire de demande
 * ---------------------------------------------------------------------
 * doPost lit le JSON envoye par sendBeacon depuis le site, ecrit une ligne
 * horodatee dans la feuille « Mishpacha - Leads », envoie un mail lisible a
 * l'operateur et joint la fiche contact PDF de Mendel (francais, WhatsApp du client compris,
 * decision Moshe du 19/10) et la fiche detaillee en anglais.
 *
 * Envoi automatique a Mendel (decision du 19/10, « B ») : le serveur WhatsApp du CRM (habad-crm)
 * interroge doGet toutes les 10 min, hors Shabbat et fetes : action=liste (demandes non envoyees
 * depuis ENVOI_DEPUIS), action=fiche&id= (PDF en base64), action=fait&id= (marque envoyee).
 * La cle CLE_ENVOI vit dans Secret.gs, hors git : ce dossier est publie sur un depot public.
 *
 * Champs recus : tour, dates, personnes, langue, nom, contact, message (langue
 * du client), message_en (memes reponses en anglais, formulaire en etapes),
 * nuits, page, params. test=1 : mail a l'operateur seul, rien dans la feuille.
 *
 * INSTALLATION : projet cree et deploye par l'API (scripts/creer_apps_script_mishpacha.py,
 * 08/10/2026), mises a jour par scripts/push_apps_script.py mishpacha-tours --apply.
 * L'URL /exec vit dans config.js.
 * ---------------------------------------------------------------------
 */

var DEST_EMAIL = 'contact@mishpachatours.com, mochetimsit@gmail.com, contact@123digital.fr';   // 123digital : fait sonner le telephone de l'operateur (12/10)
var CC_EMAIL = 'timsitelis613@gmail.com';   // la guide, en copie de chaque demande (operateur, 11/10)
var TEST_EMAIL = 'mochetimsit@gmail.com';
// Feuille v2 (16/10) : une colonne par information utile, lisible comme un CRM. L'ancienne
// disposition (ENTETE_V1) est migree automatiquement au premier passage de formater_().
var ENTETE_V1 = ['Date', 'Tour', 'Dates', 'Nombre de personnes', 'Langue', 'Nom',
                 'Email ou WhatsApp', 'Message', 'Page', 'Source', 'Message EN'];
var ENTETE = ['Reçu le', 'Statut', 'Nom', 'WhatsApp', 'E-mail', 'Voyage', 'Lieu', 'Arrivée', 'Départ', 'Nuits',
              'Familles', 'Adultes', 'Enfants', 'Bébés', 'Hommes minyan', 'Logement', 'Repas', 'Minyan et prières',
              'Budget', 'Habite à', 'Langue', 'Page', 'Résumé EN', 'Message original', 'Notes'];
var LARGEURS = [130, 115, 160, 150, 190, 230, 140, 125, 125, 55, 70, 70, 110, 70, 80, 220, 220, 220, 150, 120, 80, 130, 320, 320, 240];
var STATUTS = ['Nouveau', 'Répondu', 'Devis envoyé', 'Gagné', 'Perdu', 'Test'];
var NOM_FEUILLE = 'Leads';
var CLE_FORMAT = 'mt-leads-2026';   // GET /exec?action=formater&cle=... : relance la mise en forme (idempotent, ne supprime rien)
var TZ = 'Europe/Paris';
var ENVOI_DEPUIS = new Date('2026-10-19T00:00:00+02:00');   // demandes plus anciennes : transmises a la main

// Libelles FR/ES/HE des anciennes lignes sans « Message EN » (migration seulement).
var LABELS_EN = {
  'Voyage': 'Trip', 'Viaje': 'Trip', 'נסיעה': 'Trip',
  'Station ou lieu': 'Resort or place', 'Estación o lugar': 'Resort or place', 'אתר או מקום': 'Resort or place',
  'Arrivée': 'Arrival', 'Llegada': 'Arrival', 'הגעה': 'Arrival',
  'Départ': 'Departure', 'Salida': 'Departure', 'יציאה': 'Departure',
  'Familles': 'Families', 'Familias': 'Families', 'משפחות': 'Families',
  'Adultes': 'Adults', 'Adultos': 'Adults', 'מבוגרים': 'Adults',
  'Enfants': 'Children', 'Niños': 'Children', 'ילדים': 'Children',
  'Bébés': 'Babies', 'Bebés': 'Babies', 'תינוקות': 'Babies',
  'Hommes pour le minyan': 'Men for minyan', 'Hombres para el minyan': 'Men for minyan', 'גברים למניין': 'Men for minyan',
  'Hébergement': 'Accommodation', 'Alojamiento': 'Accommodation', 'לינה': 'Accommodation',
  'Repas': 'Meals', 'Comidas': 'Meals', 'ארוחות': 'Meals',
  'Besoins religieux': 'Religious needs', 'Necesidades religiosas': 'Religious needs', 'צרכים דתיים': 'Religious needs',
  'Niveau de minyan': 'Minyan level', 'חשיבות המניין': 'Minyan level',
  'Budget': 'Budget', 'Presupuesto': 'Budget', 'תקציב': 'Budget',
  'Budget par personne': 'Budget per person', 'תקציב לאדם': 'Budget per person',
  'Budget par famille': 'Budget per family', 'תקציב למשפחה': 'Budget per family',
  'Habite à': 'Lives in', 'Vive en': 'Lives in', 'מקום מגורים': 'Lives in',
  'Message': 'Message', 'Mensaje': 'Message', 'הודעה': 'Message'
};

// charte du site v5
var VERT = '#2D5132', JAUNE = '#FCDE73', CREME = '#FFFAED', BEIGE = '#F1EDE6', ENCRE = '#1C1B1F', GRIS = '#8a867f';
var LOGO = 'data:image/png;base64,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';

// Sections de la fiche, par libelle anglais du formulaire en etapes (_build_demande.py, LAB + LAB_NEW).
var SECTIONS = [
  ['The trip',            ['Trip', 'Resort or place', 'Resort choice', 'Accommodation address', 'Pick-up', 'Drop-off']],
  ['Dates',               ['Arrival', 'Time of day', 'Time', 'Departure', 'Dates']],
  ['The group',           ['Families', 'Adults', 'Children', 'Babies', 'Baby equipment', 'Men for minyan', 'Luggage']],
  ['Accommodation',       ['Accommodation', 'Rooms', 'Accommodation options']],
  ['Meals and kashrut',   ['Meals', 'Meal days', 'Allergies and diets', 'Kashrut', 'Kashrut details']],
  ['Shabbat and prayer',  ['Minyan level', 'Religious needs', 'Nusach']],
  ['Getting there',       ['Airport', 'Flying from', 'Flights booked', 'Flights', 'Transport']],
  ['Activities and Lyon', ['Activities', 'Ski levels', 'Lyon', 'Tour language']],
  ['Extras',              ['Extras']],
  ['Budget',              ['Budget per person', 'Budget per family', 'Budget', 'Flights and budget', 'Priorities']],
  ['In their words',      ['Message']]
];
var CONTACT_KEYS = ['Lives in', 'Urgency', 'Booking for'];   // mail seulement, jamais dans le PDF

function doPost(e) {
  var lock = LockService.getScriptLock();
  try {
    lock.waitLock(20000);

    var d = {};
    if (e && e.postData && e.postData.contents) {
      try { d = JSON.parse(e.postData.contents); } catch (err) { d = e.parameter || {}; }
    } else {
      d = (e && e.parameter) || {};
    }

    journal_('recu', txt(d.nom) + (txt(d.test) ? ' (test)' : '') + (txt(d.societe) ? ' PIEGE societe=' + txt(d.societe) : ''));
    // Piege a robots : le champ "societe" doit rester vide, un humain ne le voit jamais.
    if (txt(d.societe)) return json_({ ok: true, piege: true });

    // Rien d'exploitable : ni nom ni contact.
    if (!txt(d.nom) && !txt(d.contact)) return json_({ ok: true, vide: true });

    var test = txt(d.test) === '1' || d.test === true;
    var quand = new Date();
    if (!test) {
      var sh = feuille_();
      ecrireLigne_(sh, d, quand, 'Nouveau');
    }

    envoyerMail_(d, quand, test);
    journal_('ok', txt(d.nom));
    return json_({ ok: true, test: test });

  } catch (err) {
    journal_('ERREUR', String(err && err.stack || err));
    return json_({ ok: false, error: String(err) });
  } finally {
    try { lock.releaseLock(); } catch (err2) {}
  }
}

function doGet(e) {
  var p = (e && e.parameter) || {};
  if (p.action === 'journal' && typeof CLE_ENVOI !== 'undefined' && p.cle === CLE_ENVOI) {
    return json_(JSON.parse(PropertiesService.getScriptProperties().getProperty('JOURNAL') || '[]'));
  }
  if (/^(liste|fiche|fait)$/.test(p.action || '')) {
    if (typeof CLE_ENVOI === 'undefined' || !CLE_ENVOI || p.cle !== CLE_ENVOI) return json_({ ok: false, error: 'cle' });
    return json_(fileMendel_(p.action, txt(p.id)));
  }
  if (p.action === 'formater' && p.cle === CLE_FORMAT) {
    var sh = feuille_();
    var r = formater_(sh, true);
    return ContentService.createTextOutput('Feuille mise en forme : ' + r);
  }
  return ContentService.createTextOutput('Mishpacha Tours form endpoint - OK');
}

function feuille_() {
  // Script autonome (cree par l'API le 08/10/2026) : la feuille "Mishpacha - Leads" est creee au premier envoi
  // et son identifiant garde dans les proprietes du script. Pas de feuille liee.
  var props = PropertiesService.getScriptProperties();
  var id = props.getProperty('SHEET_ID');
  var ss = null;
  if (id) { try { ss = SpreadsheetApp.openById(id); } catch (err) { ss = null; } }
  if (!ss) {
    ss = SpreadsheetApp.create('Mishpacha - Leads');
    props.setProperty('SHEET_ID', ss.getId());
  }
  var sh = ss.getSheetByName(NOM_FEUILLE) || ss.getSheets()[0];
  if (sh.getLastRow() === 0) {
    sh.appendRow(ENTETE);
  }
  if (props.getProperty('FORMAT_V') !== '2') {
    formater_(sh, true);
    props.setProperty('FORMAT_V', '2');
  }
  return sh;
}

// ---------------------------------------------------------------- feuille v2 : une colonne par information

// Ligne de la feuille a partir des champs recus (ou d'une ancienne ligne reconstituee).
function ligne_(d, quand, statut) {
  var f = fiche_(d);
  var m = f.map;
  var nuits = parseInt(txt(d.nuits), 10);
  if (!(nuits > 0) && m['Arrival'] && m['Departure']) nuits = nuits_(m['Arrival'], m['Departure']);
  var budget = [m['Budget per person'] ? m['Budget per person'] + ' / pers.' : '',
                m['Budget per family'] ? m['Budget per family'] + ' / famille' : '',
                m['Budget'], m['Flights and budget']].filter(Boolean).join(' · ');
  var minyan = [m['Minyan level'], m['Religious needs'], m['Nusach']].filter(Boolean).join(' · ');
  var logement = [m['Accommodation'], m['Rooms'], m['Accommodation options']].filter(Boolean).join(' · ');
  var repas = [m['Meals'], m['Meal days'], m['Kashrut'], m['Allergies and diets']].filter(Boolean).join(' · ');
  var resume = txt(d.message_en) || txt(d.message);
  var original = txt(d.message_en) ? txt(d.message) : '';
  return [
    quand, statut || 'Nouveau', f.nom, f.tel ? '+' + f.tel : '', f.mail, f.tour, f.lieu,
    m['Arrival'] || (f.en ? '' : txt(d.dates)), m['Departure'] || '', nuits > 0 ? nuits : '',
    m['Families'] || '', m['Adults'] || (f.en ? '' : txt(d.personnes)), m['Children'] || '', m['Babies'] || '', m['Men for minyan'] || '',
    logement, repas, minyan, budget, m['Lives in'] || '', f.langue, f.page, resume, original, ''
  ].map(function (v) { return typeof v === 'string' ? cel_(v) : v; });
}

function ecrireLigne_(sh, d, quand, statut) {
  var row = ligne_(d, quand, statut);
  sh.appendRow(row);
  var r = sh.getLastRow();
  var tel = String(row[3]).replace(/^'/, '');
  if (tel) {
    var num = tel.replace(/[^0-9]/g, '');
    sh.getRange(r, 4).setRichTextValue(SpreadsheetApp.newRichTextValue().setText(tel).setLinkUrl('https://wa.me/' + num).build());
  }
  sh.getRange(r, 1).setNumberFormat('ddd d mmm yyyy HH:mm');
  sh.getRange(r, 1, 1, ENTETE.length).setVerticalAlignment('middle');
  sh.getRange(r, 16, 1, 9).setWrapStrategy(SpreadsheetApp.WrapStrategy.CLIP);
}

function nuits_(a, b) {
  var da = new Date(a), db = new Date(b);
  if (isNaN(da) || isNaN(db)) return 0;
  return Math.round((db - da) / 86400000);
}

// Ancienne ligne (11 colonnes) -> objet d comme celui du site, labels FR/ES/HE ramenes en anglais.
function ancienne_(v) {
  var message = txt(v[7]), en = txt(v[10]);
  if (!en && message) {
    var traduit = paires_(message).map(function (kv) { return (LABELS_EN[kv[0]] || kv[0]) + ': ' + kv[1]; });
    if (traduit.some(function (s) { return /^(Trip|Arrival|Adults|Accommodation|Meals): /.test(s); })) en = traduit.join(' | ');
  }
  return { tour: v[1], dates: v[2], personnes: v[3], langue: v[4], nom: v[5], contact: v[6],
           message: message, page: v[8], params: v[9], message_en: en };
}

function formater_(sh, migrer) {
  var ss = sh.getParent();
  var tete = sh.getRange(1, 1, 1, Math.max(sh.getLastColumn(), 1)).getValues()[0].map(txt);
  var migre = 0;

  // 1. Migration de l'ancienne disposition, sans rien perdre : l'ancienne feuille est renommee, pas supprimee.
  if (migrer && tete[0] === 'Date' && tete[1] === 'Tour') {
    var vals = sh.getLastRow() > 1 ? sh.getRange(2, 1, sh.getLastRow() - 1, 11).getValues() : [];
    var lignes = vals.filter(function (v) { return txt(v[5]) || txt(v[6]); }).map(function (v) {
      var d = ancienne_(v);
      var statut = /TEST/i.test(txt(v[5])) ? 'Test' : 'Nouveau';
      return { d: d, quand: v[0] instanceof Date ? v[0] : new Date(), statut: statut };
    });
    sh.setName('Ancienne feuille (' + Utilities.formatDate(new Date(), TZ, 'dd-MM') + ')');
    var neuf = ss.insertSheet(NOM_FEUILLE, 0);
    neuf.appendRow(ENTETE);
    lignes.forEach(function (l) { ecrireLigne_(neuf, l.d, l.quand, l.statut); migre++; });
    sh.hideSheet();
    sh = neuf;
  }
  if (sh.getName() !== NOM_FEUILLE) { try { sh.setName(NOM_FEUILLE); } catch (err) {} }

  var n = ENTETE.length, maxR = Math.max(sh.getMaxRows(), 500);
  sh.getRange(1, 1, 1, n).setValues([ENTETE]);

  // 2. En-tete, gel, largeurs
  var h = sh.getRange(1, 1, 1, n);
  h.setBackground(VERT).setFontColor(CREME).setFontWeight('bold').setFontSize(10)
   .setVerticalAlignment('middle').setWrap(true);
  sh.setRowHeight(1, 44);
  sh.setFrozenRows(1);
  sh.setFrozenColumns(3);
  LARGEURS.forEach(function (w, i) { sh.setColumnWidth(i + 1, w); });

  // 3. Corps : alternance, formats, listes
  var corps = sh.getRange(2, 1, maxR - 1, n);
  corps.setVerticalAlignment('middle').setFontSize(10);
  sh.getRange(2, 1, maxR - 1, 1).setNumberFormat('ddd d mmm yyyy HH:mm');
  sh.getRange(2, 10, maxR - 1, 6).setHorizontalAlignment('center');
  sh.getRange(2, 16, maxR - 1, 9).setWrapStrategy(SpreadsheetApp.WrapStrategy.CLIP);
  sh.getRange(2, 25, maxR - 1, 1).setWrapStrategy(SpreadsheetApp.WrapStrategy.WRAP);
  sh.getBandings().forEach(function (b) { b.remove(); });
  sh.getRange(1, 1, maxR, n).applyRowBanding(SpreadsheetApp.BandingTheme.LIGHT_GREY, true, false)
    .setHeaderRowColor(VERT).setFirstRowColor('#FFFFFF').setSecondRowColor(CREME);
  var regle = SpreadsheetApp.newDataValidation().requireValueInList(STATUTS, true).setAllowInvalid(false).build();
  sh.getRange(2, 2, maxR - 1, 1).setDataValidation(regle);

  // 4. Couleur de la ligne selon le statut
  var zone = sh.getRange(2, 1, maxR - 1, n);
  var cf = function (formule, bg, fg) {
    var b = SpreadsheetApp.newConditionalFormatRule().whenFormulaSatisfied(formule).setRanges([zone]);
    if (bg) b.setBackground(bg);
    if (fg) b.setFontColor(fg);
    return b.build();
  };
  sh.setConditionalFormatRules([
    cf('=$B2="Nouveau"', '#FFF3C4', null),
    cf('=$B2="Devis envoyé"', '#E8EEF9', null),
    cf('=$B2="Gagné"', '#DCEFDD', null),
    cf('=$B2="Perdu"', null, '#9A968F'),
    cf('=$B2="Test"', null, '#C2BEB6')
  ]);

  // 5. Filtre sur l'en-tete
  if (sh.getFilter()) sh.getFilter().remove();
  sh.getRange(1, 1, maxR, n).createFilter();
  if (sh.getMaxColumns() > n) sh.deleteColumns(n + 1, sh.getMaxColumns() - n);
  return migre + ' ligne(s) migrée(s), ' + (sh.getLastRow() - 1) + ' lead(s) dans « ' + NOM_FEUILLE + ' »';
}

function urlFeuille() {
  // A lancer une fois dans l'editeur : autorise le script et affiche l'URL de la feuille.
  var sh = feuille_();
  var url = sh.getParent().getUrl();
  Logger.log(url);
  return url;
}

// ---------------------------------------------------------------- lecture de la demande

// "Label: valeur | Label: valeur" -> [[label, valeur], ...] ; une partie sans « : » garde un label vide.
function paires_(s) {
  var out = [];
  txt(s).split(' | ').forEach(function (p) {
    p = p.trim(); if (!p) return;
    var i = p.indexOf(': ');
    out.push(i < 0 ? ['', p] : [p.slice(0, i).trim(), p.slice(i + 2).trim()]);
  });
  return out;
}

function fiche_(d) {
  // Tout ce qu'il faut pour le mail et le PDF, en anglais quand le formulaire en etapes l'a envoye.
  var en = txt(d.message_en);
  var paires = paires_(en || d.message);
  var map = {};
  paires.forEach(function (kv) { if (kv[0] && !map[kv[0]]) map[kv[0]] = kv[1]; });

  var tour = txt(d.tour).replace(/^[^:]{3,30}:\s*/, '');   // « FULL REQUEST: » et ses traductions
  var contact = txt(d.contact);
  var mail = (contact.match(/[^\s\/]+@[^\s\/]+\.[^\s\/]+/) || [''])[0];
  var tel = contact.replace(mail, '').replace(/[^0-9]/g, '').replace(/^(972|33|34|44|32|41|39)0/, '$1');   // « +972 052… » : zero national en trop
  var nuits = parseInt(txt(d.nuits), 10);
  if (en && map['Trip']) tour = map['Trip'];

  var lieu = map['Resort or place'] || map['Resort choice'] || (map['Pick-up'] ? map['Pick-up'] + ' → ' + (map['Drop-off'] || '?') : '');
  var dates = txt(d.dates);
  if (map['Arrival'] && en) dates = map['Arrival'] + (map['Departure'] ? ' → ' + map['Departure'] : '');
  if (nuits > 0) dates += ' (' + nuits + (nuits === 1 ? ' night)' : ' nights)');

  // « Who » en anglais quand le formulaire en etapes l'a envoye (sinon « 5 מבוגרים · 1 families » melange les sens d'ecriture).
  var personnes = txt(d.personnes);
  if (en && map['Adults']) {
    personnes = [map['Adults'] + ' adults', map['Children'] ? map['Children'] + ' children' : '', map['Babies'] ? map['Babies'] + ' babies' : '']
      .filter(Boolean).join(' + ');
  }

  return {
    nom: txt(d.nom) || 'No name', tour: tour, paires: paires, map: map, en: !!en,
    mail: mail, tel: tel, dates: dates, lieu: lieu,
    personnes: personnes, langue: txt(d.langue), page: txt(d.page) || '/'
  };
}

function titre_(s) {
  return '<tr><td colspan="2" style="padding:16px 0 4px;font-family:Georgia,serif;font-size:17px;color:' + VERT + '">' + s + '</td></tr>';
}

// ---------------------------------------------------------------- mail

function envoyerMail_(d, quand, test) {
  var f = fiche_(d);
  var recu = Utilities.formatDate(quand, TZ, 'dd/MM/yyyy HH:mm');
  var jour = Utilities.formatDate(quand, TZ, 'd MMMM yyyy');

  var sujetBouts = [f.nom, f.lieu, f.dates, f.personnes].filter(function (x) { return x; });
  var sujet = (test ? '[TEST] ' : '') + 'Mishpacha · ' + sujetBouts.join(' · ');

  // version texte (lecteurs sans HTML)
  var corps = ['New request from mishpachatours.com', '--------------------------------',
    'Name: ' + f.nom, 'Trip: ' + (f.tour || '(not specified)'), 'Place: ' + (f.lieu || '(not specified)'),
    'Dates: ' + (f.dates || '(not specified)'), 'People: ' + (f.personnes || '(not specified)'),
    'Reply in: ' + (f.langue || '(not specified)'), 'WhatsApp / email: ' + (txt(d.contact) || '(not specified)'), ''];
  f.paires.forEach(function (kv) { corps.push((kv[0] ? kv[0] + ': ' : '') + kv[1]); });
  corps.push('', 'Page: ' + f.page, 'Received: ' + recu);

  var cle = function (label, valeur) {
    // tuile de resume
    return '<td width="50%" style="padding:0 6px 8px 0;vertical-align:top">' +
      '<div style="background:' + CREME + ';border-radius:12px;padding:10px 12px">' +
      '<div style="font-size:11px;letter-spacing:.06em;text-transform:uppercase;color:' + VERT + ';font-weight:700">' + label + '</div>' +
      '<div style="font-size:15px;font-weight:600;color:' + ENCRE + ';margin-top:3px;line-height:1.3">' + (valeur ? esc_(valeur) : '<span style="color:' + GRIS + ';font-weight:400">not specified</span>') + '</div></div></td>';
  };
  var qui = f.personnes + (f.map['Families'] ? ' · ' + f.map['Families'] + ' families' : '');
  var tuiles = '<table role="presentation" cellpadding="0" cellspacing="0" width="100%"><tr>' +
    cle('Dates', f.dates) + cle('Who', qui) + '</tr><tr>' +
    cle('Where', f.lieu) + cle('Budget', [f.map['Budget per family'] ? f.map['Budget per family'] + ' per family' : '', f.map['Budget per person'] ? f.map['Budget per person'] + ' per person' : '',
                                          f.map['Budget'], f.map['Flights and budget']].filter(Boolean).join(', ')) + '</tr><tr>' +
    cle('Sleeping', [f.map['Accommodation'], f.map['Rooms']].filter(Boolean).join(' · ')) + cle('Meals', [f.map['Meals'], f.map['Kashrut']].filter(Boolean).join(' · ')) + '</tr></table>';

  var ligne = function (label, valeur) {
    return '<tr><td style="padding:8px 0;border-bottom:1px solid ' + BEIGE + ';color:' + GRIS + ';font-size:13px;width:36%;vertical-align:top">' + esc_(label) +
           '</td><td style="padding:8px 0;border-bottom:1px solid ' + BEIGE + ';color:' + ENCRE + ';font-size:14px;vertical-align:top;line-height:1.4">' + esc_(valeur) + '</td></tr>';
  };
  var detail = '';
  var vus = {};
  SECTIONS.forEach(function (sec) {
    var rows = '';
    sec[1].forEach(function (k) { if (f.map[k]) { rows += ligne(k, f.map[k]); vus[k] = 1; } });
    if (rows) detail += titre_(sec[0]) + rows;
  });
  var reste = '';
  f.paires.forEach(function (kv) { if ((!kv[0] || !vus[kv[0]]) && CONTACT_KEYS.indexOf(kv[0]) < 0) reste += ligne(kv[0] || 'Message', kv[1]); });
  if (reste) detail += titre_(f.en ? 'Also' : 'Message') + reste;
  var contactRows = ligne('WhatsApp / email', txt(d.contact) || 'not specified') + (f.langue ? ligne('Reply in', f.langue) : '');
  CONTACT_KEYS.forEach(function (k) { if (f.map[k]) contactRows += ligne(k, f.map[k]); });

  var bouton = function (url, texte, plein) {
    return '<a href="' + url + '" style="display:inline-block;margin:0 8px 8px 0;padding:12px 20px;border-radius:999px;font-size:14px;font-weight:700;text-decoration:none;' +
           (plein ? 'background:' + ENCRE + ';color:#FFFFFF' : 'background:#FFFFFF;color:' + ENCRE + ';border:1px solid ' + ENCRE) + '">' + texte + '</a>';
  };
  var boutons = '';
  if (f.tel.length >= 8) boutons += bouton('https://wa.me/' + f.tel, 'Reply on WhatsApp', true);
  if (f.mail) boutons += bouton('mailto:' + esc_(f.mail), 'Reply by email', !boutons);
  if (!test) { try { boutons += bouton(feuille_().getParent().getUrl(), 'Open the Sheet', false); } catch (err) {} }

  var html =
    '<div style="margin:0;padding:24px 12px;background:' + BEIGE + ';font-family:Arial,Helvetica,sans-serif">' +
    '<table role="presentation" cellpadding="0" cellspacing="0" width="100%" style="max-width:600px;margin:0 auto;background:#FFFFFF;border-radius:16px;overflow:hidden">' +
    '<tr><td style="background:' + VERT + ';padding:20px 28px"><table role="presentation" cellpadding="0" cellspacing="0" width="100%"><tr>' +
    '<td width="56" style="vertical-align:middle"><img src="' + LOGO + '" width="56" height="56" alt="" style="display:block;border:0;border-radius:50%"></td>' +
    '<td style="padding-left:14px;vertical-align:middle;color:' + CREME + ';font-size:12px;letter-spacing:.06em">NEW REQUEST · ' + esc_(jour).toUpperCase() +
    '<div style="margin-top:4px;font-family:Georgia,serif;font-size:26px;letter-spacing:0;color:#FFFFFF">' + esc_(f.nom) + '</div></td></tr></table></td></tr>' +
    '<tr><td style="background:' + JAUNE + ';padding:11px 28px;color:' + ENCRE + ';font-size:15px;font-weight:700">' + esc_(f.tour || 'Trip not specified') + '</td></tr>' +
    '<tr><td style="padding:18px 22px 6px 28px">' + tuiles + '</td></tr>' +
    (boutons ? '<tr><td style="padding:8px 28px 4px">' + boutons + '</td></tr>' : '') +
    '<tr><td style="padding:6px 28px 4px"><table role="presentation" cellpadding="0" cellspacing="0" width="100%">' +
    titre_('Contact') + contactRows + detail +
    '</table></td></tr>' +
    '<tr><td style="padding:18px 28px 22px;color:' + GRIS + ';font-size:12px;line-height:1.5">Attached: the contact sheet for Mendel (French, with WhatsApp), sent to him automatically outside Shabbat, and the detailed request.<br>Received ' + recu + ' (Paris) · page ' + esc_(f.page) + '</td></tr>' +
    '</table></div>';

  var pdf = null, pdfMendel = null;
  try { pdf = pdf_(f, jour); } catch (err) { corps.push('', 'PDF non genere : ' + err); }
  try { pdfMendel = pdfMendel_(ficheMendel_(d, quand)); } catch (err) { corps.push('', 'Fiche Mendel non generee : ' + err); }

  var options = { subject: sujet, body: corps.join('\n'), htmlBody: html, name: 'Mishpacha Tours' };
  if (test) { options.to = TEST_EMAIL; } else { options.to = DEST_EMAIL; options.cc = CC_EMAIL; }
  if (f.mail) options.replyTo = f.mail;
  options.attachments = [pdfMendel, pdf].filter(Boolean);
  MailApp.sendEmail(options);
}

// ---------------------------------------------------------------- PDF « fiche client » (A4, sans coordonnees)

function pdf_(f, jour) {
  var ligne = function (label, valeur) {
    return '<tr><td class="k">' + esc_(label) + '</td><td class="v">' + esc_(valeur) + '</td></tr>';
  };
  var blocs = '';
  var vus = {};
  SECTIONS.forEach(function (sec) {
    var rows = '';
    sec[1].forEach(function (k) { if (f.map[k]) { rows += ligne(k, f.map[k]); vus[k] = 1; } });
    if (rows) blocs += '<h2>' + sec[0] + '</h2><table class="t">' + rows + '</table>';
  });
  var reste = '';
  f.paires.forEach(function (kv) { if ((!kv[0] || !vus[kv[0]]) && CONTACT_KEYS.indexOf(kv[0]) < 0) reste += ligne(kv[0] || 'Message', kv[1]); });
  if (reste) blocs += '<h2>' + (f.en ? 'Also' : 'Message') + '</h2><table class="t">' + reste + '</table>';
  if (!blocs) blocs = '<p>No details given.</p>';

  var tuile = function (label, valeur) {
    return '<td class="c"><div class="cl">' + label + '</div><div class="cv">' + (valeur ? esc_(valeur) : '—') + '</div></td>';
  };
  var qui = f.personnes + (f.map['Families'] ? ' · ' + f.map['Families'] + ' families' : '');
  var html = '<!DOCTYPE html><html><head><meta charset="utf-8"><style>' +
    '@page{size:A4;margin:16mm 16mm 18mm}' +
    'body{font-family:Arial,Helvetica,sans-serif;color:' + ENCRE + ';font-size:11pt;line-height:1.4;margin:0}' +
    '.tete{background:' + VERT + ';color:#fff;padding:14pt 18pt;border-radius:10pt}' +
    '.tete td{vertical-align:middle}' +
    '.sur{font-size:9pt;letter-spacing:.08em;color:' + CREME + '}' +
    'h1{font-family:Georgia,serif;font-weight:normal;font-size:22pt;margin:2pt 0 0;color:#fff}' +
    '.bande{background:' + JAUNE + ';padding:7pt 18pt;font-weight:bold;font-size:11.5pt;border-radius:6pt;margin-top:6pt}' +
    '.cles{width:100%;border-collapse:separate;border-spacing:6pt 0;margin:10pt 0 0}' +
    '.c{background:' + CREME + ';border-radius:8pt;padding:7pt 9pt;width:33%;vertical-align:top}' +
    '.cl{font-size:8pt;letter-spacing:.06em;text-transform:uppercase;color:' + VERT + ';font-weight:bold}' +
    '.cv{font-size:11pt;font-weight:bold;margin-top:2pt}' +
    'h2{font-family:Georgia,serif;font-weight:normal;font-size:14pt;color:' + VERT + ';margin:14pt 0 3pt;border-bottom:1px solid ' + BEIGE + ';padding-bottom:2pt}' +
    '.t{width:100%;border-collapse:collapse}' +
    '.t td{padding:4pt 0;vertical-align:top;border-bottom:1px solid ' + BEIGE + '}' +
    '.k{width:34%;color:' + GRIS + ';font-size:9.5pt;padding-right:8pt}' +
    '.v{font-size:10.5pt}' +
    '.pied{margin-top:16pt;font-size:8.5pt;color:' + GRIS + '}' +
    '</style></head><body>' +
    '<table class="tete" width="100%" cellpadding="0" cellspacing="0"><tr>' +
    '<td width="52"><img src="' + LOGO + '" width="48" height="48" style="border-radius:50%"></td>' +
    '<td style="padding-left:12pt"><div class="sur">MISHPACHA TOURS · TRIP REQUEST · ' + esc_(jour).toUpperCase() + '</div><h1>' + esc_(f.nom) + '</h1></td></tr></table>' +
    '<div class="bande">' + esc_(f.tour || 'Trip not specified') + '</div>' +
    '<table class="cles"><tr>' + tuile('Dates', f.dates) + tuile('Who', qui) + tuile('Where', f.lieu) + '</tr></table>' +
    blocs +
    '<div class="pied">Mishpacha Tours · mishpachatours.com · kosher stays in the French Alps and Jewish Lyon. Client contact details held by Mishpacha Tours.</div>' +
    '</body></html>';
  var nom = 'Mishpacha-request-' + f.nom.replace(/[^A-Za-z0-9À-ɏ ]+/g, ' ').trim().replace(/\s+/g, '-') + '-' + Utilities.formatDate(new Date(), TZ, 'yyyy-MM-dd') + '.pdf';
  return Utilities.newBlob(html, 'text/html', 'fiche.html').getAs('application/pdf').setName(nom);
}

// ---------------------------------------------------------------- fiche contact pour Mendel (FR, avec WhatsApp)

// Ligne de la feuille -> objet d comme celui du site (colonnes ENTETE v2).
function depuisLigne_(v) {
  return { nom: v[2], contact: [v[3], v[4]].filter(Boolean).join(' / '), message_en: v[22], message: txt(v[23]) || txt(v[22]),
           nuits: v[9], dates: [v[7], v[8]].filter(Boolean).join(' → '), personnes: v[11], langue: v[20], page: v[21] };
}

function ficheMendel_(d, quand) {
  var f = fiche_(d), m = f.map;
  var jn = function (a) { return a.filter(Boolean).join(' · '); };
  var log = jn([m['Accommodation'], m['Rooms'], m['Accommodation options']]);
  var chalet = /already|déjà|booked|réservé/i.test(m['Accommodation'] || '') ? 'Non, logement déjà réservé · ' + log
             : /chalet/i.test(m['Accommodation'] || '') ? 'Oui · ' + log : log;
  var enfants = [m['Children'], m['Babies'] && m['Babies'] !== '0' ? m['Babies'] + ' bébé(s)' : ''].filter(Boolean).join(' + ');
  var autres = [['Minyan', jn([m['Minyan level'], m['Religious needs'], m['Nusach']])], ['Vols', jn([m['Airport'], m['Flying from'], m['Flights booked']])],
                ['Activités', m['Activities']], ['Extras', m['Extras']], ['Allergies', m['Allergies and diets']],
                ['Matériel bébé', m['Baby equipment']], ['Priorités', m['Priorities']], ['Urgence', m['Urgency']]]
    .filter(function (kv) { return kv[1]; }).map(function (kv) { return kv[0] + ' : ' + kv[1]; });
  return {
    id: String(quand.getTime()), nom: f.nom, recu: Utilities.formatDate(quand, TZ, "d/MM/yyyy 'à' HH'h'mm"),
    pays: m['Lives in'] || '', whatsapp: f.tel ? '+' + f.tel : '', dates: f.dates, station: f.lieu,
    adultes: (m['Adults'] || txt(d.personnes)) + (m['Families'] && m['Families'] !== '1' ? ' (' + m['Families'] + ' familles)' : ''),
    enfants: enfants || '0', hommes: m['Men for minyan'] || '?', chalet: chalet,
    repas: jn([m['Meals'], m['Meal days'], m['Kashrut']]),
    budget: jn([m['Budget per person'] ? m['Budget per person'] + ' / pers.' : '', m['Budget per family'] ? m['Budget per family'] + ' / famille' : '',
                m['Budget'], m['Flights and budget']]),
    message: m['Message'] || '', autres: autres
  };
}

function pdfMendel_(x) {
  var NUIT = '#141416', OR = '#C9A961', NEIGE = '#EEF1F8', FILET = '#E2DCCF', GRIS2 = '#5A6068';
  // Le convertisseur PDF de Google ignore les fonds (background et bgcolor) : tout passe par des bordures.
  var tuile = function (l, v) {
    return '<td width="33%" style="border:1px solid ' + FILET + ';border-top:5px solid ' + NUIT + ';padding:10px 14px;vertical-align:top"><div style="font-size:8pt;text-transform:uppercase;color:' + OR + ';font-weight:bold">' + l +
      '</div><div style="font-size:18pt;font-weight:bold;color:' + NUIT + ';margin-top:3px">' + esc_(v || '—') + '</div></td>';
  };
  var lignes = [['Pays', x.pays], ['WhatsApp', x.whatsapp], ['Dates', x.dates], ['Station', x.station], ['Chalet', x.chalet], ['Repas', x.repas], ['Budget', x.budget]]
    .map(function (kv) {
      return '<tr><td width="24%" style="padding:7px 10px 7px 0;border-bottom:1px solid ' + FILET + ';font-size:8.5pt;text-transform:uppercase;color:' + GRIS2 +
        ';vertical-align:top">' + kv[0] + '</td><td style="padding:7px 0;border-bottom:1px solid ' + FILET + ';font-size:10.5pt">' + esc_(kv[1] || 'Non indiqué') + '</td></tr>';
    }).join('');
  var msg = [x.message].concat(x.autres).filter(Boolean).map(esc_).join('<br>') || 'Aucun message.';
  var html = '<!DOCTYPE html><html><head><meta charset="utf-8"><style>@page{size:A4;margin:14mm 16mm}</style></head>' +
    '<body style="margin:0;font-family:Arial,Helvetica,sans-serif;color:' + ENCRE + '">' +
    '<table width="100%" cellpadding="0" cellspacing="0"><tr><td style="vertical-align:middle"><img src="' + LOGO_MT_LONG + '" width="230"></td>' +
    '<td style="text-align:right;vertical-align:middle"><div style="font-size:7.5pt;text-transform:uppercase;color:' + GRIS2 + ';margin-bottom:4px">En partenariat avec</div>' +
    '<img src="' + LOGO_WP_LONG + '" width="170"></td></tr></table>' +
    '<div style="border-top:3px solid ' + OR + ';margin:16px 0 18px"></div>' +
    '<div style="font-size:8.5pt;text-transform:uppercase;color:' + VERT + ';font-weight:bold">Fiche contact · reçu le ' + esc_(x.recu) + '</div>' +
    '<div style="font-family:Georgia,serif;font-size:28pt;margin:4px 0 2px">' + esc_(x.nom) + '</div>' +
    '<div style="font-size:8.5pt;color:' + GRIS2 + ';margin-bottom:14px">Données du formulaire, non vérifiées : à confirmer avec le client.</div>' +
    '<table width="100%" cellpadding="0" cellspacing="6"><tr>' + tuile('Adultes', x.adultes) + tuile('Enfants', x.enfants) + tuile('Hommes', x.hommes) + '</tr></table>' +
    '<table width="100%" cellpadding="0" cellspacing="0" style="margin-top:12px">' + lignes + '</table>' +
    '<table width="100%" cellpadding="0" cellspacing="0" style="margin-top:16px"><tr><td style="border:1px solid ' + FILET + ';border-left:4px solid ' + OR + ';padding:12px 14px">' +
    '<div style="font-size:8.5pt;text-transform:uppercase;color:' + VERT + ';font-weight:bold;margin-bottom:5px">Message</div>' +
    '<div style="font-size:10pt;line-height:1.5">' + msg + '</div></td></tr></table>' +
    '<div style="font-size:7.5pt;color:' + GRIS2 + ';margin-top:18px;border-top:1px solid ' + FILET + ';padding-top:8px">Mishpacha Tours en partenariat avec Winter Prestige · document interne, ne pas transférer au client</div>' +
    '</body></html>';
  var nom = 'Fiche-' + x.nom.replace(/[^A-Za-z0-9À-ɏ ]+/g, ' ').trim().replace(/\s+/g, '-') + '.pdf';
  return Utilities.newBlob(html, 'text/html', 'fiche.html').getAs('application/pdf').setName(nom);
}

function legendeMendel_(x) {
  var qui = x.adultes + ' adultes' + (x.enfants && x.enfants !== '0' ? ', ' + x.enfants + ' enfants' : '');
  return 'Mendel, nouvelle demande 📎\n' + x.nom + (x.station ? ', ' + x.station : '') + '\n' + (x.dates ? x.dates + '\n' : '') + qui +
    (x.whatsapp ? '\nWhatsApp : ' + x.whatsapp : '') + '\nTout est dans la fiche 🙏';
}

// File d'envoi lue par le serveur WhatsApp du CRM. Les ids envoyes vivent dans les proprietes du script.
function fileMendel_(action, id) {
  var props = PropertiesService.getScriptProperties();
  var faits = JSON.parse(props.getProperty('MENDEL_ENVOYES') || '[]');
  if (action === 'fait') {
    if (id && faits.indexOf(id) < 0) { faits.push(id); props.setProperty('MENDEL_ENVOYES', JSON.stringify(faits.slice(-500))); }
    return { ok: true };
  }
  var vals = feuille_().getDataRange().getValues().slice(1);
  var lignes = vals.filter(function (v) { return v[0] instanceof Date; }).map(function (v) { return { v: v, id: String(v[0].getTime()) }; });
  if (action === 'fiche') {
    var l = lignes.filter(function (x) { return x.id === id; })[0];
    if (!l) return { ok: false, error: 'id inconnu' };
    var x = ficheMendel_(depuisLigne_(l.v), l.v[0]);
    var b = pdfMendel_(x);
    return { ok: true, id: id, nom: b.getName(), legende: legendeMendel_(x), pdf: Utilities.base64Encode(b.getBytes()) };
  }
  return { ok: true, attente: lignes.filter(function (x) {
    return x.v[0] >= ENVOI_DEPUIS && txt(x.v[1]) !== 'Test' && faits.indexOf(x.id) < 0;
  }).map(function (x) { return { id: x.id, nom: txt(x.v[2]) }; }) };
}

// ---------------------------------------------------------------- utilitaires

// Journal des 30 derniers passages de doPost (lu par doGet action=journal avec la cle) : sans lui, aucune trace
// d'une demande perdue (19/10, demande de Moshe jamais arrivee).
function journal_(quoi, detail) {
  try {
    var props = PropertiesService.getScriptProperties();
    var j = JSON.parse(props.getProperty('JOURNAL') || '[]');
    j.push([Utilities.formatDate(new Date(), TZ, 'dd/MM HH:mm:ss'), quoi, String(detail).slice(0, 300)]);
    props.setProperty('JOURNAL', JSON.stringify(j.slice(-30)));
  } catch (e) {}
}

function esc_(v) {
  return String(v).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}

function txt(v) { return String(v == null ? '' : v).trim(); }

// Une valeur qui commence par + = - ou @ (ex. "+33 6...") est lue comme une formule par Sheets
// et affiche #ERROR! : l'apostrophe en tete force le texte, elle ne s'affiche pas dans la cellule.
function cel_(v) { var t = txt(v); return /^[+=\-@]/.test(t) ? "'" + t : t; }

function json_(o) {
  return ContentService.createTextOutput(JSON.stringify(o)).setMimeType(ContentService.MimeType.JSON);
}
