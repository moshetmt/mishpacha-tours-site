/**
 * Mishpacha Tours - reception du formulaire de reservation
 * ---------------------------------------------------------------------
 * doPost lit le JSON envoye par sendBeacon depuis index.html, ecrit une
 * ligne horodatee dans la feuille active et envoie un email a
 * contact@mishpachatours.com via MailApp.
 *
 * INSTALLATION (a faire par l'operateur, voir README.md)
 *   Projet cree et deploye par l'API (scripts/creer_apps_script_mishpacha.py, 08/10/2026).
 *   La feuille "Mishpacha - Leads" est creee au premier envoi (voir feuille_).
 *   Autorisation : ouvrir le script, executer urlFeuille() une fois, accepter.
 *   L'URL /exec vit dans config.js.
 * ---------------------------------------------------------------------
 */

var DEST_EMAIL = 'contact@mishpachatours.com, mochetimsit@gmail.com';
var CC_EMAIL = 'timsitelis613@gmail.com';   // la guide, en copie de chaque demande (operateur, 11/10)
var ENTETE = ['Date', 'Tour', 'Dates', 'Nombre de personnes', 'Langue', 'Nom',
              'Email ou WhatsApp', 'Message', 'Page', 'Source'];
var TZ = 'Europe/Paris';

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

    // Piege a robots : le champ "societe" doit rester vide, un humain ne le voit jamais.
    if (txt(d.societe)) return json_({ ok: true, piege: true });

    // Rien d'exploitable : ni nom ni contact.
    if (!txt(d.nom) && !txt(d.contact)) return json_({ ok: true, vide: true });

    var sh = feuille_();
    var quand = new Date();
    sh.appendRow([
      quand, txt(d.tour), txt(d.dates), txt(d.personnes), txt(d.langue),
      txt(d.nom), txt(d.contact), txt(d.message), txt(d.page), txt(d.params)
    ]);

    envoyerMail_(d, quand);
    return json_({ ok: true });

  } catch (err) {
    return json_({ ok: false, error: String(err) });
  } finally {
    try { lock.releaseLock(); } catch (err2) {}
  }
}

function doGet(e) {
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
  var sh = ss.getSheets()[0];
  if (sh.getLastRow() === 0) {
    sh.appendRow(ENTETE);
    sh.setFrozenRows(1);
  }
  return sh;
}

function urlFeuille() {
  // A lancer une fois dans l'editeur : autorise le script et affiche l'URL de la feuille.
  var sh = feuille_();
  var url = sh.getParent().getUrl();
  Logger.log(url);
  return url;
}

