/**
 * Mishpacha Tours - reception du formulaire de reservation
 * ---------------------------------------------------------------------
 * doPost lit le JSON envoye par sendBeacon depuis index.html, ecrit une
 * ligne horodatee dans la feuille active et envoie un email a
 * contact@mishpachatours.com via MailApp.
 *
 * INSTALLATION (a faire par l'operateur, voir README.md)
 *   1. Google Sheets : creer une feuille nommee "Mishpacha - Leads".
 *   2. Extensions > Apps Script, coller ce fichier en entier, Enregistrer.
 *   3. Deployer > Nouveau deploiement > type "Application web".
 *      Executer en tant que : Moi. Qui a acces : Tout le monde.
 *   4. Copier l'URL /exec et la coller dans index.html (voir README.md).
 * ---------------------------------------------------------------------
 */

var DEST_EMAIL = 'contact@mishpachatours.com';
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
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var sh = ss.getActiveSheet();
  if (sh.getLastRow() === 0) {
    sh.appendRow(ENTETE);
    sh.setFrozenRows(1);
  }
  return sh;
}

function envoyerMail_(d, quand) {
  var sujet = 'New tour request - ' + (txt(d.tour) || 'Mishpacha Tours') + ' - ' + (txt(d.nom) || 'no name');
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
    'Received: ' + Utilities.formatDate(quand, TZ, 'dd/MM/yyyy HH:mm')
  ].join('\n');
  MailApp.sendEmail(DEST_EMAIL, sujet, corps);
}

function txt(v) { return String(v == null ? '' : v).trim(); }

function json_(o) {
  return ContentService.createTextOutput(JSON.stringify(o)).setMimeType(ContentService.MimeType.JSON);
}
