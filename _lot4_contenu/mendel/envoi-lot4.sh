#!/bin/bash
# Lot 4 Mishpacha (06/11/2026) : 8 messages a Mendel (+33 7 81 82 31 93), un toutes les 75 s, programme a 9 h 30 Europe/Paris.
# Reessaie 10 fois par message si le verrou WhatsApp est pris, puis s'efface de la crontab. Annuler avant : crontab -l | grep -v envoi-lot4 | crontab -
cd /home/moche/crm
LOG=/home/moche/crm/etat/envoi-lot4.log
MARQ=/home/moche/crm/etat/envoi-lot4.fait
[ -f "$MARQ" ] && exit 0
for F in /home/moche/crm/etat/lot4/0*.txt; do
  for i in $(seq 1 10); do
    echo "$(date '+%F %T') $F essai $i" >> "$LOG"
    if node src/envoyer-texte.js +33781823193 < "$F" >> "$LOG" 2>&1; then echo "$(date '+%F %T') OK $F" >> "$LOG"; break; fi
    sleep 60
  done
  sleep 75
done
date > "$MARQ"
crontab -l | grep -v envoi-lot4.sh | crontab -