function envoyerMail_(d, quand) {
  var sujet = 'New tour request - ' + (txt(d.tour) || 'Mishpacha Tours') + ' - ' + (txt(d.nom) || 'no name');
  var recu = Utilities.formatDate(quand, TZ, 'dd/MM/yyyy HH:mm');
  var corps = [
    'New booking request from mishpachatours.com',
    '--------------------------------',
    'Tour: ' + (txt(d.tour) || '(not specified)'),
    'Dates: ' + (txt(d.dates) || '(not specified)'),
    'Number of people: ' + (txt(d.personnes) || '(not specified)'),
    'Tour language: ' + (txt(d.langue) || '(not specified)'),
    'Name: ' + (txt(d.nom) || '(not specified)'),
    'WhatsApp / email: ' + (txt(d.contact) || '(not specified)'),
    'Message: ' + (txt(d.message) || '(empty)'),
    '',
    'Page: ' + (txt(d.page) || '/'),
    'Received: ' + recu
  ].join('\n');

  // contact = "+1 2125550100 / nom@exemple.com" : on separe le numero et l'e-mail.
  var contact = txt(d.contact);
  var mail = (contact.match(/[^\s\/]+@[^\s\/]+\.[^\s\/]+/) || [''])[0];
  var tel = contact.replace(mail, '').replace(/[^0-9]/g, '');

  var ligne = function (label, valeur) {
    return '<tr><td style="padding:10px 0;border-bottom:1px solid #F1EDE6;color:#35705A;font-size:13px;width:38%;vertical-align:top">' + label +
           '</td><td style="padding:10px 0;border-bottom:1px solid #F1EDE6;color:#1C1B1F;font-size:15px;font-weight:600;vertical-align:top">' +
           (valeur ? esc_(valeur) : '<span style="color:#9a968f;font-weight:400">not specified</span>') + '</td></tr>';
  };
  var bouton = function (url, texte, plein) {
    return '<a href="' + url + '" style="display:inline-block;margin:0 8px 8px 0;padding:13px 22px;border-radius:999px;font-size:15px;font-weight:700;text-decoration:none;' +
           (plein ? 'background:#1C1B1F;color:#FFFFFF' : 'background:#FFFFFF;color:#1C1B1F;border:1px solid #1C1B1F') + '">' + texte + '</a>';
  };
  var boutons = '';
  if (tel.length >= 8) boutons += bouton('https://wa.me/' + tel, 'Reply on WhatsApp', true);
  if (mail) boutons += bouton('mailto:' + esc_(mail), 'Reply by email', !boutons);

  var html =
    '<div style="margin:0;padding:24px 12px;background:#FFFAED;font-family:Arial,Helvetica,sans-serif">' +
    '<table role="presentation" cellpadding="0" cellspacing="0" width="100%" style="max-width:560px;margin:0 auto;background:#FFFFFF;border-radius:15px;overflow:hidden">' +
    '<tr><td style="background:#2D5132;padding:20px 28px"><table role="presentation" cellpadding="0" cellspacing="0" width="100%"><tr>' +
    '<td width="64" style="vertical-align:middle"><img src="https://mishpachatours.com/img/apple-touch-icon.png" width="64" height="64" alt="Mishpacha Tours" style="display:block;border:0;border-radius:50%"></td>' +
    '<td style="padding-left:16px;vertical-align:middle;color:#FFFAED;font-size:13px;letter-spacing:.04em">MISHPACHA TOURS' +
    '<div style="margin-top:6px;font-family:Georgia,serif;font-size:24px;letter-spacing:0;color:#FFFFFF">New request' +
    (txt(d.nom) ? ' from ' + esc_(txt(d.nom)) : '') + '</div></td></tr></table></td></tr>' +
    '<tr><td style="background:#FCDE73;padding:12px 28px;color:#1C1B1F;font-size:15px;font-weight:700">' +
    esc_(txt(d.tour) || 'Tour not specified') + '</td></tr>' +
    '<tr><td style="padding:14px 28px 6px"><table role="presentation" cellpadding="0" cellspacing="0" width="100%">' +
    ligne('Dates', txt(d.dates)) +
    ligne('Number of people', txt(d.personnes)) +
    ligne('Tour language', txt(d.langue)) +
    ligne('Name', txt(d.nom)) +
    ligne('WhatsApp / email', contact) +
    (txt(d.message) ? ligne('Message', txt(d.message)) : '') +
    '</table></td></tr>' +
    (boutons ? '<tr><td style="padding:18px 28px 10px">' + boutons + '</td></tr>' : '') +
    '<tr><td style="padding:14px 28px 22px;color:#8a867f;font-size:12px">Received ' + recu + ' (Paris) · page ' +
    esc_(txt(d.page) || '/') + '</td></tr>' +
    '</table></div>';

  var options = { to: DEST_EMAIL, cc: CC_EMAIL, subject: sujet, body: corps, htmlBody: html, name: 'Mishpacha Tours' };
  if (mail) options.replyTo = mail;
  MailApp.sendEmail(options);
}

function esc_(v) {
  return String(v).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}

function txt(v) { return String(v == null ? '' : v).trim(); }

function json_(o) {
  return ContentService.createTextOutput(JSON.stringify(o)).setMimeType(ContentService.MimeType.JSON);
}
