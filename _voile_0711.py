# -*- coding: utf-8 -*-
"""Voile du héros des 4 accueils renforcé sous le bloc titre (Moshé 05/11 : titre lisible, ≥ 4,5:1, sur la pire image de la vidéo ;
le voile radial centré du 02/11 ne couvrait pas le bloc titre, posé en bas : 1,1:1 sur iPhone à 5,5 s, plan du skieur).
Mesure : 06-reports/2026-11-05-video-accueil/contraste_accueil.py. Idempotent (marqueur VOILE-0711 dans lv.css). Depuis site-v5/ :
python _voile_0711.py"""
import io, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
SEL = "html body.valora.lv:not(#lv1):not(#lv2):not(#lv3):not(#lv4):not(#lv5):not(#lv6):not(#lv7) .ac-hero::before"
BLOC = f"""
/* ===VOILE-0711=== héros d'accueil : voile sombre sous le bloc titre (texte de 55 % à 93 % de la hauteur sur téléphone, 62 % à 95 % sur ordinateur), haut de la vidéo presque libre */
{SEL}{{background:linear-gradient(180deg,rgba(0,0,0,.16) 0%,rgba(0,0,0,.06) 30%,rgba(0,0,0,.36) 46%,rgba(0,0,0,.70) 56%,rgba(0,0,0,.78) 100%) !important}}
@media (min-width:900px){{{SEL}{{background:linear-gradient(180deg,rgba(0,0,0,.16) 0%,rgba(0,0,0,.05) 36%,rgba(0,0,0,.36) 52%,rgba(0,0,0,.70) 62%,rgba(0,0,0,.78) 100%) !important}}}}
/* ===/VOILE-0711=== */
"""
s = io.open("lv.css", encoding="utf-8", newline="").read()
if "VOILE-0711" in s: print("déjà fait")
else: io.open("lv.css", "a", encoding="utf-8", newline="").write(BLOC); print("bloc VOILE-0711 ajouté à lv.css")
